import os
import sys
import json
import inspect

# import tkinter
# import tkinter.ttk

# FRM = tkinter.ttk.Frame
# NB = tkinter.ttk.Notebook
# ST = tkinter.scrolledtext.ScrolledText
# TV = tkinter.ttk.Treeview
# BTN = tkinter.ttk.Button
# ENT = tkinter.ttk.Entry
# LB = tkinter.ttk.Label
# SBX = tkinter.ttk.Spinbox

# def add_notebook(root, tabs):
#   pages = {}

#   # Define Notebook
#   s_nb = {"pack": {"expand": True, "fill": "both", "pady": 5}}
#   nb = add_widget(root, NB, **s_nb)

#   # Add all tabs to notebook
#   for tab in tabs:
#     pages[tab] = add_widget(nb, FRM, **s_nb)
#     nb.add(pages[tab], text=tab)

#   return nb, pages

# def add_treeview(root):

#     s_tv = {"pack": {"side": "left", "fill": "y"}, "show": "tree",
#             "selectmode": "browse"}
#     tree = add_widget(root, TV, **s_tv)
#     tree.column("#0", width=100)

#     return tree

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