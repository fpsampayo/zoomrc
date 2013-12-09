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
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from zoomrcdialog import ZoomRCDialog

from xml.dom import minidom 
from xml.dom.minidom import parseString
import urllib2
import urllib

class ZoomRC:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/zoomrc"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale")[0:2]
       
        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/zoomrc_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)
   

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(QIcon(":/plugins/zoomrc/icon.png"), \
            u"Catastro - ZoomRC", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Catastro - ZoomRC", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Catastro - ZoomRC",self.action)
        self.iface.removeToolBarIcon(self.action)
        
    def consultaCatastro(self, refcat, escala, projection):
        
         # The Spanish Cadastre url service 
        url = "https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCoordenadas.asmx/Consulta_CPMRC?"
        params = urllib.urlencode({'Provincia' : "", 'Municipio' : "", 'SRS' : projection, 'RC' : refcat})
        print url + params
        try:
            try:
                f = urllib2.urlopen(url, params, timeout=10)
            except URLError, e:
                print "Tiempo de expera máximo alcanzado.\nLa sede electrónica de la DGC no está accesible."
                QMessageBox.information(None, "Aviso", "Tiempo de expera máximo alcanzado.\nLa sede electrónica de la DGC no está accesible.")
                pass
            
            data = f.read()
            f.close()
            dom = parseString(data)
            
            if len(dom.getElementsByTagName('err')) >= 1:
                errMsg = u'La oficina virtual dice:\n\n'
                desTag = dom.getElementsByTagName('des')[0].toxml()
                errMsg += desTag.replace('<des>','').replace('</des>','')
                QMessageBox.information(self.dlg, "Aviso", errMsg)
            else:
                xTag = dom.getElementsByTagName('xcen')[0].toxml()
                xcen = xTag.replace('<xcen>','').replace('</xcen>','')
                
                yTag = dom.getElementsByTagName('ycen')[0].toxml()
                ycen = yTag.replace('<ycen>','').replace('</ycen>','')
                
                self.zoomToPoint(xcen, ycen, escala)
                pass
        except:
            QMessageBox.information(None, "Aviso", "Error al obtener coordenadas.")
        
    '''This function alow to center the map view en a x, y and scale'''    
    def zoomToPoint(self, xcen, ycen, scale):
        
        mc = self.iface.mapCanvas()
        
        rect = QgsRectangle(float(xcen)-20,float(ycen)-20,float(xcen)+20,float(ycen)+20)
        mc.setExtent(rect)
        mc.zoomScale(scale)
        
        mc.refresh()
        
        
    '''Fuction to validate if the projection of the canvas equals with one 
    of the Spanish Cadastre SRS'''
    def validarEpsg(self, epsg):
        
        validProjections = ["EPSG:4230", "EPSG:4326", 
                            "EPSG:4258", "EPSG:32627", 
                            "EPSG:32628", "EPSG:32629", 
                            "EPSG:32630", "EPSG:32631", 
                            "EPSG:25829", "EPSG:25830", 
                            "EPSG:25831", "EPSG:23029", 
                            "EPSG:23030", "EPSG:23031"]
        
        if epsg in validProjections:
            return True
        else:
            QMessageBox.information(None, "Aviso", u"Proyección no válida!! \nPuede consultar los SRS posibles en: \nhttps://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCoordenadas.asmx?op=Consulta_CPMRC")
            return False
    '''Function to validate the fields of the ui_zoomrc form.'''    
    def validateFields(self):
        #QMessageBox.information(None, "Aviso", "Ok")
        
        msg = ''
        ui = self.dlg.ui
        if ui.cmpRefCat.text() == '' or \
            ui.cmpEscala.text() == '':
                msg = u'Ningún campo debe estar vacío.\n'
        if len(ui.cmpRefCat.text()) != 14:
            msg += u'La referencia catastral debe tener 14 dígitos.\n'
        try:
            flt = float(ui.cmpEscala.text())
        except ValueError:
            msg += u'El campo escala debe ser numérico.\n'
        if msg != '':
            QMessageBox.warning(self.dlg, "Aviso", msg)
        else:
            self.dlg.accept()
        
    # run method that performs all the real work
    def run(self):
        
        self.dlg = ZoomRCDialog()
        
        QObject.connect(self.dlg.ui.buttonBox, SIGNAL("accepted()"), self.validateFields)
        
        
        # show the dialog
        self.dlg.show()
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1:
            # Gets the canvas actual SRS Projection in EPSG
            projection = self.iface.mapCanvas().mapRenderer().destinationCrs().authid()
            refcat = self.dlg.ui.cmpRefCat.text()
            escala = float(self.dlg.ui.cmpEscala.text())
            if self.validarEpsg(projection):
                self.consultaCatastro(refcat, escala, projection)
            else:
                self.run()
