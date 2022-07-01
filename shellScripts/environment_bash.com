#!/bin/bash

# . Bash environment variables and paths to be added to a user's ".bash_profile" file.
# . PDYNAMO3_ORCACOMMAND, PDYNAMO3_SCRATCH and PYTHONPATH will likely need modifying.

# . The root of the program.
EASYHYBRID3_HOME=/home/fernando/programs/EasyHybrid3 ; export EASYHYBRID3_HOME

# . Additional paths.
#PDYNAMO3_ORCACOMMAND=$HOME/programs/orca_local/orca                ; export PDYNAMO3_ORCACOMMAND
GTKVIS=$EASYHYBRID3_HOME/GTK3VisMol                                ; export GTKVIS
PDYNAMO3_PYTHONCOMMAND=python3                                     ; export PDYNAMO3_PYTHONCOMMAND
#PDYNAMO3_SCRATCH=$PDYNAMO3_HOME/scratch                            ; export PDYNAMO3_SCRATCH   
#PDYNAMO3_STYLE=$PDYNAMO3_PARAMETERS/ccsStyleSheets/defaultStyle.css ; export PDYNAMO3_STYLE     

# . The python path.
PYTHONPATH=.:$EASYHYBRID3_HOME ; export PYTHONPATH
