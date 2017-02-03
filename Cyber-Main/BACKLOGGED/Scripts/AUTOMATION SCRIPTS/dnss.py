import dns.resolver
import csv
import multiprocessing.pool
import socket
socket.setdefaulttimeout(1)



def rez(ip):
    try:
        resp = socket.gethostbyaddr(ip.replace("\n",''))
        return [resp[2],resp[0]]
    except:
        return [ip.replace("\n",''), '']


if __name__ == '__main__':

    with open('badips.txt') as in_file:
        lines = in_file.readlines()

    p = multiprocessing.pool.Pool(2)
    output_data = p.map(rez, lines)


