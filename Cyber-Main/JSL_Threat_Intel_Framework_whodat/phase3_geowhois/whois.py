import datetime
import os
import sys


def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]


def main():
    if len(sys.argv) < 4:
        print " USAGE : python whois.py inputfile outputfile batchsize"
        return
    else:
        inputfn = sys.argv[1]
        outputfn = sys.argv[2]
        batchSize = int(sys.argv[3])
        batchSize = int(sys.argv[3])

    command = "netcat whois.cymru.com 43 < %s | tail -n +2 >> %s"
    command1 = "sed -i 's/,/./g' %s"
    command2 = "sed -i 's/|/,/g' %s"
    command3 = "sort -u -t',' -k2,2 %s >> %s"
    inputData = open(inputfn, 'r')
    ips = inputData.readlines()
    print len(ips)

    Chunks = chunks(ips, batchSize)
    print len(Chunks)
    i = 0
    for chnk in Chunks:
        print len(chnk)

        output = open("output" + str(i), 'w')

        currentTime = datetime.datetime.strftime(datetime.datetime.now(), ' %Y-%m-%d %H:%M:%S')
        output.write("begin\nverbose\n")
        for ip in chnk:
            output.write(ip.strip() + currentTime + '\n')
        output.write('end\n')

        output.close()
        print (command % ("output" + str(i), outputfn + ".tmp"))
        os.system(command % ("output" + str(i), outputfn + ".tmp"))

        print "done"

        i += 1
    os.system(command1 % (outputfn + ".tmp"))
    os.system(command2 % (outputfn + ".tmp"))
    os.system(command3 % (outputfn + ".tmp", outputfn))


main()
