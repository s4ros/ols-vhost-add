import os
from config import *
from map_httpd import HttpdConfig
from icecream import ic
import logging
import config

ic.configureOutput(includeContext=True)


def main():
    # if os.getuid() != 0:
    #     print("You need to run this script as root.")
    #     exit(1)

    vhost = input("Enter the vhost name: ")
    domains = input("Enter the domains separated by comma: ")

    logging.basicConfig(level=config.loglevel)
    running_config = HttpdConfig()

    running_config.add_vhost(vhost, domains.strip().split(","))
    print(running_config.write_config())

######################################################
main()