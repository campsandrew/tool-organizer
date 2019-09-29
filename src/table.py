import sys
import tkinter
import tkinter.ttk
import tkinter.font

# Local Imports
from utils import Map
from utils import new_widget

# Constant Variables
SIZE_BUFFER = 15
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
        self._sorted = None
        self.deleted = None
        self._items = []
        self._root = root
        self._order = decending
        self._addable = addable
        self._headings = headings
        self._width_adjust = True
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
        self.bind("<Button-2>", self._on_right_click)
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

        # Sort column when clicked on if sortable
        # if region == "heading":
        #     column = self.identify_column(event.x).split("#")[-1]
        #     index = int(column) - 1

        return None

    def _on_right_click(self, event):
        popup_menu = new_widget(self, MENU, **{"tearoff": 0})
        item = self.identify_row(event.y)
        items = self.selection()

        # Create add menu button if table can be added to
        if self._addable:
            popup_menu.add_command(label="Add", command=self._on_item_add)
        
        # If user right clicked on a tree item
        if items:
            popup_menu.add_command(label="Delete", command=self._on_item_delete)
        elif item:
            popup_menu.add_command(label="Delete", command=self._on_item_delete)
            self.selection_set(item)
            self.focus(item)
            self.update()
        else: pass

        # Cause menu to popup
        try: popup_menu.tk_popup(event.x_root, event.y_root + 30, 0)
        finally: popup_menu.grab_release()

        return None

    def _on_item_add(self):
        return None

    def _on_item_delete(self):
        items = self.selection()
        self.deleted = [self.item(item, "values") for item in items]
        self.delete(*items)
        self.event_generate("<<DeleteItems>>")

        return None

    def _on_configuration(self, event):
        if not self._width_adjust: return None
        sizes = [[] for c in self["columns"]]
        self._width_adjust = False
        total_width = event.width
        fixed = []

        # Take heading text withs into account
        for i, column in enumerate(self["columns"]):
            w = self._font.measure(column) + SIZE_BUFFER
            sizes[i].append(w)

        # Loop through all items in table
        for item in self._items:

            # Loop through each columns in table
            for i in range(len(item)):
                w = self._font.measure(item[i]) + SIZE_BUFFER
                sizes[i].append(w)

        # Configure column widths autosized columns
        sizes = [max(s) for s in sizes]
        for i, size in enumerate(sizes):
            heading = self._headings[i]

            # Check if columns should be autosized
            if not heading.autosize:
                fixed.append(self["columns"][i])
                continue

            # Apply widths
            total_width -= size
            self.column(self["columns"][i], width=size, stretch=False)

        # Set width of fixed size columns
        total_width /= len(fixed)
        for column in fixed:
            self.column(column, width=int(total_width))

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

        # Will reconfigure column withs for autosize columns
        self._width_adjust = True
        self._on_configuration(Map({"width": self.winfo_width()}))

        return self

    def add(self, item):
        s_item = {"values": item}
        self.insert("", tkinter.END, **s_item)

        # Will reconfigure column withs for autosize columns
        self._width_adjust = True
        self._on_configuration(Map({"width": self.winfo_width()}))

        return None

    def sort(self, index):
        heading = self._headings[index]

        # Remove all items from tree
        self.delete(*self.get_children())

        # Get values of column being sorted
        col_dict = {}
        for item in self._items:
            col_dict[item[index]] = item

        # Sort the column
        column = list(col_dict.keys())
        column.sort(reverse=self._order)
        self._items = [col_dict[item] for item in column]

        # Add all items to table
        for item in self._items:
            s_item = {"values": item}
            self.insert("", tkinter.END, **s_item)

        # Swap the order of current sorted column
        self._order = not self._order

        return None


    