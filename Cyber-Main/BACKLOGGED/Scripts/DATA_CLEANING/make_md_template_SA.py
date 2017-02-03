# -*- coding: utf-8 -*-

import re
import textwrap

#This script has the ability to copy text, and generate a python script from that.

with open("DNS_Blacklist.md") as f_old, open("generate_reference_template_SA.py", "w") as f_new:
    f_new.write('# -*- coding: utf-8 -*-\n')
    f_new.write('\n\n')
    f_new.write('import re\n\n')
    f_new.write('#This script was built automatically, using the script: "make_md_template_SA.py"\n\n')
    f_new.write('with open("reference_file.md", "w") as f_new:\n')
    for i, line in enumerate(f_old):
        line = line.replace("'", "\\'")
        line = line + '\\n'
        line.replace("'", "\'")
        line = '\t' + "f_new.write('" + str(line).replace('\n', '') + "')\n"
        #test for lines to edit here
        f_new.write(line)
