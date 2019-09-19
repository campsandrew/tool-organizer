import sys
import tkinter
import tkinter.ttk

# Local import
from util import new_widget

# Constant Definitions
FRAME = tkinter.ttk.Frame
TREEVIEW = tkinter.ttk.Treeview
SCROLLBAR = tkinter.ttk.Scrollbar

class Tree(TREEVIEW):

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, root, heading, width=100, **kwargs):

        # Class variable initialization
        self._root = root
        self.configuration = root.configuration

        # Create main frame to hold tree parts
        s_tree_frm = {"pack": kwargs["pack"]}
        self._tree_frm = new_widget(root, FRAME, **s_tree_frm)

        # Create tree widget
        new_widget(self._tree_frm, super(), **kwargs)

        # Tree width configuration
        self.column("#0", width=width)
        self.heading("#0", text=heading) # TODO: this is where to add heading click event to sort data
        self._add_verticle_scroll()

        return None

    def _add_verticle_scroll(self):
        s_scroll = {"pack": {"side": "right", "fill": "y"},
                    "orient": "vertical", "command": self.yview}
        v_scroll = new_widget(self._tree_frm, SCROLLBAR, **s_scroll)
        self.configure(yscrollcommand=v_scroll.set)

        return None

    def add_items(self, items):

        # Loop through the items and add them to the tree
        for item in items:
            s_item = {"text": item, "iid": item}
            self.insert("", tkinter.END, **s_item)

        # Set first item as selected
        self.focus(items[0])
        self.selection_set(items[0])

        return self


