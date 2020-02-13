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

class Quickie:
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

    def get_last_command(self, custom_history = None):
        history = os.path.expanduser(custom_history)

        with open(history, "r") as bash_history:
            if "fish" in history:
                cmds = re.findall(r"cmd: (.*)", bash_history.read())
                return cmds[-2]
            else:
                return bash_history.readlines()[-2]

        return ""

        # os.system('history > tmp')
        # print(open('tmp', 'r').read())

    def get_prediction(self, command):
        commands = []
        highest_word = ""
        highest_ratio = 0
        
        with open(f"{self.application_path}/commands.txt", "r") as file:
            commands = file.readlines()
        
        for cmd in commands:
            ratio = SequenceMatcher(None, command, cmd).ratio()

            if ratio > highest_ratio:
                highest_word = cmd
                highest_ratio = ratio

        
        params = command.strip().split(" ")[ len(highest_word.split(" ")): ]

        return f"{ highest_word.strip() } { ' '.join(params) }" if highest_ratio > 0.5 else ""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("alias", nargs="?", default="", help="Path alias")
    parser.add_argument("-a", "--add", action="store_true", default=False, help="Add path")
    parser.add_argument("-r", "--remove", action="store_true", default=False, help="Remove path")
    parser.add_argument("-f", "--force", action="store_true", default=False, help="Let the force be with you!")
    parser.add_argument("-z", "--history", default="~/.bash_history", help="History file")
    args = parser.parse_args()

    q = Quickie()

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
            print(q.get_prediction(q.get_last_command(args.history)))

if __name__ == "__main__":
    main()
