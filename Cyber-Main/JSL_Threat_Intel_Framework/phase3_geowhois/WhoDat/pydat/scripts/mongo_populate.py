#!/usr/bin/env python

import sys
import os
import unicodecsv
import hashlib
import signal
import time
from optparse import OptionParser
import pymongo
from pymongo import MongoClient
import threading
from threading import Thread, Lock
import Queue
import multiprocessing  # for num cpus
from multiprocessing import Process, Queue as mpQueue
from pprint import pprint

STATS = {'total': 0,
         'new': 0,
         'updated': 0,
         'unchanged': 0,
         'duplicates': 0
         }
STATS_LOCK = Lock()

VERSION_KEY = 'dataVersion'
UNIQUE_KEY = 'dataUniqueID'
FIRST_SEEN = 'dataFirstSeen'

CHANGEDCT = {}

shutdown_event = threading.Event()


######## READER THREAD ######
def reader_worker(work_queue, collection, options):
    if options.directory:
        scan_directory(work_queue, collection, options.directory, options)
    elif options.file:
        parse_csv(work_queue, collection, options.file, options)
    else:
        print "File or Directory required"


def scan_directory(work_queue, collection, directory, options):
    for root, subdirs, filenames in os.walk(directory):
        if len(subdirs):
            for subdir in subdirs:
                scan_directory(work_queue, collection, subdir, options)
        for filename in filenames:
            if options.extension != '':
                fn, ext = os.path.splitext(filename)
                if ext and ext[1:] != options.extension:
                    continue

            full_path = os.path.join(root, filename)
            parse_csv(work_queue, collection, full_path, options)


def check_header(header):
    for field in header:
        if field == "domainName":
            return True

    return False


def parse_csv(work_queue, collection, filename, options):
    if options.verbose:
        print "Processing file: %s" % filename

    csvfile = open(filename, 'rb')
    dnsreader = unicodecsv.reader(csvfile, strict=True, skipinitialspace=True)
    try:
        header = dnsreader.next()
        if not check_header(header):
            raise unicodecsv.Error('CSV header not found')

        for row in dnsreader:
            work_queue.put({'header': header, 'row': row})
    except unicodecsv.Error, e:
        sys.stderr.write(
            "CSV Parse Error in file %s - line %i\n\t%s\n" % (os.path.basename(filename), dnsreader.line_num, str(e)))


###### MONGO PROCESS ######

def mongo_worker(insert_queue, options):
    # Ignore signals that are sent to parent process
    # The parent should properly shut this down
    os.setpgrp()

    bulk_counter = 0
    client = MongoClient(host=options.mongo_host, port=options.mongo_port)
    whodb = client[options.database]
    collection = whodb[options.collection]
    finishup = False
    bulk = collection.initialize_unordered_bulk_op()

    while not finishup:
        request = insert_queue.get()
        if not isinstance(request, basestring):
            if request['type'] == 'insert':
                bulk.insert(request['insert'])
                bulk_counter += 1
            elif request['type'] == 'update':
                bulk.find(request['find']).update(request['update'])
                bulk_counter += 1
            else:
                print "Unrecognized"
        else:
            finishup = True

        if ((bulk_counter >= options.bulk_size) or finishup) and bulk_counter > 0:
            finished_bulk = bulk
            bulk = collection.initialize_unordered_bulk_op()
            bulk_counter = 0

            try:
                finished_bulk.execute()
            except pymongo.bulk.BulkWriteError as bwe:
                details = bwe.details
                if options.vverbose:
                    pprint(bwe.details, stream=sys.stderr)
                elif options.verbose:
                    for error in details['writeErrors']:
                        sys.stderr.write("Error inserting/updating %s\n\tmessage: %s\n" % (
                            error['op']['domainName'], error['errmsg'].encode('ascii', 'replace')))
            except Exception as e:
                sys.stderr.write("Error inserting/updating: %s\n" % str(e))


######## WORKER THREADS #########

def update_required(collection, header, input_entry, options):
    if len(input_entry) == 0:
        return False

    current_entry = None
    domainName = ''
    for i, item in enumerate(input_entry):
        if header[i] == 'domainName':
            domainName = item
            break

    current_entry = find_entry(collection, domainName)

    if current_entry is None:
        return True

    if current_entry[VERSION_KEY] == options.identifier:  # This record already up to date
        return False
    else:
        return True


def update_stats(stat):
    global STATS_LOCK
    global STATS
    STATS_LOCK.acquire()
    try:
        STATS[stat] += 1
    finally:
        STATS_LOCK.release()


