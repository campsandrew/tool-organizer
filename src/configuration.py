import os
import sys

# Local File Imports
from map import Map
from util import load_json
from util import dump_json

HOME = os.path.expanduser("~")
TORG_CONF_PATH = os.path.join(HOME, ".torg")
TORG_DOC_FILE = os.path.join(TORG_CONF_PATH, "torg.doc")
TORG_HIST_FILE = os.path.join(TORG_CONF_PATH, "torg.hist")
TORG_CONF_FILE = os.path.join(TORG_CONF_PATH, "torg.conf")

class Configuration:

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

        return tabs

    def get_terminal_command(self):
        t_cmd = None

        if sys.platform == "linux":
            t_cmd = self._conf.os.linux.terminal_command
        elif sys.platform == "darwin":
            t_cmd = self._conf.os.darwin.terminal_command
        else: pass

        return t_cmd

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
        #TODO: create page to configure operating system commands

        # Creates file and writes json content
        dump_json(filepath, conf)

        return None

    @staticmethod
    def _gen_doc_file(filepath):
        doc = {
            "filepath": filepath,
            "doc": ""
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