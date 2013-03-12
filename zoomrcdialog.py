# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ZoomRCDialog
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
"""

from PyQt4 import QtCore, QtGui
from ui_zoomrc import Ui_ZoomRC
# create the dialog for zoom to point
class ZoomRCDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_ZoomRC()
        self.ui.setupUi(self)