def process_worker(work_queue, insert_queue, collection, options):
    global shutdown_event
    while not shutdown_event.isSet():
        work = work_queue.get()
        process_entry(insert_queue, collection, work['header'], work['row'], options)
        work_queue.task_done()


def process_reworker(work_queue, insert_queue, collection, options):
    global shutdown_event
    while not shutdown_event.isSet():
        work = work_queue.get()
        if update_required(collection, work['header'], work['row'], options):
            process_entry(insert_queue, collection, work['header'], work['row'], options)
        work_queue.task_done()


def process_entry(insert_queue, collection, header, input_entry, options):
    global VERSION_KEY
    global STATS

    update_stats('total')
    if len(input_entry) == 0:
        return

    current_entry = None
    details = {}
    domainName = ''
    for i, item in enumerate(input_entry):
        if header[i] == 'domainName':
            if options.vverbose:
                print "Processing domain: %s" % item
            domainName = item
            continue
        details[header[i]] = item

    entry = {
        VERSION_KEY: options.identifier,
        FIRST_SEEN: options.identifier,
        'details': details,
        'domainName': domainName,
    }

    current_entry = find_entry(collection, domainName)

    global CHANGEDCT
    if current_entry:
        if current_entry[VERSION_KEY] == options.identifier:  # duplicate entry in source csv's?
            update_stats('duplicates')
            return

        if options.exclude is not None:
            details_copy = details.copy()
            for exclude in options.exclude:
                del details_copy[exclude]

            changed = set(details_copy.items()) - set(current_entry['details'].items())
            diff = len(set(details_copy.items()) - set(current_entry['details'].items())) > 0

        elif options.include is not None:
            details_copy = {}
            for include in options.include:
                try:  # TODO
                    details_copy[include] = details[include]
                except:
                    pass

            changed = set(details_copy.items()) - set(current_entry['details'].items())
            diff = len(set(details_copy.items()) - set(current_entry['details'].items())) > 0

        else:
            changed = set(details.items()) - set(current_entry['details'].items())
            diff = len(set(details.items()) - set(current_entry['details'].items())) > 0

            # The above diff doesn't consider keys that are only in the latest in mongo
            # So if a key is just removed, this diff will indicate there is no difference
            # even though a key had been removed.
            # I don't forsee keys just being wholesale removed, so this shouldn't be a problem
        for ch in changed:
            if ch[0] not in CHANGEDCT:
                CHANGEDCT[ch[0]] = 0
            CHANGEDCT[ch[0]] += 1

        if diff:
            update_stats('updated')
            if options.vverbose:
                print "Creating entry for updated domain %s" % domainName

            entry[FIRST_SEEN] = current_entry[FIRST_SEEN]
            entry[UNIQUE_KEY] = generate_id(domainName, options.identifier)
            insert_queue.put({'type': 'insert', 'insert': entry})
        else:
            update_stats('unchanged')
            if options.vverbose:
                print "Unchanged entry for %s" % domainName
            insert_queue.put({'type': 'update', 'find': {UNIQUE_KEY: current_entry[UNIQUE_KEY]},
                              'update': {'$set': {'details': details, VERSION_KEY: options.identifier}}})
    else:
        update_stats('new')
        if options.vverbose:
            print "Creating new entry for %s" % domainName
        entry[UNIQUE_KEY] = generate_id(domainName, options.identifier)
        insert_queue.put({'type': 'insert', 'insert': entry})


def generate_id(domainName, identifier):
    dhash = hashlib.md5(domainName).hexdigest() + str(identifier)
    return dhash


def find_entry(collection, domainName):
    try:
        entry = collection.find({"domainName": domainName}, sort=[(VERSION_KEY, pymongo.DESCENDING)])[0]
    except IndexError:
        return None

    return entry


###### MAIN ######

