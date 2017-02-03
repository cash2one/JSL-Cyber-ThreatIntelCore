from phase1_datagg.ScriptRunner import *
from phase2_rdns.rDNS_functions import *
from phase3_geowhois.GIOWHOIS import *
import time
import datetime


def single_runner(iteration, offenderClass, inputClass):
    filename = '*'
    files = [filename + '.whois', filename + '.ips', filename + '.whois.tmp', filename + '.domains',
             filename + '.whois.shrunk',
             filename + '.whois.shrunk.spaceless', filename + '.whois.shrunk.clean', 'output*', '*list']

    for fn in files:
        try:
            os.system("rm %s" % fn)
        except:
            pass
    RunScripts(LoadScripts(os.path.abspath("phase1_datagg/%s/%s" % (offenderClass, inputClass))))

    resolve_domains(inputClass)

    if inputClass in "badips":
        filename = "iplist"

    elif inputClass in "baddomains":
        filename = "dnslist"
    ts = time.time()

    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    main_geowhois(filename, offenderClass + '_bl', iteration, st)

    if inputClass in "badips":

        os.system("mv iplist.gio %s_%s.gio" % (offenderClass, inputClass))

    elif inputClass in "baddomains":
        os.system("mv dnslist.gio %s_%s.gio" % (offenderClass, inputClass))


def auto_runner(iteration):
    all = [
        ['domains', ['baddomains', 'badips']],
        ['malware', ['baddomains', 'badips']],
        ['phishing', ['baddomains', 'badips']],
        ['spam', ['baddomains', 'badips']],
        ['ssl', ['badips']],
        ['tor', ['badips']]

    ]

    for entry in all:

        for inputClass in entry[1]:
            single_runner(iteration, entry[0], inputClass)


def main():
    iteration = input('Enter the iteration N: ')

    phase = input(
        "*** \nType 0 for a full iteration \nType 1 for running only phase 1 \n Type 2 for running up to phase 2 :")

    offenderClass = str(raw_input('Enter the offenderclass :  [tor, ssl, malware...]  '))

    inputClass = str(raw_input('enter the input type : [badips, baddomains]'))

    RunScripts(LoadScripts(os.path.abspath("phase1_datagg/%s/%s" % (offenderClass, inputClass))))
    if inputClass in "badips":
        filename = "iplist"


    elif inputClass in "baddomains":
        filename = "dnslist"

    if phase == 1:
        os.system("mv ../output* phase1_%s.%s" % (offenderClass, inputClass))

        return

    resolve_domains(inputClass)
    if phase == 2:
        os.system("rm output")
        os.system("mv %s phase2_%s.%s" % (filename, offenderClass, inputClass))

        return

    ts = time.time()

    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    main_geowhois(filename, offenderClass + '_bl', iteration, st)

    if inputClass in "badips":

        os.system("mv iplist.gio %s_%s.gio" % (offenderClass, inputClass))

    elif inputClass in "baddomains":
        os.system("mv dnslist.gio %s_%s.gio" % (offenderClass, inputClass))


if __name__ == '__main__':
    main()
    # auto_runner(20)
