#!/usr/bin/env python

from pathlib import Path
import os
import configparser
import argparse
import sys
import re
from difflib import SequenceMatcher

##
# The F!
# 
# Shorthand for terminal
#
######
# Installation
#
#########
### Bash
#
# function q()
# {
#     source="python /{installation path}/main.py"
#
#     if [[ ( $# -eq 0 ) ]]; then
#         history -w
#         $($source $1)
#     elif [[ ( $1 == -* ) || ( $# -gt 1 ) ]]; then
#         $source $@
#     else
#         cd $($source $1)
#     fi
# }
#########
### Fish
# function f
#         set -l source "python /{installation path}/main.py"
#
#         if test (count $argv) -eq 0
#                 history save
#                 eval (eval $source $argv --history "~/.local/share/fish/fish_history")
#         else
#                 cd (eval $source $argv)
#         end
# end
#
#

class TheF:
    """TheF!
    An application inspired by Fuck and Jump
    """

    # User home directory
    homedir = "/"

    # Loaded Configurations
    config = None

    # Configuration filename
    config_file = ".q"
    # Configuration full path
    config_path = ""

    # Loaded paths from configuration
    paths = None

    # Application Full Path
    application_path = ""

    def __init__(self):
        """TheF"""

        # Apply full home directory
        self.homedir = str(Path.home())
        
        self.config = configparser.ConfigParser()
        self.config_path = f"{self.homedir}/{self.config_file}"

        if Path(self.config_path).exists():
            self.config.read(self.config_path)
        
        if not "paths" in self.config:
            # Make sure path section exists
            self.config["paths"] = {}

            self.__save_config()

        self.paths = self.config["paths"]

        self.application_path = str(Path(__file__).parent)

    def __save_config(self):
        """Save configurations file"""
        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)

    def __get_match(self, needle, haystack):
        """Get closest match for command. Would append parameters or arguments for closest match\n

        \nArguments:\n
        `needle` (str) -- Needle or the mistaken command\n
        `haystack` (str) -- Haystack\n

        \nReturns:\n
        `str|None` Match
        """
        highest_word = ""
        highest_ratio = 0

        for hay in haystack:
            ratio = SequenceMatcher(None, needle, hay).ratio()

            if ratio > highest_ratio:
                highest_word = hay
                highest_ratio = ratio
        
            params = needle.strip().split(" ")[ len(highest_word.split(" ")): ]

            if highest_ratio > 0.8 and highest_ratio != 1.0:
                return f"{ highest_word.strip() } { ' '.join(params) }"

        return None

    ##
    ## Jump Path!
    ###############################################################

    def add_path(self, alias, path, force=False):
        """Add path to Jump list\n

        \nArguments:\n
        `alias` (str) -- Alias for path\n
        `path` (str) -- Full path\n

        \nReturns:\n
        `None`
        """
        if not alias in self.paths or force:
            self.paths[alias] = path
            self.__save_config()

    def get_path(self, alias):
        """Get path\n
        \nArguments:\n
        `alias` (str) -- Path alias\n

        \nReturns:\n
        `str` Path from alias else current working directory
        """
        if alias in self.paths:
            return self.paths[alias]
        
        return os.getcwd()

    def remove_path(self, alias):
        """Remove path\n
        \nArguments:\n
        `alias` (str) -- Path alias to be removed\n
        \nReturns:\n
        `None`
        """
        if alias in self.paths:
            del self.paths[alias]
            self.__save_config()

    ##
    ## What the F!
    ###############################################################

    def get_last_command(self, custom_history = "~/.bash_history"):
        """Get last command from history\n

        \nArguments:\n
        `custom_history` (str) -- History file. Default history file is for bash\n

        \nReturns:\n
        `str`\n

        \nNotes:\n
        - Make sure to update history file before using this command. See installation section for
        more information\n

        \nSupported Shells:\n
        - Bash
        - Fish
        """
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
        """Get all history\n

        \nArguments:\n
        `custom_history` (str) -- History file. Default history file is for bash\n

        \nReturns:\n
        `list`\n

        \nNotes:\n
        - Make sure to update history file before using this command. See installation section for
        more information\n

        \nSupported Shells:\n
        - Bash
        - Fish
        """
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
        """Get prediction from command\n

        \nArguments:\n
        `command` (str) Wrong command\n
        `custom_history` (str) -- History file. Default history file is for bash

        \nReturns:\n
        `str`
        """
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
        # Add path to paths list
        q.add_path(name, cwd, args.force)
    elif args.remove:
        # Remove path from list
        q.remove_path(name)
    else:
        if args.alias:
            # Directory Jump!
            print(q.get_path(args.alias))
        else:
            # The F!
            print(q.get_prediction(q.get_last_command(args.history), args.history))

if __name__ == "__main__":
    main()