def main():
    global STATS
    global VERSION_KEY
    global CHANGEDCT
    global shutdown_event

    def signal_handler(signum, frame):
        signal.signal(signal.SIGINT, SIGINT_ORIG)
        sys.stdout.write("\rCleaning Up ... Please Wait ...\n")
        shutdown_event.set()

        # Let the current workload finish
        sys.stdout.write("\tStopping Workers\n")
        for t in threads:
            t.join(1)

        insert_queue.put("finished")

        # Give the Mongo process 5 seconds to exit
        mongo_worker_thread.join(5)

        # If it's still alive, terminate it
        if mongo_worker_thread.is_alive():
            try:
                mongo_worker_thread.terminate()
            except:
                pass

        # Attempt to update the stats
        try:
            meta.update({'metadata': options.identifier}, {'$set': {
                'total': STATS['total'],
                'new': STATS['new'],
                'updated': STATS['updated'],
                'unchanged': STATS['unchanged'],
                'duplicates': STATS['duplicates'],
                'changed_stats': CHANGEDCT
            }
            });
        except:
            pass

        sys.stdout.write("... Done\n")

        sys.exit(0)

    optparser = OptionParser(usage='usage: %prog [options]')
    optparser.add_option("-f", "--file", action="store", dest="file",
                         default=None, help="Input CSV file")
    optparser.add_option("-d", "--directory", action="store", dest="directory",
                         default=None, help="Directory to recursively search for CSV files - prioritized over 'file'")
    optparser.add_option("-e", "--extension", action="store", dest="extension",
                         default='csv',
                         help="When scanning for CSV files only parse files with given extension (default: 'csv')")
    optparser.add_option("-i", "--identifier", action="store", dest="identifier", type="int",
                         default=None,
                         help="Numerical identifier to use in update to signify version (e.g., '8' or '20140120')")
    optparser.add_option("-m", "--mongo-host", action="store", dest="mongo_host",
                         default='localhost', help="Location of mongo db/cluster")
    optparser.add_option("-p", "--mongo-port", action="store", dest="mongo_port", type="int",
                         default=27017, help="Location of mongo db/cluster")
    optparser.add_option("-b", "--database", action="store", dest="database",
                         default='whois', help="Name of database to use (default: 'whois')")
    optparser.add_option("-c", "--collection", action="store", dest="collection",
                         default='whois', help="Name of collection to use (default: 'whois')")
    optparser.add_option("-t", "--threads", action="store", dest="threads", type="int",
                         default=multiprocessing.cpu_count(), help="Number of worker threads")
    optparser.add_option("-B", "--bulk-size", action="store", dest="bulk_size", type="int",
                         default=1000, help="Size of Bulk Insert Requests")
    optparser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                         default=False, help="Be verbose")
    optparser.add_option("--vverbose", action="store_true", dest="vverbose",
                         default=False, help="Be very verbose (Prints status of every domain parsed, very noisy)")
    optparser.add_option("-s", "--stats", action="store_true", dest="stats",
                         default=False, help="Print out Stats after running")
    optparser.add_option("-x", "--exclude", action="store", dest="exclude",
                         default="", help="Comma separated list of keys to exclude if updating entry")
    optparser.add_option("-n", "--include", action="store", dest="include",
                         default="",
                         help="Comma separated list of keys to include if updating entry (mutually exclusive to -x)")
    optparser.add_option("-o", "--comment", action="store", dest="comment",
                         default="", help="Comment to store with metadata")
    optparser.add_option("-r", "--redo", action="store_true", dest="redo",
                         default=False,
                         help="Attempt to re-import a failed import or import more data, uses stored metatdata for previous import (-o and -x not required and will be ignored!!)")

    (options, args) = optparser.parse_args()

    if options.vverbose:
        options.verbose = True

    threads = []
    work_queue = Queue.Queue(maxsize=options.bulk_size)
    insert_queue = mpQueue(maxsize=options.bulk_size)

    client = MongoClient(host=options.mongo_host, port=options.mongo_port)
    whodb = client[options.database]
    collection = whodb[options.collection]
    meta = whodb[options.collection + '_meta']

    if options.identifier is None and options.redo is False:
        print "Identifier required"
        sys.exit(1)
    elif options.identifier is not None and options.redo is True:
        print "Redo requested and Identifier Specified. Please choose one or the other"
        sys.exit(1)
    elif options.exclude != "" and options.include != "":
        print "Options include and exclude are mutually exclusive, choose only one"
        sys.exit(1)

    metadata = meta.find_one({'metadata': 0})
    meta_id = None
    if metadata is None:  # Doesn't exist
        if options.redo is False:
            md = {
                'metadata': 0,
                'firstVersion': options.identifier,
                'lastVersion': options.identifier,
            }
            meta_id = meta.insert(md)
            metadata = meta.find_one({'_id': meta_id})

            # Setup indexes
            collection.ensure_index(UNIQUE_KEY, background=True, unique=True)
            collection.ensure_index(VERSION_KEY, background=True)
            collection.ensure_index('domainName', background=True)
            collection.ensure_index([('domainName', pymongo.ASCENDING), (VERSION_KEY, pymongo.ASCENDING)],
                                    background=True)
            collection.ensure_index('details.contactEmail', background=True)
            collection.ensure_index('details.registrant_name', background=True)
            collection.ensure_index('details.registrant_telephone', background=True)
        else:
            print "Cannot redo when no initial import exists"
            sys.exit(1)
    else:
        if options.redo is False:  # Identifier is auto-pulled from db, no need to check
            if options.identifier < 1:
                print "Identifier must be greater than 0"
                sys.exit(1)
            if metadata['lastVersion'] >= options.identifier:
                print "Identifier must be 'greater than' previous identifier"
                sys.exit(1)
        meta_id = metadata['_id']

    if options.redo is False:
        if options.exclude != "":
            options.exclude = options.exclude.split(',')
        else:
            options.exclude = None

        if options.include != "":
            options.include = options.include.split(',')
        else:
            options.include = None

        # Start worker threads
        if options.verbose:
            print "Starting %i worker threads" % options.threads

        for i in range(options.threads):
            t = Thread(target=process_worker,
                       args=(work_queue,
                             insert_queue,
                             collection,
                             options),
                       name='Worker %i' % i)
            t.daemon = True
            t.start()
            threads.append(t)

        # Upate the lastVersion in the metadata
        meta.update({'_id': meta_id}, {'$set': {'lastVersion': options.identifier}})
        # Create the entry for this import
        meta_struct = {
            'metadata': options.identifier,
            'comment': options.comment,
            'total': 0,
            'new': 0,
            'updated': 0,
            'unchanged': 0,
            'duplicates': 0,
            'changed_stats': {}
        }

        if options.exclude != None:
            meta_struct['excluded_keys'] = options.exclude
        elif options.include != None:
            meta_struct['included_keys'] = options.include

        meta.insert(meta_struct)

    else:  # redo is True
        # Get the record for the attempted import
        options.identifier = int(metadata['lastVersion'])
        redo_record = meta.find_one({'metadata': options.identifier})

        if 'excluded_keys' in redo_record:
            options.exclude = redo_record['excluded_keys']
        else:
            options.exclude = None

        if 'included_keys' in redo_record:
            options.include = redo_record['included_keys']
        else:
            options.include = None

        options.comment = redo_record['comment']
        STATS['total'] = int(redo_record['total'])
        STATS['new'] = int(redo_record['new'], )
        STATS['updated'] = int(redo_record['updated'])
        STATS['unchanged'] = int(redo_record['unchanged'])
        STATS['duplicates'] = int(redo_record['duplicates'])
        CHANGEDCT = redo_record['changed_stats']

        if options.verbose:
            print "Re-importing for: \n\tIdentifier: %s\n\tComment: %s" % (options.identifier, options.comment)

        for ch in CHANGEDCT.keys():
            CHANGEDCT[ch] = int(CHANGEDCT[ch])

        # Start the reworker threads
        if options.verbose:
            print "Starting %i reworker threads" % options.threads

        for i in range(options.threads):
            t = Thread(target=process_reworker,
                       args=(work_queue,
                             insert_queue,
                             collection,
                             options),
                       name='Worker %i' % i)
            t.daemon = True
            t.start()
            threads.append(t)
            # No need to update lastVersion or create metadata entry

    # Start up the Mongo Bulk Processor
    mongo_worker_thread = Process(target=mongo_worker, args=(insert_queue, options))
    mongo_worker_thread.daemon = True
    mongo_worker_thread.start()

    # Set up signal handler before we go into the real work
    SIGINT_ORIG = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal_handler)

    # Start up Reader Thread
    reader_thread = Thread(target=reader_worker, args=(work_queue, collection, options), name='Reader')
    reader_thread.daemon = True
    reader_thread.start()

    while True:
        reader_thread.join(.1)
        if not reader_thread.isAlive():
            break

    time.sleep(.1)

    while not work_queue.empty():
        time.sleep(.01)

    work_queue.join()
    insert_queue.put("finished")
    mongo_worker_thread.join()

    # Update the stats
    meta.update({'metadata': options.identifier}, {'$set': {
        'total': STATS['total'],
        'new': STATS['new'],
        'updated': STATS['updated'],
        'unchanged': STATS['unchanged'],
        'duplicates': STATS['duplicates'],
        'changed_stats': CHANGEDCT
    }
    });

    if options.stats:
        print "Stats: "
        print "Total Entries:\t\t %d" % STATS['total']
        print "New Entries:\t\t %d" % STATS['new']
        print "Updated Entries:\t %d" % STATS['updated']
        print "Duplicate Entries\t %d" % STATS['duplicates']
        print "Unchanged Entries:\t %d" % STATS['unchanged']


if __name__ == "__main__":
    main()
