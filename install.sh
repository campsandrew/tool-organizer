#!/bin/bash

# Get referenitial directory of install path
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Make bin directory if doesn't exist
if [ ! -d $HOME/bin ]
then
    mkdir $HOME/bin
    mkdir $HOME/bin/tool-organizer
fi

# Move source directory to install path
cp -r $DIR/* $HOME/bin/tool-organizer
chmod +x $HOME/bin/tool-organizer/torg

# Add tool path to .bash_profile or .bashrc
if [[ ":$PATH:" != *":$HOME/bin/tool-organizer:"* ]]
then
    if [ -f $HOME/.bash_profile ]
    then
        echo "export PATH=$HOME/bin/tool-organizer:${PATH}" >> $HOME/.bash_profile
    else
        echo "export PATH=$HOME/bin/tool-organizer:${PATH}" >> $HOME/.bashrc
    fi

    echo "Restart your terminal..."
fi