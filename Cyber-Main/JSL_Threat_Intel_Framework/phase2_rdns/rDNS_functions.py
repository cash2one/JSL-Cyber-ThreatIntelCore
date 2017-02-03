import os

def resolve_badips():
    DNS_RESOLUTION = "phase2_rdns/dns_resolver -ip output -output iplist"

    #os.system('head output -n 1000 > tmp')

    #os.system('mv tmp output')
    os.system(DNS_RESOLUTION)


def resolve_baddomains():
    DNS_RESOLUTION = "phase2_rdns/dns_resolver -domain output -output dnslist"
    CLEAN_DNS_OUTPUT_1 = "grep ^[0-9] dnslist > tmp "
    CLEAN_DNS_OUTPUT_2 = "mv tmp dnslist"

    #os.system('head output -n 1000 > tmp')

    #os.system('mv tmp output')
    os.system(DNS_RESOLUTION)

    os.system(CLEAN_DNS_OUTPUT_1)
    os.system(CLEAN_DNS_OUTPUT_2)

def resolve_domains(inputClass):
    # os.system("pwd")
    # os.chdir("..")
    # os.system("pwd")

    print "resolving hosts"
    os.system("mv ../output_* output")

    if inputClass in "badips":

        resolve_badips()

    elif inputClass in 'baddomains':

        resolve_baddomains()




def resolve_items(items):
    print "Resolving bad ips"
    resolve_badips(items[0])
    print "Resolving bad domains"
    resolve_baddomains(items[1])
    print "merging all output"
    filenames = ['items', 'dnslist']
    with open('items', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

    os.system('rm iplist')
    os.system('rm dnslist')
