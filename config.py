##
## Paths
##
# httpd_conf_path = "/var/lib/docker/volumes/litespeed_ls-conf/_data/httpd_config.conf"
httpd_conf_path = "./test/httpd_config.conf"
# services_www_path = "/home/ubuntu/services"
services_dir = "./text/services"
# vhost_dir = "/var/lib/docker/volumes/litespeed_ls-conf/_data/vhosts"
vhost_dir = "./test/vhosts"

##
## Logging
##
import logging
loglevel = logging.ERROR