import unittest
from restV3 import *
class TestStringMethods(unittest.TestCase):
    def exception(self):
        pass
    def test_user(self):
        a = Credencials('test','test')
        self.assertEqual(a.user, 'test')

    def test_dateCriteria(self):
        a = DateCriteria('2014-06-01','2014-06-27')
        self.assertEqual(a.init, '2014-06-01')
        self.assertEqual(a.end, '2014-06-27')
        self.assertEqual(a.build(),'{"type": "datecriteria","end":"2014-06-27 12:00:00","init":"2014-06-01 12:00:00"}')

    def test_programCriteria(self):
        a = ProgramCriteria('GTC40-14A')
        self.assertEqual(a.programId, 'GTC40-14A')
        self.assertEqual(a.build(),'{"type":"programidcriteria","programID":"GTC40-14A"}')
    def test_obBlockCriteria(self):
        a = ObservationBlockCriteria('0006')
        self.assertEqual(a.observationBlock, '0006')
        self.assertEqual(a.build(),'{"type":"observationblockidcriteria","observationBlockID":"0006"}')
    def test_andOperator(self):
        a = AndOperator()
        self.assertEqual(a.build(), '{"type":"operatorcriteria","operator":"AND"}')
    def test_criterias(self):
        criterias = [DateCriteria('2014-06-01','2014-06-27'),ProgramCriteria('GTC40-14A'),AndOperator(),ObservationBlockCriteria('0006'),AndOperator()]
        self.assertEqual(CriteriaBuilder(criterias).reCheck, 'True')
        criterias = [DateCriteria('2014-06-01','2014-06-27'),ProgramCriteria('GTC40-14A'),AndOperator(),ObservationBlockCriteria('0006')]
        try:
            CriteriaBuilder(criterias)
            self.fail('Error in the criterias') 
        except Exception:
            pass

    def test_results(self):
        criterias = [DateCriteria('2014-06-01','2014-06-27'),ProgramCriteria('GTC40-14A'),AndOperator(),ObservationBlockCriteria('0006'),AndOperator()]
        self.server = Server(Credencials('test','test'))
        self.server.query(CriteriaBuilder(criterias), 100, 0)
        self.assertEqual(len(self.server.results.frame),13)
        self.assertEqual(str(self.server.results.frame[0]['programId']),'GTC40-14A')
        a = self.server.results.getFrameByIndex(0)
        self.assertEqual(int(a.id), 676568)
        headers = ['INSTRUME', 'OBSMODE', 'PI']
        a = self.server.results.getHeaderList(0,headers)
        for item in a.fitsKeywords:
            if item.fitsKeywordDef.name in headers:
                pass
            else:
                self.fail('Error in getFramesByHeadersList '+item.fitsKeywordDef.name+' is not in the headers list') 

if __name__ == '__main__':
    unittest.main()