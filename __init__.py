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

def classFactory(iface):
    # load ZoomRC class from file ZoomRC
    from zoomrc import ZoomRC
    return ZoomRC(iface)
