import sys
from os import listdir
from os.path import isfile, join
import os

DNS_RESOLUTION = "./dns_resolver -%s %s/%s -output %s/%s.dns"
CLEAN_DNS_OUTPUT_1 = "grep ^[0-9] %s/%s.dns > tmp "
CLEAN_DNS_OUTPUT_2 = "mv tmp %s/%s.dns"


def main():

    if len(sys.argv) < 3:
        print """USAGE :
                            python Iteration11.py ip|domain inputDir
                """
        return

    category = sys.argv[1]
    directory = str(sys.argv[2])
    onlyfiles = [f for f in listdir(directory) if isfile(join(directory, f))]
    if __file__ in onlyfiles:
        onlyfiles.remove(__file__)

    for fn in onlyfiles:
        os.system(DNS_RESOLUTION % (category, directory, fn, directory, fn))

    if category in 'domain':
        for fn in onlyfiles:
            os.system(CLEAN_DNS_OUTPUT_1 % (directory, fn))
            os.system(CLEAN_DNS_OUTPUT_2 % (directory, fn))


if __name__ == '__main__':
    main()
