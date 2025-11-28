# -*- coding: utf-8 -*-
"""
/***************************************************************************

                                 A QGIS plugin
 Zoom to a Spanish Cadastre Reference
                             -------------------
        begin                : 2018-02-27
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Francisco P. Sampayo
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

from urllib import request, parse
from xml.dom import minidom
from qgis.core import QgsVectorLayer, QgsRectangle, QgsProject
from qgis.gui import QgsRubberBand
from PyQt5.QtGui import QColor

from qgis.core import Qgis

class CatastroTools():

    def __init__(self, iface):

        self.iface = iface
        self.urlWfs = 'https://ovc.catastro.meh.es/INSPIRE/wfsCP.aspx?service=wfs&version=2&request=getfeature&typenames=cp:CadastralParcel&STOREDQUERIE_ID={}&srsname={}&REFCAT={}'
        self.rubber = QgsRubberBand(self.iface.mapCanvas(), Qgis.GeometryType.Polygon)

    def XYbyRefCat(self, refcat, srs, resaltar=True, cargarCapa=False, lindantes=False):

        self.clearRubber()

        valido, msg = self.__validarEpsg(srs)
        if not valido:
            return False, msg

        url = self.urlWfs.format('GetParcel', srs, refcat)
        layer = QgsVectorLayer(url, refcat, 'ogr')
        if not layer.isValid():
            return False, "Error cargando la capa."
        else:
            feat = list(layer.getFeatures())
            geom = None
            if len(feat) == 1:
                geom = feat[0].geometry()

            if resaltar:
                self.rubber.setToGeometry(geom, layer)
                self.rubber.setColor(QColor(0, 0, 255, 50))
                self.rubber.setWidth(3)

            if cargarCapa:
                if lindantes:
                    url = self.urlWfs.format('GetNeighbourParcel', srs, refcat)
                    layer_lindantes = QgsVectorLayer(url, refcat + '_lindantes', 'ogr')
                    QgsProject.instance().addMapLayer(layer_lindantes)
                QgsProject.instance().addMapLayer(layer)

            self.iface.mapCanvas().setExtent(geom.boundingBox())
            self.iface.mapCanvas().refresh()

        return True, ""


    def clearRubber(self):

        self.rubber.reset()


    def __validarEpsg(self, epsg):

        validProjections = [
            "EPSG:4326",
            "EPSG:4258",
            "EPSG:25829",
            "EPSG:25830",
            "EPSG:25831",
            "EPSG:3785",
            "EPSG:3857",
            "EPSG:3035",
            "EPSG:3041",
            "EPSG:3042",
            "EPSG:3043",
            "EPSG:32627",
            "EPSG:32628"
        ]

        if epsg in validProjections:
            return True, "Ok"
        else:
            msg = u"Proyección no válida!! \n" \
                  u"Puede consultar los SRS posibles en: \n" \
                  u"https://ovc.catastro.meh.es/INSPIRE/wfsCP.aspx?service=WFS&Version=2.0.0&request=GetCapabilities"
            return False, msg



