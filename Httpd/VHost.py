import os
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

    def prepare_dir(self):
        pass