# Module responsible for mapping the HTTPD configuration file.
from icecream import ic
from logging import getLogger

class Parser:
    def __init__(self, src_path):
        self.path = src_path
        self.raw_config = self.load_config()
        self.httpd_config = {
            "vhosts": [],
            "extprocessors": [],
            "global": {},
        }
        self.BLOCK = False
        self.VIRTUAL_HOST = False
        self.EXTPROCESSOR = False
        self.LISTENER = True
        self.current_block = ""
        self.current_vhost_name = ""
        self.current_extprocessor_name = ""
        self.logger = getLogger(__name__)
        self.__map_config()
        ic(self.httpd_config)

    def load_config(self):
        with open(self.path, "r") as f:
            return f.read()

    def __str__(self) -> str:
        return str(self.httpd_config)

    def __map_config(self):
        for line in self.raw_config.strip().split("\n"):
            self.logger.debug(f"LINE:>> {line}")
            # ic("#LINE:>> ", line)
            if len(line) == 0:              # empty line
                continue
            if line[0] == "#":              # comment line
                continue
            if line[0] == "}":              # end of block
                self.logger.debug(f"###END OF BLOCK:>> {self.current_block}")
                self.BLOCK = False
                self.VIRTUAL_HOST = False
                self.EXTPROCESSOR = False
                self.LISTENER = False
                self.current_block = ""
                self.current_vhost_name = ""
                continue
            if "{" not in line:             # normal line, not a block
                try:
                    key = line.split()[0]
                except IndexError:
                    continue
                try:
                    value = line.replace(",", "").split()[1:]
                except IndexError:
                    value = ""
                #
                # virtualhost {} block
                #
                if self.BLOCK and self.VIRTUAL_HOST:
                    self.httpd_config["vhosts"][-1][self.current_vhost_name][key] = value
                    self.logger.debug(f'###VHOST:>> {self.httpd_config["vhosts"][-1]}')
                #
                # extprocessor {} block
                #
                elif self.BLOCK and self.EXTPROCESSOR:
                    self.httpd_config["extprocessors"][-1][self.current_extprocessor_name][key] = value
                    self.logger.debug(f'###EXTPROCESSOR:>> {self.httpd_config["extprocessors"][-1]}')
                #
                # listener HTTP {} block
                #
                elif self.BLOCK and self.LISTENER:
                    if key == "map":
                        vhost = value[0]
                        value.pop(0)
                        domains = value
                        self.httpd_config[self.current_block]["maps"].append({"vhost":vhost, "domains": domains})
                        self.logger.debug(f'###LISTENER:>> {self.httpd_config[self.current_block]["maps"]}')
                    else:
                        self.httpd_config[self.current_block][key] = value
                        self.logger.debug(f'###LISTENER:>> {self.httpd_config[self.current_block][key]}')
                    # ic(self.httpd_config[self.current_block])

                #
                # AccessDenyDir {} block
                #
                elif self.BLOCK and "accessdenydir" in self.current_block.lower():
                    if key == "dir":
                        self.httpd_config[self.current_block]["dirs"].append(value)
                        self.logger.debug(f'###ACCESSDENYDIR:>> {self.httpd_config[self.current_block]["dirs"]}')

                #
                # other blocks
                #
                elif self.BLOCK and not self.VIRTUAL_HOST and not self.EXTPROCESSOR:
                    self.httpd_config[self.current_block][key] = value
                    self.logger.debug(f'###BLOCK:>> {self.httpd_config[self.current_block][key]}')
                #
                # global config
                #
                else:
                    self.httpd_config["global"][key] = value
                    self.logger.debug(f'###HTTPD:>> {self.httpd_config["global"]}')
            if "{" in line:                 # start of block
                self.BLOCK = True
                self.current_block = line[:-1].rstrip()
                self.logger.debug(f"###BLOCK:>> {self.current_block}")
                if "virtualhost" in self.current_block.lower():
                    self.current_vhost_name = line.split()[1]
                    self.VIRTUAL_HOST = True
                    self.logger.debug(f"###VHOST:>> {self.current_vhost_name}")
                    self.httpd_config["vhosts"].append({self.current_vhost_name: {}})
                elif "extprocessor" in self.current_block.lower():
                    self.current_extprocessor_name = line.split()[1]
                    self.EXTPROCESSOR = True
                    self.logger.debug(f"###EXTPROCESSOR:>> {self.current_extprocessor_name}")
                    self.httpd_config["extprocessors"].append({self.current_extprocessor_name: {}})
                elif "listener" in self.current_block.lower():
                    self.httpd_config[self.current_block] = {"maps": []}
                    self.LISTENER = True
                elif "accessdenydir" in self.current_block.lower():
                    self.httpd_config[self.current_block] = {"dirs": []}
                else:
                    self.httpd_config[self.current_block] = {}
                # print("###BLOCK:>> ", self.current_block)
