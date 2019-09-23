import sys
import tkinter
import tkinter.ttk

# Local Imports
from utils import Map
from notebook import Notebook
from command_bar import CommandBar

# Constant Definitions
TK = tkinter.Tk

class GUIMain(TK):

    def __new__(cls, configuration, name):
        return super().__new__(cls)

    def __init__(self, config, name):
        super().__init__()

        # Initialize class variables
        self.configuration = config
        self.var_map = self._init_vars()
        self._menu = tkinter.Menu(self)
        self._notebook = None
        self._cmd_bar = None

        # Root configuration
        self.title(name)
        self.geometry("1200x600")

        # Configure menu bar on root
        self.config(menu=self._menu)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        return None

    def __call__(self):
        return self

    def _init_vars(self):
        tvars = Map({
            "filepath": tkinter.StringVar(),
            "new_history": tkinter.StringVar()
        })

        # Variable initializations
        tvars.filepath.set("")
        tvars.new_history.set("")

        return tvars

    def _new_tab(self):

        self._notebook.add_tool_tab("TODO")

        return None
    
    def _on_close(self):

        # Kill root window
        self.destroy()

        return None

    def execute(self):

        # Add menu dropdown
        file_menu = tkinter.Menu(self._menu, tearoff=0)
        file_menu.add_command(label="New Tab", command=self._new_tab)
        self._menu.add_cascade(label="File", menu=file_menu)

        # Create main notebook displaying tabs
        s_nb = {"pack": {"expand": True, "fill": "both"}}
        self._notebook = Notebook(self, **s_nb)

        # Create command bar
        s_cmd_bar = {"pack": {"side": "bottom", "fill": "x", "pady": 5, "padx": 5}}
        self._cmd_bar = CommandBar(self, **s_cmd_bar)

        # Start GUI
        self.mainloop()

        return None