import sys
import tkinter
import tkinter.ttk
import tkinter.font

# Local import
from utils import new_widget

# Constant Variables
MENU = tkinter.Menu
FRAME = tkinter.ttk.Frame
TREEVIEW = tkinter.ttk.Treeview
SCROLLBAR = tkinter.ttk.Scrollbar

class Table(TREEVIEW):

    #################
    # Special Methods
    #################
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, root, headings=[], addable=True,
                 decending=True, **kwargs):

        # Private class variable
        self._table_frm = None
        self._items = None
        self._root = root
        self._order = decending
        self._addable = addable
        self._headings = headings
        self._font = tkinter.font.Font()

        # Create main frame to hold tree parts
        s_table_frm = {"pack": {"side": "right", "fill": "both", "expand": True}, "borderwidth": 5,
                                "relief": tkinter.RAISED}
        self._table_frm = new_widget(root, FRAME, **s_table_frm)

        # Create tree widget
        s_table = {"pack": {"side": "left", "fill": "both", "expand": True,
                            "pady": 5, "padx": (5, 0)}, "selectmode": "extended",
                   "show": "headings"}
        new_widget(self._table_frm, super(), **s_table)
        self._add_verticle_scroll()
        self._add_headings()

        # Table event bindings
        self.bind("<Button-1>", self._on_click)
        self.bind("<Configure>", self._on_configuration)

        return None

    #################
    # Private Methods
    #################
    def _add_verticle_scroll(self):
        s_scroll = {"pack": {"side": "right", "fill": "y", "pady": 5,
                             "padx": (0, 5)},
                    "orient": "vertical", "command": self.yview}
        v_scroll = new_widget(self._table_frm, SCROLLBAR, **s_scroll)
        self.configure(yscrollcommand=v_scroll.set)

        return None

    def _add_headings(self):
        self["columns"] = [h.labels[0] for h in self._headings]

        # Add all headings to table
        for i, column in enumerate(self["columns"]):
            col_id = "#" + str(i + 1)
            self._headings[i].col_id = col_id
            self.heading(col_id, text=column)

        return None

    #######################
    # Event/Binding Methods
    #######################
    def _on_click(self, event):
        region = self.identify("region", event.x, event.y)

        # Disable column resize for tree
        if region == "separator":
            return "break"

        return None

    def _on_configuration(self, event):

        print(event.width)

        return None

    ################
    # Public Methods
    ################
    def add_items(self, items):
        self._items = items

        # Add all items to table
        for item in items:
            s_item = {"values": item}
            self.insert("", tkinter.END, **s_item)

            # TODO: Make function to do complex column width adjustment
            #w, h = self._font.measure(item[-1]), self._font.metrics("linespace")
            #m.append(w)

        #self.column("#2", width=max(m))

        return None

    # TODO: need to sort items after adding
    def add(self, item):
        #s_item = {"values": item}
        #self.insert("", tkinter.END, **s_item)

        return None

    