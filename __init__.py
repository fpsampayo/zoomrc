# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ZoomRC
                                 A QGIS plugin
 Herramienta para hacer zoom a una referencia catastral
                             -------------------
        begin                : 2012-10-03
        copyright            : (C) 2012 by Francisco Pérez Sampayo
        email                : fpsampayo@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
def name():
    return "ZoomRC"
def description():
    return "Tool that allow to zoom to a Spanish Cadastre reference"
def version():
    return "Version 0.2"
def icon():
    return "icon.png"
def qgisMinimumVersion():
    return "1.0"
def author():
    return "Francisco Pérez Sampayo"
def email():
    return "fpsampayo@gmail.com"
def classFactory(iface):
    # load ZoomRC class from file ZoomRC
    from zoomrc import ZoomRC
    return ZoomRC(iface)
