import sys
import tkinter
import tkinter.ttk

# Local Imports
from utils import new_widget

# Constant Variables
ENTRY = tkinter.ttk.Entry
STYLE = tkinter.ttk.Style

class ResponsiveEntry(ENTRY):

    #################
    # Special Methods
    #################
    def __init__(self, root, default="", **kwargs):

        # Private Class Variables
        self._root = root
        self._style = STYLE()
        self._default = default

        # Configure styles
        self._style.configure("CommandDefault.TEntry", foreground="grey")
        self._style.configure("Command.TEntry", foreground="black")

        # Create entry widget
        kwargs["style"] = "CommandDefault.TEntry"
        new_widget(root, super(), **kwargs)
        self.insert(0, self._default)

        # Add event bindings to entry
        self.bind("<FocusIn>", self._entry_focus)
        self.bind("<FocusOut>", self._entry_focus)
        #self.bind("<Return>", self._)

        return None

    #################
    # Private Methods
    #################
    def _entry_focus(self, event):
        text = self.get()
        is_default = text == self._default
        no_text = text == ""

        # Perform FocusIn vs FocusOut conditions
        if str(event.type) == "FocusIn" and is_default:
            self["style"] = "Command.TEntry"
            self.delete(0, tkinter.END)
        elif str(event.type) == "FocusOut" and no_text:
            self["style"] = "CommandDefault.TEntry"
            self.insert(tkinter.INSERT, self._default)
        else: pass

        return None

    ################
    # Public Methods
    ################
    def clear(self):

        # Send cursor to entry and delete
        self["style"] = "Command.TEntry"
        self.focus()
        self.delete(0, tkinter.END)

        return None

    