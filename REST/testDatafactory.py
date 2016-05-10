import unittest
class TestStringMethods(unittest.TestCase):
	def test_getData(self):
		self.path = '/scidb/framedb/OSIRIS/2009-04-01/OsirisBroadBandImage/2009-04-18_20_28_52/raw/0000001762-20090418-OSIRIS-OsirisBroadBandImage.fits'
		data = getDataFitsImages(self.path)
		try:
			self.assertEqual(data[0]['GTCPROGI'][0], 999)
		except KeyError:
			self.assertEqual(data[0]['GTCPRGID'][0], 999)
		try:
			self.assertEqual(data[0]['INSTRUME'][0], 'OSIRIS')
		except KeyError:
			self.assertEqual(data[0]['INSTRUME'][0], 'OSIRIS')
		try:
			self.assertEqual(data[0]['OBSMODE'][0], 'OsirisBroadBandImage')
		except KeyError:
			self.assertEqual(data[0]['OBSMODE'][0], 'OsirisBroadBandImage')
		self.data = data
	def test_hchecker(self):
		self.test_getData()
		check = Checker('/scidb/framedb/OSIRIS/2009-04-01/OsirisBroadBandImage/2009-04-18_20_28_52/raw/0000001762-20090418-OSIRIS-OsirisBroadBandImage.fits')
		a = check.isRaw()
		self.assertEqual(a, 1)
		self.assertEqual(check.getPathWithoutFileName(), '/scidb/framedb/OSIRIS/2009-04-01/OsirisBroadBandImage/2009-04-18_20_28_52/raw')
		self.assertEqual(check.getFileName(), '0000001762-20090418-OSIRIS-OsirisBroadBandImage.fits')
		self.assertEqual(check.getDataByPath('INSTRUME'), 'OSIRIS')
		self.assertEqual(check.getDataByPath('OBSMODE'), 'OsirisBroadBandImage')
		self.assertEqual(check.getDataByPath('DATE'), '2009-04-01')
		self.assertEqual(check.getNumberFrame(), '0000001762')
		self.assertEqual(check.checkObservationMode(self.data), 'OsirisBroadBandImage')
		b = check.checkProgramKey(self.data)
		self.assertEqual(b, 999)
		self.check = check
	def test_models(self):
		self.models = SetModels()
		self.assertEqual(self.models.camera.id, None)
		self.assertEqual(self.models.observationMode.id, None)
		self.assertEqual(self.models.frame.id, None)
		self.assertEqual(self.models.headerDefinition.id, None)
		self.assertEqual(self.models.header.id, None)
	def test_setModels(self):
		self.test_hchecker()
		self.models = SetModels()
		setCamera(self.models.camera, self.data, self.check)
		self.assertEqual(self.models.camera.instrument, 'OSIRIS')
		setObservationMode(self.models.observationMode,self.data,self.models.camera, self.check)
		self.assertEqual(self.models.observationMode.mode, 'OsirisBroadBandImage')
		setFrame(self.models.frame,self.data,self.check,self.models.camera, self.models.observationMode)
		self.assertEqual(self.models.frame.programId, 999) 
		self.models.headerDefinition.id = 1
		self.assertEqual(self.models.frame.observationDate, '2009-04-18T20:14:00')
		headerDefList = [self.data[0]['OBSMODE'][1],'OBSMODE',\
    	'STRING',self.models.camera]
		setHeaderDefinition(self.models.headerDefinition, headerDefList)
		self.assertEqual(self.models.headerDefinition.name, 'OBSMODE')
		self.assertEqual(self.models.headerDefinition.dataType, 'STRING')
if __name__ == '__main__':
	from astropy.io import fits
	import models
	from controllers_v4 import CameraDAO, ObservationModeDAO, FrameDAO, \
	HeaderDefinitionDAO, HeaderDAO, setCamera, setObservationMode,setFrame,\
	setHeaderDefinition, setHeader, InitDAOsAndDB, SetModels, getDataFitsImages,Checker
	from datetime import datetime
	import time
	import logging
	logging.disable(logging.CRITICAL)
	unittest.main()