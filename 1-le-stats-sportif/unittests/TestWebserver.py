import unittest
import os
# from app import data_ingestor as data_ingestor
from app import DataIngestor
import json

ONLY_LAST = False

class TestWebServer(unittest.TestCase):
    
    def setUp(self):
        self.obj = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
        
    
    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_states_mean(self):
        question = {"question": "Percent of adults aged 18 years and older who have an overweight classification"}
        result = self.obj.get_states_data(question)
        res = str("\"District of Columbia\": 30.746875")
        self.assertTrue( res in result)
        
    
    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_state_mean(self):
        question = {"question": "Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)", "state": "Guam"}
        result = self.obj.get_state_data(question)
        res = "Guam"
        self.assertTrue(res in result)
        
    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_best5(self):
        question = {"question": "Percent of adults aged 18 years and older who have an overweight classification"}
        result = self.obj.best_5(question)
        res = str("\"District of Columbia\": 30.746875")
        self.assertTrue(res in result)
    
        
    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_worst5(self):
        question = {"question": "Percent of adults aged 18 years and older who have an overweight classification"}
        result = self.obj.worst_5(question)
        res = str("Puerto Rico")
        self.assertTrue(res in result)
        
    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_global_mean(self):
        
        question = {"question": "Percent of adults aged 18 years and older who have an overweight classification"}
        result = self.obj.global_mean(question)
        res = str("34.482761415833565")
        self.assertTrue(res in result)
        
    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_diff_from_mean(self):
        question = {"question": "Percent of adults aged 18 years and older who have an overweight classification"}
        result = self.obj.diff_from_mean(question)
        res = str("\"District of Columbia\": 3.7358864158335656")
        self.assertTrue(res in result)
        
    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_state_diff_from_mean(self):
        question = {"question": "Percent of adults who report consuming vegetables less than one time daily", "state": "Virgin Islands"}
        result = self.obj.diff_from_mean_state(question)
        res = str("dummy")
        self.assertFalse(res in result)
        
    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_mean_by_category(self):
        question = {"question": "Percent of adults aged 18 years and older who have an overweight classification"}
        result = self.obj.mean_by_category(question)
        self.assertTrue ("\"('Alabama', 'Age (years)\', '18 - 24')\": 24.9" in result)
        self.assertFalse ("\"('Alabama', 'Age (years)', '18 - 24')\": 13.8" in result)
        
    @unittest.skipIf(ONLY_LAST, "Checking only the last added test")
    def test_state_mean_by_category(self):
        question = {"question": "Percent of adults aged 18 years and older who have an overweight classification", "state": "Oklahoma"}
        result = self.obj.mean_by_category_state(question)
        self.assertTrue("\"('Race/Ethnicity', 'Other')\": 34.5" in result)
        
    
if __name__ == '__main__':
    unittest.main()