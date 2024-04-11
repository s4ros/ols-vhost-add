import os
from config import *
import Httpd
from icecream import ic
import logging
import config

ic.configureOutput(includeContext=True)
ic.disable()


def main():
    # if os.getuid() != 0:
    #     print("You need to run this script as root.")
    #     exit(1)

    vhost = input("Enter the vhost name: ")
    domains = input("Enter the domains separated by comma: ")

    logging.basicConfig(level=config.loglevel)

    ols = Httpd.Config()
    ols.add_vhost(vhost, domains.strip().split(","))
    print(ols.generate())
    ols.save_config(vhost)


######################################################
main()
