import os
from config import *
import Httpd
from icecream import ic
import logging
import config

ic.configureOutput(includeContext=True)
ic.disable()

def check_write_permissions():
    LOCATIONS = [
        config.httpd_conf_path,
        # config.services_dir,
        config.vhost_dir,
        config.vhost_conf_dir
    ]
    for location in LOCATIONS:
        if not os.access(location, os.W_OK):
            ic(location)
            logging.error(f"Permission denied to write to {location}")
            return False
    return True

def main():
    if not check_write_permissions():
        logging.error("Please run the script as root.")
        return
    vhost = input("Enter the vhost name: ")
    domains = input("Enter the domains separated by comma: ")

    logging.basicConfig(level=config.loglevel)

    ols = Httpd.Config()
    ols.add_vhost(vhost, domains)
    ols.save_config()
    ols.restart()
    print("Vhost added successfully.")


######################################################
main()
