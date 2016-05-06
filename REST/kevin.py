from restV3 import *
server = Server(Credencials('test','test'))
criterias = []
criterias.append(ObservationBlockCriteria('0006'))
criterias.append(ProgramCriteria('GTC40-14A'))
criterias.append(AndOperator())
criterias.append(DateCriteria('2014-06-01','2014-06-27'))
criterias.append(AndOperator())
server.query(CriteriaBuilder(criterias), 100, 0)

frames = server.results.frame

for frame in frames:
	if frame.isRaw=='1':
		print frame.path
		for keyword in frame.fitsKeywords:
			try:
				print keyword.fitsKeywordDef.name,
				if keyword.fitsKeywordDef.dataType=='STRING':
					print keyword.stringVal,
				if keyword.fitsKeywordDef.dataType=='DOUBLE':
					print keyword.doubleVal,
				if keyword.fitsKeywordDef.dataType=='LONG':
					print keyword.longVal,
				print keyword.fitsKeywordDef.comment
			except AttributeError:
				pass

