#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  __main__.py
#  
#  Copyright 2016 Carlos Eduardo Sequeiros Borja <casebor@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import gi, sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import os


#from visual import vismol
#from visual import vis_parser
#from visual import vismol_shaders as vm_sh
#from VISMOL  import vismol_core

'''
from VISMOL.vCore.VismolSession  import VisMolSession
'''
from gtkGUI  import gtkgui


#from easymol import * 
#from EasyMol import vis_parser





"""Definitions needed by the examples.

import glob, math, os.path

from pBabel                    import ExportSystem                                 , \
                                  ImportCoordinates3                           , \
                                  ImportSystem                                 , \
                                  SMILES_ToSystem                              , \
                                  SystemGeometryTrajectory                     , \
                                  SystemRestraintTrajectory
from pCore                     import Clone                                        , \
                                  logFile                                      , \
                                  Selection                                    , \
                                  TestScript_InputDataPath                     , \
                                  TestScript_OutputDataPath                    , \
                                  XHTMLLogFileWriter
from pMolecule                 import RestraintDistance                            , \
                                  RestraintEnergyModelHarmonic                 , \
                                  RestraintEnergyModelHarmonicRange            , \
                                  RestraintModel                               , \
                                  RestraintTether                              , \
                                  System                                       , \
                                  SystemGeometryObjectiveFunction
from pMolecule.MMModel         import MMModelOPLS
from pMolecule.NBModel         import NBModelCutOff                                , \
                                  NBModelFull                                  , \
                                  NBModelMonteCarlo                            , \
                                  NBModelORCA                                  , \
                                  PairwiseInteractionABFS
from pMolecule.QCModel         import DIISSCFConverger                             , \
                                  QCModelMNDO
from pScientific               import Constants                                    , \
                                  Units
from pScientific.Arrays        import ArrayPrint2D
from pScientific.Geometry3     import PairListGenerator                            , \
                                  Vector3
from pScientific.RandomNumbers import NormalDeviateGenerator                       , \
                                  RandomNumberGenerator
from pScientific.Statistics    import Statistics
from pScientific.Symmetry      import CrystalSystemCubic                           , \
                                  PeriodicBoundaryConditions                   , \
                                  SymmetryParameters
from pSimulation               import BakerSaddleOptimize_SystemGeometry           , \
                                  BuildCubicSolventBox                         , \
                                  BuildHydrogenCoordinates3FromConnectivity    , \
                                  BuildSolventBox                              , \
                                  ChainOfStatesOptimizePath_SystemGeometry     , \
                                  ConjugateGradientMinimize_SystemGeometry     , \
                                  GrowingStringInitialPath                     , \
                                  LeapFrogDynamics_SystemGeometry              , \
                                  MergeByAtom                                  , \
                                  MonteCarlo_IsolateInteractionEnergy          , \
                                  MonteCarlo_ScaleIsolateInteractionParameters , \
                                  MonteCarlo_SystemGeometry                    , \
                                  NormalModes_SystemGeometry                   , \
                                  NormalModesTrajectory_SystemGeometry         , \
                                  PruneByAtom                                  , \
                                  RadialDistributionFunction                   , \
                                  SelfDiffusionFunction                        , \
                                  SolventCubicBoxDimensions                    , \
                                  SolvateSystemBySuperposition                 , \
                                  SteepestDescentPath_SystemGeometry           , \
                                  SystemDensity                                , \
                                  ThermodynamicsRRHO_SystemGeometry            , \
                                  VelocityVerletDynamics_SystemGeometry        , \
                                  WHAM_ConjugateGradientMinimize

# . Local name.
_name  = "book"

# . The input data paths.
dataPath = TestScript_InputDataPath ( _name )cd E
molPath  = os.path.join ( dataPath, "mol" )
pdbPath  = os.path.join ( dataPath, "pdb" )
pklPath  = os.path.join ( dataPath, "pkl" )
xyzPath  = os.path.join ( dataPath, "xyz" )

# . The output data path.
scratchPath = TestScript_OutputDataPath ( _name )
#"""


def main():
    
    #vismolSession  =  VisMolSession(glwidget = True, backend = 'gtk3')
	vismolSession  = None
	gui            = gtkgui.GTKGUI(vismolSession)
	return 0 

if __name__ == '__main__':
    main()

