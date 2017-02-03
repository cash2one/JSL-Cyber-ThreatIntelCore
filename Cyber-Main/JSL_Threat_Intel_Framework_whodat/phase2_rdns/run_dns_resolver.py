import os


def run_resolver(toresolve):
    os.system('dns_resolver -domain/-ip ../%s -output ../%s_resolved', toresolve, toresolve)
