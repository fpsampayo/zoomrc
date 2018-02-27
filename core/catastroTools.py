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


class CatastroTools():
    
    def __init__(self):
        
        self.url = "https://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCoordenadas.asmx/Consulta_CPMRC?"
        
        
    def XYbyRefCat(self, refcat, srs):
        
        valido, msg = self.__validarEpsg(srs)
        if not valido:
            return True, "0", "0", msg
        
        data = parse.urlencode({'Provincia': "",
                                'Municipio': "",
                                'SRS': srs,
                                'RC': refcat}).encode()
                                
        req = request.Request(self.url, data=data)
        resp = request.urlopen(req)
        
        data = resp.read()
        
        dom = minidom.parseString(data)
         
        if len(dom.getElementsByTagName('err')) >= 1:
            errMsg = u'La oficina virtual dice:\n\n'
            desTag = dom.getElementsByTagName('des')[0].toxml()
            errMsg += desTag.replace('<des>','').replace('</des>','')
            
            return True, "0", "0", errMsg
        else:
            xTag = dom.getElementsByTagName('xcen')[0].toxml()
            xcen = xTag.replace('<xcen>','').replace('</xcen>','')
            yTag = dom.getElementsByTagName('ycen')[0].toxml()
            ycen = yTag.replace('<ycen>','').replace('</ycen>','')
            
            return False, xcen, ycen, ""
        
        
    def __validarEpsg(self, epsg):
        
        validProjections = ["EPSG:4230", "EPSG:4326", 
                            "EPSG:4258", "EPSG:32627", 
                            "EPSG:32628", "EPSG:32629", 
                            "EPSG:32630", "EPSG:32631", 
                            "EPSG:25829", "EPSG:25830", 
                            "EPSG:25831", "EPSG:23029", 
                            "EPSG:23030", "EPSG:23031"]
        
        if epsg in validProjections:
            return True, "Ok"
        else:
            msg = u"Proyección no válida!! \nPuede consultar los SRS posibles en: \nhttps://ovc.catastro.meh.es/ovcservweb/OVCSWLocalizacionRC/OVCCoordenadas.asmx?op=Consulta_CPMRC"
            return False, msg



