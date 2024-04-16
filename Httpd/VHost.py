import os
import config
from icecream import ic

class VHost:
    def __init__(self, vhost_name, domains) -> None:
        self.vhost_name = vhost_name
        self.domains = domains

    def generate_map(self):
        return {
            "vhost": self.vhost_name,
            "domains": [x.strip() for x in self.domains],
            }

    def generate_vhost(self):
        return {self.vhost_name: {
            "vhRoot": [f"$SERVER_ROOT/conf/vhosts/{self.vhost_name}"],
            "configFile": ['$SERVER_ROOT/conf/vhosts/$VH_NAME/vhconf.conf'],
            "allowSymbolLink": [1],
            "enableScript": [1],
            "restrained": [1],
        }}

    def get_config(self):
        with open(f"{config.vhost_conf_dir}/{self.vhost_name}/vhconf.conf", "r") as f:
            return f.read()

    def __prepare_dirs(self):
        DIRS = [
            os.path.join(config.vhost_dir, self.vhost_name),
            os.path.join(config.vhost_conf_dir, self.vhost_name),
            os.path.join(config.services_dir, self.vhost_name),
            os.path.join(config.vhost_dir, self.vhost_name, "logs"),
            os.path.join(config.vhost_dir, self.vhost_name, "conf"),
            os.path.join(config.vhost_dir, self.vhost_name, "html"),
        ]
        for dir in DIRS:
            if not os.path.exists(dir):
                os.makedirs(dir)

    def save_config(self):
        self.__prepare_dirs()
        CONFIG = f"docRoot\t\t/var/www/services/{self.vhost_name}\n"
        CONFIG += "scripthandler  {\n"
        CONFIG += "    add\t\tlsapi:lsphp82 php\n"
        CONFIG += "}\n"
        CONFIG += "context / {\n"
        CONFIG += "    allowBrowse\t\t1\n"
        CONFIG += "    rewrite  {\n"
        CONFIG += "        enable\t\t1\n"
        CONFIG += "    }\n"
        CONFIG += "    addDefaultCharset\t\toff\n"
        CONFIG += "    phpIniOverride  {\n"
        CONFIG += "    }\n"
        CONFIG += "}\n"
        CONFIG += "rewrite  {\n"
        CONFIG += "    enable\t\t1\n"
        CONFIG += "    autoLoadHtaccess\t\t1\n"
        CONFIG += "}\n"
        with open(f"{config.vhost_conf_dir}/{self.vhost_name}/vhconf.conf", "w") as f:
            f.write(CONFIG)