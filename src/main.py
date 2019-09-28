#!/usr/bin/env python3

import os
import sys

# Local python file imports
from gui_main import GUIMain
from configuration import Configuration

__version__ = "1.0.0"

NAME = "Tool Organizer - v" + __version__

#### TAB ####
# TODO: Make tool settings have collapsable label frames
# TODO: Add live updating history when a command is entered on history page

#### TREE ####
# TODO: Add and remove items in tree

#### TABLE ####
# TODO: Add text wrapping to cells with wrap is defined in headings maps
# TODO: Column sorting based on which headings have sortable headings
# TODO: Add and remove items from table

#### RESPONSIVE ENTRY ####
# TODO: Have text wrap if too long

#### MISC ####


def main():

    # Initialize configuration
    try:
        config = Configuration()
    except(IOError, OSError, ValueError) as e:
        print("{}".format(e))
        sys.exit()
    except:
        print("Unexpected Error:", sys.exc_info()[0])
        sys.exit()
  
    # Initialize and start gui
    GUIMain(config, NAME).execute()

    return None

# MAIN ENTRY POINT
if __name__ == "__main__":
    main()