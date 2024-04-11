##
## Paths
##
# httpd_conf_path = "/var/lib/docker/volumes/litespeed_ls-conf/_data/httpd_config.conf"
httpd_conf_path = "./test/httpd_config.conf"
# services_www_path = "/home/ubuntu/services"
services_dir = "./test/services"
# vhost_conf_dir = "/var/lib/docker/volumes/litespeed_ls-conf/_data/vhosts"
vhost_conf_dir = "./test/vhosts"
# vhost_dir = "/var/lib/docker/volumes/litespeed_ls-vhost/_data"
vhost_dir = "./test/vhost_dir"

##
## Logging
##
import logging
loglevel = logging.ERROR

lsadm_uid = 999
lsadm_gid = 1000

lsws_bin_dir = "/usr/local/lsws/bin"
