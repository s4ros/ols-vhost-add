from .Parser import Parser
from .VHost import VHost
import os
import config

class Config:
    def __init__(self):
        self.config = Parser(config.httpd_conf_path)

    def generate(self):
        local_config = self.config.httpd_config.copy()
        specials = {
            "accessDenyDir": local_config.pop("accessDenyDir"),
            "extprocessors": local_config.pop("extprocessors"),
            "vhosts": local_config.pop("vhosts"),
            "listener HTTP": local_config.pop("listener HTTP"),
            "global": local_config.pop("global"),
        }
        CONFIG = "# CONFIG GENERATED BY VHOST-SETUP.PY\n"
        CONFIG += "# DO NOT EDIT THIS FILE MANUALLY\n\n"
        # global config
        for key, value in specials["global"].items():
            CONFIG += f"{key:<{25}} {' '.join(value)}\n"
        # accessdenydir config
        CONFIG += "\n"
        CONFIG += "accessDenyDir {\n"
        for key, value in specials["accessDenyDir"].items():
            for dir in value:
                CONFIG += f"    dir        {dir[0]}\n"
        CONFIG += "}\n"
        # rest of the config
        for block, items in local_config.items():
            CONFIG += f"\n{block} {{\n"
            for key, value in items.items():
                CONFIG += f"    {key:<{25}} {' '.join(value)}\n"
            CONFIG += "}\n"
        # extprocessor config
        for extprocessor in specials["extprocessors"]:
            for key, value in extprocessor.items():
                CONFIG += f"\nextprocessor {str(key)} {{\n"
                for k, v in value.items():
                    CONFIG += f"    {k:<{20}} {v[0]}\n"
                CONFIG += "}\n"
        # virtualhost config
        for vhost in specials["vhosts"]:
            for key, value in vhost.items():
                CONFIG += f"\nvirtualHost {key} {{\n"
                for k, v in value.items():
                    CONFIG += f"    {k:<{20}} {v[0]}\n"
                CONFIG += "}\n"
        # listener config
        CONFIG += "\nlistener HTTP {\n"
        for key, value in specials["listener HTTP"].items():
            if key == "maps":
                for item in value:
                    CONFIG += f"    map {item['vhost']:<{25}} {', '.join(item['domains'])}\n"
            else:
                CONFIG += f"    {key:<{20}} {value[0]}\n"
        CONFIG += "}\n"
        return CONFIG

    def add_vhost(self, vhost_name, domains):
        vhost = VHost(vhost_name, domains)
        self.config.httpd_config["listener HTTP"]["maps"].append(vhost.generate_map())
        self.config.httpd_config["vhosts"].append(vhost.generate_vhost())

    def __str__(self) -> str:
        return str(self.config)

    def __make_dirs(self, vhost_name: str):
        pass

    def save_config(self, vhost_name: str):
        with open(self.config.path, "w") as f:
            f.write(self.generate())
        self.__make_dirs(vhost_name)
