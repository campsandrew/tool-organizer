import os
import sys
import datetime

# Local File Imports
from map import Map
from util import load_json
from util import dump_json

# Constant Definitions
HOME = os.path.expanduser("~")
TORG_CONF_PATH = os.path.join(HOME, ".torg")
TORG_DOC_FILE = os.path.join(TORG_CONF_PATH, "torg.doc")
TORG_HIST_FILE = os.path.join(TORG_CONF_PATH, "torg.hist")
TORG_CONF_FILE = os.path.join(TORG_CONF_PATH, "torg.conf")

class Configuration:

    # Class Constant Definitions
    SAVED_TAB = "Saved"
    HISTORY_TAB = "History"
    DOC_TAB = "Documentation"
    DEFAULT_TABS = [SAVED_TAB, HISTORY_TAB, DOC_TAB]

    def __init__(self):
        gen_funcs = [self._gen_doc_file, self._gen_hist_file, self._gen_conf_file]
        cfiles = [TORG_DOC_FILE, TORG_HIST_FILE, TORG_CONF_FILE]

        # Check for main config directory structure
        if not os.path.isdir(TORG_CONF_PATH):
            os.mkdir(TORG_CONF_PATH)
            for i in range(len(cfiles)):
                gen_funcs[i](cfiles[i])

        # Check if all config files exist
        for i in range(len(cfiles)):
            if not os.path.isfile(cfiles[i]):
                gen_funcs[i](cfiles[i])

        # Read all config files
        conf = load_json(TORG_CONF_FILE)
        hist = load_json(TORG_HIST_FILE)
        doc = load_json(TORG_DOC_FILE)
        self._conf = Map.recursive_map(Map(conf))
        self._hist = Map.recursive_map(Map(hist))
        self._doc = Map.recursive_map(Map(doc))

        return None

    def get_tab_names(self):
        tabs = []

        # Get all user defined tab names
        for tab in self._conf.user_defined_tabs:
            tabs.append(tab.tab_name)

        return tabs + self.DEFAULT_TABS

    def get_terminal_command(self):
        t_cmd = None

        if sys.platform == "linux":
            t_cmd = self._conf.os.linux.terminal_command
        elif sys.platform == "darwin":
            t_cmd = self._conf.os.darwin.terminal_command
        else: pass

        return t_cmd

    def get_filepath(self, key):
        filepath = ""

        # Return filepath for particular configuration file
        if key == self.DOC_TAB: filepath = self._doc.filepath
        elif key == self.HISTORY_TAB: filepath = self._hist.filepath
        elif key == self.SAVED_TAB: filepath = self._conf.filepath
        else: filepath = self._conf.filepath

        return filepath

    def edit_doc_file(self, documentation):
        self._doc.documentation = documentation
        dump_json(self._doc.filepath, self._doc)

        return None

    def read_doc_file(self):
        return self._doc.documentation

    def get_history_dates(self):
        return [hist.date for hist in self._hist.history]

    def add_history(self, command):
        date = datetime.date.today().strftime("%Y/%m/%d")
        time = datetime.datetime.now().strftime("%H:%M")
        command_tup = (command, time)

        # Determining if date exists in history or not
        if self._hist.history and date == self._hist.history[0].date:
            self._hist.history[0].commands.insert(0, command_tup)
        else:
            new_date = Map({
                "date": date,
                "commands": [command_tup]
            })
            self._hist.history.insert(0, new_date)

        # Save history information to history file
        dump_json(self._hist.filepath, self._hist)
        
        return None

    def add_user_tab(self, tab_name):
        self._conf.user_defined_tabs.append({
            "tab_name": tab_name,
            "tools": []
        })

        # Save tab information to config file
        dump_json(self._conf.filepath, self._conf)

        return None

    def delete_user_tab(self, tab_key):

        # Loop to find tab_key that matches and delete
        for i, tab in enumerate(self._conf.user_defined_tabs):
            if tab.tab_name == tab_key:
                del self._conf.user_defined_tabs[i]
                break

        # Save tab information to config file
        dump_json(self._conf.filepath, self._conf)

        return None

    @staticmethod
    def _gen_conf_file(filepath):
        conf = {
            "filepath": filepath,
            "os": {
                "darwin": {
                    "terminal_command": "osascript -e '\ntell application \"Terminal\"\n do script \"{}\"\n activate\n end tell'"
                },
                "linux": {
                    "terminal_command": "knosole --hold -e /bin/bash -c \"{}; exec /bin/bash\""
                }
            },
            "user_defined_tabs": []
        }

        #TODO: add all os systems into default config
        #TODO: create page to configure os specific commands

        # Creates file and writes json content
        dump_json(filepath, conf)

        return None

    @staticmethod
    def _gen_doc_file(filepath):
        doc = {
            "filepath": filepath,
            "documentation": ""
        }

        # Creates file and writes json content
        dump_json(filepath, doc)

        return None

    @staticmethod
    def _gen_hist_file(filepath):
        hist = {
            "filepath": filepath,
            "history": []
        }

        # Creates file and writes json content
        dump_json(filepath, hist)

        return None