from ftplib import FTP

final = ""


class ftp_parser(object):
    def __init__(self):
        self.dump = ""
        self.lines = []

    def pull(self, addition):
        self.dump += addition

    def parse(self):
        [self.lines.append(x.split('|')) for x in self.dump.split('\n')]


parser = ftp_parser()
ftp = FTP('ftp.arin.net')  # connect to host, default port
ftp.login()  # user anonymous, passwd anonymous@

ftp.cwd('pub/stats/afrinic')  # change into "debian" directory

output = []

ftp.retrbinary('RETR delegated-afrinic-latest', parser.pull)

parser.parse()

print parser.lines
