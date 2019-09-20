import sys
import json
import inspect

# LB = tkinter.ttk.Label
# SBX = tkinter.ttk.Spinbox

def load_json(filepath):

    # Opening config file and reading json
    with open(filepath) as cfile:
        config = json.load(cfile)

    return config

def dump_json(filepath, data):

    # Creates file and writes json content
    with open(filepath, "w") as cfile:
        json.dump(data, cfile, indent=4)

    return None

def new_widget(root, widget, **kw):
    if "pack" in kw: pack = kw.pop("pack")
    else: pack = {}
    if "grid" in kw: grid = kw.pop("grid")
    else: grid = {}

    # Create Widget
    if inspect.isclass(widget):
        wdgt = widget(root, **kw)
    else:
        widget.__init__(root, **kw)
        wdgt = widget

    # Widget Layout Configuration
    if pack: wdgt.pack(**pack)
    if grid: wdgt.grid(**grid)

    return wdgt

class Map(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

        return None

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super().__delitem__(key)
        del self.__dict__[key]

    @staticmethod
    def recursive_map(mp):
        nomap = []

        for attr in [a for a in vars(mp)]:
            if attr in nomap: continue
            if type(mp[attr]) is not dict:
                if type(mp[attr]) is list:
                    for i, item in enumerate(mp[attr]):
                        if type(item) is dict:
                            mp[attr][i] = Map.recursive_map(Map(item))
                continue

            mp[attr] = Map.recursive_map(Map(mp[attr]))

        return mp

# def link_hover_enter(link):
#     link["font"] = ("Courier", 10, "underline", "bold")

#     return None

# def link_hover_leave(link):
#     link["font"] = ("Courier", 10, "underline")

#     return None

# def destroy_children(root):

#     # Remove all items from frame
#     for widget in root.winfo_children():
#         widget.destroy()

#     return None

# def open_browser(url):

#   # Fixing bug in webbrowser register function
#   if os.environ.get("BROWSER") is not None:
#     del os.environ["BROWSER"]

#   # Open Browser
#   webbrowser.open_new(url)

#   return None

# def grid_config(root, rows, columns, **kw):

#     # Rows
#     for row in range(0, rows):
#         if "row" in kw and row in kw["row"]:
#         root.grid_rowconfigure(row, **kw["row"][row])
#         continue

#         root.grid_rowconfigure(row, weight=1)

#     # Columns
#     for column in range(0, columns):
#         if "col" in kw and row in kw["col"]:
#         root.grid_columnconfigure(column, **kw["col"][column])
#         continue

#         root.grid_columnconfigure(column, weight=1)

#     return None