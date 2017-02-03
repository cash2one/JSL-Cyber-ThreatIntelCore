import os
import glob

Folder = '.'

Files = glob.glob(os.path.join(Folder, "*.csv"))

for fichier in Files:
    content = open(fichier, 'r')
    dump = content.read()

    dump = dump.replace('\r\n', '\n')
    new_file = open(fichier + '_', 'w')
    new_file.write(dump)
