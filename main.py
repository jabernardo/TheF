#!/usr/bin/env python

from pathlib import Path
import os
import configparser
import argparse
import sys
import re
from difflib import SequenceMatcher

# function q()
# {
#     source="python /home/jabernardo/Workspace/q/main.py"

#     if [[ ( $# -eq 0 ) ]]; then
#         history -w
#         $($source $1)
#     elif [[ ( $1 == -* ) || ( $# -gt 1 ) ]]; then
#         $source $@
#     else
#         cd $($source $1)
#     fi
# }

class TheF:
    homedir = "/"

    config = None

    config_file = ".q"
    config_path = ""

    paths = None

    application_path = ""

    def __init__(self):
        self.homedir = str(Path.home())
        
        self.config = configparser.ConfigParser()
        self.config_path = f"{self.homedir}/{self.config_file}"

        if Path(self.config_path).exists():
            self.config.read(self.config_path)
        
        if not "paths" in self.config:
            self.config["paths"] = {}

            self.__save_config()

        self.paths = self.config["paths"]

        self.application_path = str(Path(__file__).parent)

    def __save_config(self):
        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)

    def __get_match(self, needle, haystack):
        highest_word = ""
        highest_ratio = 0

        for cmd in haystack:
            ratio = SequenceMatcher(None, needle, cmd).ratio()

            if ratio > highest_ratio:
                highest_word = cmd
                highest_ratio = ratio
        
            params = needle.strip().split(" ")[ len(highest_word.split(" ")): ]

            if highest_ratio > 0.8 and highest_ratio != 1.0:
                return f"{ highest_word.strip() } { ' '.join(params) }"

        return None

    ##
    ## Paths
    ##

    def add_path(self, alias, path, force=False):
        if not alias in self.paths or force:
            self.paths[alias] = path
            self.__save_config()

    def get_path(self, alias):
        if alias in self.paths:
            return self.paths[alias]
        
        return os.getcwd()

    def remove_path(self, alias):
        if alias in self.paths:
            del self.paths[alias]
            self.__save_config()

    ###############################################################3

    # F*ck!

    def get_last_command(self, custom_history = "~/.bash_history"):
        history = os.path.expanduser(custom_history)

        try:
            with open(history, "r") as bash_history:
                if "fish" in history:
                    cmds = re.findall(r"cmd: (.*)", bash_history.read())
                    return cmds[-2]
                else:
                    return bash_history.readlines()[-2]
        except:
            pass

        return ""

    def get_history(self, custom_history = "~/.bash_history"):
        history = os.path.expanduser(custom_history)

        try:
            with open(history, "r") as bash_history:
                    if "fish" in history:
                        return re.findall(r"cmd: (.*)", bash_history.read())
                    else:
                        return bash_history.readlines()
        except:
            pass

        return []

    def get_prediction(self, command, custom_history = "~/.bash_history"):
        commands = []
        
        with open(f"{self.application_path}/commands.txt", "r") as file:
            commands = file.readlines()
        
        ## First pass
        result = self.__get_match(command, commands)

        if result:
            return result
 
        ## Second result
        result = self.__get_match(command, self.get_history(custom_history))

        return "" if result is None else result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("alias", nargs="?", default="", help="Path alias")
    parser.add_argument("-a", "--add", action="store_true", default=False, help="Add path")
    parser.add_argument("-r", "--remove", action="store_true", default=False, help="Remove path")
    parser.add_argument("-f", "--force", action="store_true", default=False, help="Let the force be with you!")
    parser.add_argument("-z", "--history", default="~/.bash_history", help="History file")
    args = parser.parse_args()

    q = TheF()

    name = args.alias
    cwd = os.getcwd()

    if len(name) == 0:
        name = os.path.basename(cwd)

    if args.add:
        q.add_path(name, cwd, args.force)
    elif args.remove:
        q.remove_path(name)
    else:
        if args.alias:
            print(q.get_path(args.alias))
        else:
            print(q.get_prediction(q.get_last_command(args.history), args.history))

if __name__ == "__main__":
    main()
