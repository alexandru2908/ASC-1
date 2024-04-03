import os
import json
import pandas as pd
from flask import jsonify

class DataIngestor:
    def __init__(self, csv_path: str):
        # TODO: Read csv from csv_path
        
        

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]
        
        
        self.content = pd.read_csv(csv_path)
        
       
        #print header 
        # print(content.columns)
        
    def get_state_data(self, data):
        # return self.content[self.content['LocationDesc'] == state and "Obesity" in self.content['Class']]  
        # obesity = self.content[self.content['Class'].str.contains('Obesity')]
        # return jsonify({"status": "done", "data": "ceva"})
        
        
        # return obesity[self.content['LocationDesc'] == state]
        # return  self.content[ self.content['Class'] and self.content['LocationDesc'] == state]
        
        
        
        
        