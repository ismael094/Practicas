from restV3 import *
server = Server(Credencials('test','test'))
criterias = []
criterias.append(ObservationBlockCriteria('0006'))
criterias.append(ProgramCriteria('GTC40-14A'))
criterias.append(AndOperator())
criterias.append(DateCriteria('2014-06-01','2014-06-27'))
criterias.append(AndOperator())
server.query(CriteriaBuilder(criterias), 100, 0)

frames = server.results.getFrames()
frameByIndex = server.results.getFrameByIndex(2)
frameWithHeaderList = server.results.getHeaderList(6, ['INSTRUME', 'PI'])

