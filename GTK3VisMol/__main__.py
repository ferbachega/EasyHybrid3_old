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

import gi

gi.require_version('Gtk', '3.0')

from VISMOL.vCore.VismolSession import VisMolSession
from GTKGUI import VismolMain


def main():
    vismolSession = VisMolSession(glwidget=True, toolkit='gtk3')

    def menu_show_lines(_):
        """ Function doc """
        vismolSession.show_or_hide(_type='lines', show=True)

    def menu_hide_lines(_):
        """ Function doc """
        vismolSession.show_or_hide(_type='lines', show=False)

    def menu_show_sticks(_):
        """ Function doc """
        vismolSession.show_or_hide(_type='sticks', show=True)

    def menu_hide_sticks(_):
        """ Function doc """
        vismolSession.show_or_hide(_type='sticks', show=False)

    def menu_show_spheres(_):
        """ Function doc """
        vismolSession.show_or_hide(_type='spheres', show=True)

    def menu_hide_spheres(_):
        """ Function doc """
        vismolSession.show_or_hide(_type='spheres', show=False)

    menu = {
        'Teste Menu from main ': ['MenuItem', None],

        'separator1': ['separator', None],

        'show': [
            'submenu', {

                'lines': ['MenuItem', menu_show_lines],
                'sticks': ['MenuItem', menu_show_sticks],
                'spheres': ['MenuItem', menu_show_spheres],
                'separator2': ['separator', None],
                'nonbonded': ['MenuItem', None],

            }
        ],

        'hide': [
            'submenu', {
                'lines': ['MenuItem', menu_hide_lines],
                'sticks': ['MenuItem', menu_hide_sticks],
                'spheres': ['MenuItem', menu_hide_spheres],
                'nonbonded': ['MenuItem', None],
            }
        ],

        'separator2': ['separator', None],

    }

    # vismolSession.insert_glmenu(bg_menu = menu)
    vismolSession.insert_glmenu()

    gui = VismolMain.VismolMainWindow(vismolSession)
    return 0


if __name__ == '__main__':
    main()
