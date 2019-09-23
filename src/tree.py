import sys
import tkinter
import tkinter.ttk

# Local import
from utils import new_widget

# Constant Definitions
MENU = tkinter.Menu
FRAME = tkinter.ttk.Frame
TREEVIEW = tkinter.ttk.Treeview
SCROLLBAR = tkinter.ttk.Scrollbar

class Tree(TREEVIEW):

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self, root, headings=["Decending", "Acending"], addable=True,
                 decending=True, width=150, selectmode="browse",
                 pack={"side": "left", "fill": "y"}, **kwargs):

        # Class variable initialization
        self._root = root
        self._order = decending
        self._addable = addable
        self._headings = headings
        self.deleted = None

        # Create main frame to hold tree parts
        self._tree_frm = new_widget(root, FRAME, **{"pack": pack})

        # Create tree widget
        options = {"pack": pack, "selectmode": selectmode}
        new_widget(self._tree_frm, super(), **options, **kwargs)

        # Tree width configuration
        self.heading("#0", text=headings[int(not self._order)])
        self.column("#0", width=width)
        self._add_verticle_scroll()

        # Tree bindings
        self.bind("<Button-1>", self._on_click)
        self.bind("<Button-2>", self._on_right_click)

        return None

    def __contains__(self, item):
        return item in self.get_children()

    def _add_verticle_scroll(self):
        s_scroll = {"pack": {"side": "right", "fill": "y"},
                    "orient": "vertical", "command": self.yview}
        v_scroll = new_widget(self._tree_frm, SCROLLBAR, **s_scroll)
        self.configure(yscrollcommand=v_scroll.set)

        return None

    def _on_click(self, event):
        region = self.identify("region", event.x, event.y)

        # Disable column resize for tree
        if region == "separator":
            return "break"

        # Sort tree if heading is clicked
        if region == "heading":
            self.sort()

        return None

    def _on_right_click(self, event):
        popup_menu = new_widget(self, MENU, **{"tearoff": 0})
        item = self.identify_row(event.y)

        # Create add menu button if tree can be added to by user
        if self._addable:
            popup_menu.add_command(label="Add", command=self._on_item_add)
        
        # If user right clicked on a tree item
        if item:
            popup_menu.add_command(label="Delete", command=self._on_item_delete)
            self.selection_set(item)
            self.focus(item)

        # Cause menu to popup
        try:
            popup_menu.tk_popup(event.x_root, event.y_root + 30, 0)
        finally:
            popup_menu.grab_release()

        return None

    def _on_item_add(self):
        # TODO: figure out how this will work
        
        return None

    # TODO: this needs to be implemented one level up (tab specific)
    def _on_item_delete(self):
        item = self.selection()[0]
        self.delete(item)
        self.deleted = item
        self.event_generate("<<DeleteItem>>", data=item)

        return None

    def add_items(self, items):

        # Loop through the items and add them to the tree
        for item in items:
            s_item = {"text": item, "iid": item}
            self.insert("", tkinter.END, **s_item)

        # Set first item as selected
        if items:
            self.focus(items[0])
            self.selection_set(items[0])

        return self

    def add(self, item):
        items = list(self.get_children())

        # Remove all items from tree
        self.delete(*items)

        # Add new item in correct sorted order
        items.append(item)
        items.sort(reverse=self._order)
        self.add_items(items)

        return None

    def sort(self):
        self.heading("#0", text=self._headings[int(self._order)])
        self._order = not self._order
        items = list(self.get_children())

        # Remove all items from tree
        self.delete(*items)

        # Sorts item list and add back to tree
        items.sort(reverse=self._order)
        self.add_items(items)

        return None


