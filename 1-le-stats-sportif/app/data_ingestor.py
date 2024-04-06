import os
import json
import pandas as pd
from flask import jsonify
import csv

class DataIngestor:
    def __init__(self, csv_path: str):
        # TODO: Read csv from csv_path
        
        pd.options.display.max_rows = 999999
        
        

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

        
    def get_states_data(self, data):
        
        data_question = self.content[self.content['Question'] == data["question"]]
        states = set(data_question['LocationDesc'])
        
        result = {}
        states_appearance = {}
        
        for i in states:
            result[i] = 0
            states_appearance[i] = 0
        
        for i in range(len(data_question)):
            result[data_question.iloc[i]['LocationDesc']] += data_question.iloc[i]['Data_Value']
            states_appearance[data_question.iloc[i]['LocationDesc']] += 1
        
        for key, value in result.items():
            result[key] = value / states_appearance[key]
        
        result_sorted = dict(sorted(result.items(), key=lambda x:x[1]))
        return json.dumps(result_sorted)

    
    

    def get_state_data(self, data):
        data_question = self.content[self.content['Question'] == data["question"]]
        state = data["state"]
        
        result = {data["state"]: 0}
        state_appearance = 0
        l = []
        for i in data_question.iterrows():
            if i[1]['LocationDesc'] == state:
                l.append(i[1]['Data_Value'])
                result[state] += i[1]['Data_Value']
                state_appearance += 1
                
        result[state] = result[state] / state_appearance
        with open("logs.txt", "w") as f:
            f.write(str(l))
        
        
        return json.dumps(result)
    
    def best_5(self, data):
        res = self.get_states_data(data)
        res_json = json.loads(res)
        list_res = list(res_json.items())
        if data["question"] in self.questions_best_is_max:
            list_res = sorted(list_res, key=lambda x: x[1],reverse=True)
        
        return json.dumps(dict(list_res[:5]))
    
    
    def worst_5(self, data):
        res = self.get_states_data(data)
        res_json = json.loads(res)
        list_res = list(res_json.items())
        
        if data["question"] in self.questions_best_is_min:
            list_res = sorted(list_res, key=lambda x: x[1],reverse=True)
        
        return json.dumps(dict(list_res[:5]))
    
    
    
    def global_mean(self, data):
        data_question = self.content[self.content['Question'] == data["question"]]
        return json.dumps({"global_mean": data_question['Data_Value'].mean()})
    
            
        
        
        
        
        
        
        
        
        
        
        
        