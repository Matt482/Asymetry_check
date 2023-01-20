import unittest

import helpers
import main


class TestCurrencyConversion(unittest.TestCase):

    def test_get_data_identifier_url(self):
        self.assertEqual("https://sdw-wsrest.ecb.europa.eu/service/data/BSI/M.A.I8.W1.S1T.S1A.T.N.FA.F.F7.T.EUR._T.T.N?detail=dataonly",
                         helpers.get_data_identifier_url("M.A.I8.W1.S1T.S1A.T.N.FA.F.F7.T.EUR._T.T.N"))
        self.assertEqual("https://sdw-wsrest.ecb.europa.eu/service/data/BSI/M.N.I8.W1.S1Q.S1.T.N.FA.F.F7.T.GBP._T.T.N?detail=dataonly",
                         helpers.get_data_identifier_url("M.N.I8.W1.S1Q.S1.T.N.FA.F.F7.T.GBP._T.T.N"))
        self.assertEqual("https://sdw-wsrest.ecb.europa.eu/service/data/BSI/M.N.I8.W1.S1P.S1Q.T.N.FA.F.F7.T.EUR._T.T.N?detail=dataonly",
                         helpers.get_data_identifier_url("M.N.I8.W1.S1P.S1Q.T.N.FA.F.F7.T.EUR._T.T.N"))

    def test_get_transactions(self):
        df = main.get_transactions("Q.DE.N.A.A20.A.1.AT.2000.Z01.E")
        time = df['TIME_PERIOD']
        value = df['OBS_VALUE']
        ident = df['IDENTIFIER']
        def checking(df_time, df_value, df_ident):
            if df_time[0] == "2012-Q2" and df_value[0] == 14001:
                return True
            if df_time[1] == "2012-Q3" and df_value[1] == 13568:
                return True
            if df_ident[0] == "Q.DE.N.A.A20.A.1.AT.2000.Z01.E":
                return True

        self.assertTrue(checking(time, value, ident))

    def test_get_symmetric_identifier(self):

        self.assertEqual("Q.AT.A.N.A20.A.1.HR.2000.Z01.E",
                         main.get_symmetric_identifier("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {1: 7, 2: 3}))
        self.assertEqual("Q.HR.N.A20.A.1.A.AT.2000.Z01.E",
                         main.get_symmetric_identifier("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {3: 4, 5: 6}))
        self.assertEqual("Q.N.HR.A20.A.A.1.2000.AT.Z01.E",
                         main.get_symmetric_identifier("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {1: 2, 3: 4, 7: 8}))
        self.assertNotEqual("Q.N.HR.A20.A.A.1.2000.AT.Z01.E",
                         main.get_symmetric_identifier("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {3: 4, 1: 5}))
        self.assertNotEqual("Q.N.HR.A20.A.A.1.2000.AT.Z01.E",
                         main.get_symmetric_identifier("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {7: 1, 8: 3}))

    def test_get_asymmetries(self):
        df = main.get_asymmetries("Q.HR.N.A.A20.A.1.AT.2000.Z01.E", {1: 7})

        prov_id = df['PROVIDED_ID']
        symm_id = df['SYMMETRIC_ID']
        delta = df['DELTA']

        def checking(provided_id, symmetric_id, delta):
            if delta[2] == 9036.2925:
                return True
            if delta[2] == 8809.512144:
                return True
            if provided_id[0] == "Q.HR.N.A.A20.A.1.AT.2000.Z01.E":
                return True

        self.assertTrue(checking(prov_id, symm_id, delta))


if __name__ == '__main__':
    unittest.main()
