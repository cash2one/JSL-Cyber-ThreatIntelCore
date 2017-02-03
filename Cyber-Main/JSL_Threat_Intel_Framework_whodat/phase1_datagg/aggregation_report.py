import datetime
import time


class AggregationReport(object):
    def __init__(self):
        ts = time.time()
        self.startTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.phases = {}
        self.pulls = []

    def add_phase(self, phaseName):
        ts = time.time()
        self.phases[phaseName] = []
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.phases[phaseName].append(st)

    def end_phase(self, phaseName):
        ts = time.time()
        self.phases[phaseName] = []
        self.phases[phaseName].append(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

    def add_pull(self, item, url, number):
        self.pulls.append("%s %s where pulled from %s" % (number, item, url))
