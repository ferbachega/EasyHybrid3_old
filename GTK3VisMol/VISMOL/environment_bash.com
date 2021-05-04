#!/bin/bash

# . Bash environment variables and paths to be added to a user's ".bash_profile" file.
# . Some of these values may need modifying (e.g. PDYNAMO_SCRATCH and PYTHONPATH).

# . The root of the program.
VISMOL=/home/fernando/programs/EasyHybrid3/GTK3VisMol/VISMOL ; export PDYNAMO_ROOT

# . Package paths.
#PDYNAMO_PBABEL=$PDYNAMO_ROOT/pBabel-1.9.0                     ; export PDYNAMO_PBABEL           
#PDYNAMO_PCORE=$PDYNAMO_ROOT/pCore-1.9.0                       ; export PDYNAMO_PCORE            
#PDYNAMO_PMOLECULE=$PDYNAMO_ROOT/pMolecule-1.9.0               ; export PDYNAMO_PMOLECULE       
#PDYNAMO_PMOLECULESCRIPTS=$PDYNAMO_ROOT/pMoleculeScripts-1.9.0 ; export PDYNAMO_PMOLECULESCRIPTS 

# . Additional paths.
VISMOL_GLCORE=$VISMOL/glCore                                    ; export VISMOL_GLCORE

VISMOL_GLWIDGET=$VISMOL/glWidget                                ; export VISMOL_GLWIDGET 

#PDYNAMO_PYTHONCOMMAND=/usr/bin/python3                            ; export PDYNAMO_PYTHONCOMMAND 


#PDYNAMO_ORCACOMMAND=$/home/fernando/programs/orca_3_0_3_linux_x86-64/orca ; export PDYNAMO_ORCACOMMAND 

# . The python path.
#PYTHONPATH=:$PDYNAMO_ROOT/pBabel-1.9.0:$PDYNAMO_ROOT/pCore-1.9.0:$PDYNAMO_ROOT/pGraph-0.1:$PDYNAMO_ROOT/pMolecule-1.9.0:$PDYNAMO_ROOT/pMoleculeScripts-1.9.0 ; export PYTHONPATH

PYTHONPATH=$VISMOL ; export PYTHONPATH
