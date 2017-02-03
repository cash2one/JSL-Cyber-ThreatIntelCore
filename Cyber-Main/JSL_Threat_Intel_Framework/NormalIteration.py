from phase1_datagg.agg_functions import *
from phase2_rdns.rDNS_functions import *
from phase3_geowhois.GIOWHOIS import *
from memory_profiler import profile


def do_iteration(offender_class):
    print "starting %s iteration" % offender_class
    print "Phase 1 starting "
    pulled_items = pull_all(offender_class)  # Phase 1

    report = phase1report
    ts = time.time()
    startTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    print (startTime)
    print type(report)
    report += ('This iteration started at ')
    report += startTime

    for item in pulled_items[2]:
        report += '\n' + str(item) + '\n '
    print report

    send_mail('fzdahmane@gmail.com', 'data aggregation phase report', report)
    # send_mail('abdou@johnsnowlabs.com', ' jai ajoute les espaces ', report)

    print "Phase 2 starting "
    #    resolve_items(pulled_items)  # Phase 2


    print "Phase 3 starting "
    #    main_geowhois('items', offender_class + '_bl')  # Phase 3

    print "Iteration Done  "


if __name__ == '__main__':
    do_iteration('malware')
