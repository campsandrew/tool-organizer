import os
import sys
import json
import tkinter
import tkinter.ttk

# Local Imports
from utils import new_widget
from responsive_entry import ResponsiveEntry

# Constant Definitions
FRAME = tkinter.ttk.Frame
LABEL = tkinter.ttk.Label
BUTTON = tkinter.ttk.Button

class CommandBar(FRAME):
    RUN_TEXT = "Run"
    SAVE_TEXT = "Save"
    CLEAR_TEXT = "Clear"
    COMMAND_DEFAULT_TEXT = "Enter Command"

    def __init__(self, root, **kwargs):

        # Class variable initializations
        self._root = root
        self.configuration = root.configuration
        self.var_map = root.var_map
        self._run_btn = None
        self._save_btn = None
        self._clear_btn = None
        self._cmd_entry = None
        self._file_lb = None

        # Create main frame
        new_widget(root, super(), **kwargs)

        #TODO: make entry wrap. Need to switch this to Text entry
        # Add children to main frame
        s_cmd_entry = {"pack": {"fill": "x", "pady": (0, 5)}, 
                       "default": self.COMMAND_DEFAULT_TEXT}
        self._cmd_entry = ResponsiveEntry(self, **s_cmd_entry)
        self._cmd_entry.focus()
        self._add_actions()

        # Add event bindings
        self._cmd_entry.bind("<Return>", lambda e: self._action_click(self.RUN_TEXT))

        return None

    def __call__(self):
        return self

    def _add_actions(self):
        btn_texts = [self.RUN_TEXT, self.SAVE_TEXT, self.CLEAR_TEXT]
        btn_vars = [self._run_btn, self._save_btn, self._clear_btn]

        # Adding layout frames
        s_action_frm = {"pack": {"fill": "x"}}
        s_btn_frm = {"pack": {"side": "right", "fill": "x"}}
        action_frm = new_widget(self, FRAME, **s_action_frm)
        btn_frm = new_widget(action_frm, FRAME, **s_btn_frm)

        # Adding file label
        s_file_lb = {"pack": {"side": "left"}, "text": self.var_map.filepath.get(),
                     "font": ("Courier", 8)}
        self._file_lb = new_widget(action_frm, LABEL, **s_file_lb)
        self.var_map.filepath.trace("w", self._on_filepath_change)

        # Adding all command buttons
        for i in range(len(btn_vars)):
            s_btn = {"pack": {"side": "right", "padx": (5, 0)}, "text": btn_texts[i]}
            btn_vars[i] = new_widget(btn_frm, BUTTON, **s_btn)
            btn_vars[i]["command"] = lambda text=btn_texts[i]: self._action_click(text)

        return None

    def _on_filepath_change(self, *args):
        self._file_lb["text"] = self.var_map.filepath.get()

        return None

    def _action_click(self, btn_text):
        cmd = self._cmd_entry.get()
        no_cmd = cmd == self.COMMAND_DEFAULT_TEXT

        # Check the type of button clicked
        if btn_text == self.CLEAR_TEXT:
            self._cmd_entry.clear()
        elif btn_text == self.RUN_TEXT and not no_cmd:
            hist = self.configuration.add_history(cmd) # TODO: Need to stringify this and save in variable
            self.var_map.new_history.set(json.dumps(hist))
            t_cmd = self.configuration.get_terminal_command()
            os.system(t_cmd.format(cmd))
        elif btn_text == self.SAVE_TEXT and not no_cmd:
            #TODO: Create popup to pick save location
            pass
        else: pass

        return None