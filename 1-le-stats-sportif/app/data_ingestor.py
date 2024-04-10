"""
Used to ingest data from a csv file and provide various methods to extract data from the csv file
"""

import json
import time
import logging
import logging.handlers
import pandas as pd




class DataIngestor:
    def __init__(self, csv_path: str):
        # initializing the logger
        pd.options.display.max_rows = 999999
        self.logger = logging.handlers.RotatingFileHandler("webserver.log", maxBytes=10000, backupCount=10)
        self.logger.setFormatter(logging.Formatter("%(asctime)s - %(message)s", "%Y-%m-%d %H:%M:%S"))
        self.logger.time = time.gmtime()
        self.logger1 = logging.getLogger("webserver")
        self.logger1.addHandler(self.logger)
        self.logger1.setLevel(logging.INFO)
        self.logger1.info("webserver started")
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
        """
        Method which extracts the data for a specific question and returns the mean value all states
        """
        data_question = self.content[self.content['Question'] == data["question"]]
        states = set(data_question['LocationDesc'])
        self.logger1.info("get_states_data called" + str(data))
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
        result_sorted = dict(sorted(result.items(), key=lambda x: x[1]))
        return json.dumps(result_sorted)

    def get_state_data(self, data):
        """
        Extracting the data for a specific question and state
        """
        self.logger1.info("get_state_data called" + str(data))
        data_question = self.content[self.content['Question'] == data["question"]]
        state = data['state']
        result = {state: 0}
        state_appearance = 0
        for i in data_question.iterrows():
            if i[1]['LocationDesc'] == state:
                result[state] += i[1]['Data_Value']
                state_appearance += 1
        result[state] = result[state] / state_appearance
        return json.dumps(result)
    def best_5(self, data):
        """
        Extracting the best mean for 5 states for a specific question
        """
        self.logger1.info("best_5 called" + str(data))
        res = self.get_states_data(data)
        res_json = json.loads(res)
        list_res = list(res_json.items())
        if data["question"] in self.questions_best_is_max:
            list_res = sorted(list_res, key=lambda x: x[1], reverse=True)
        return json.dumps(dict(list_res[:5]))
    def worst_5(self, data):
        """
        Extracting the worst mean for 5 states for a specific question
        """
        self.logger1.info("worst_5 called" + str(data))
        res = self.get_states_data(data)
        res_json = json.loads(res)
        list_res = list(res_json.items())
        if data["question"] in self.questions_best_is_min:
            list_res = sorted(list_res, key=lambda x: x[1], reverse=True)
        return json.dumps(dict(list_res[:5]))
    def global_mean(self, data):
        """
        Extracting the mean for a specific question
        """
        self.logger1.info("global_mean called" + str(data))
        data_question = self.content[self.content['Question'] == data["question"]]
        return json.dumps({"global_mean": data_question['Data_Value'].mean()})
    def diff_from_mean(self, data):
        """
        Extracing the difference from the global mean for all states
        """
        self.logger1.info("diff_from_mean called" + str(data))
        states_mean = self.get_states_data(data)
        states_mean_json = json.loads(states_mean)
        global_mean = self.global_mean(data)
        global_mean_json = json.loads(global_mean)
        for key, value in states_mean_json.items():
            states_mean_json[key] = global_mean_json['global_mean'] - value
        return json.dumps(states_mean_json)
    def diff_from_mean_state(self, date):
        """
        Extracting the difference from the global mean for a specific state
        """
        self.logger1.info("diff_from_mean_state called" + str(date))
        state_mean = self.get_state_data(date)
        state_mean_json = json.loads(state_mean)
        global_mean = self.global_mean(date)
        global_mean_json = json.loads(global_mean)
        return json.dumps({date["state"]: global_mean_json["global_mean"] - state_mean_json[date["state"]]})
    def mean_by_category(self, data):
        """
        Extracting the mean for a specific question and stratification category for all states
        """
        self.logger1.info("mean_by_category called" + str(data))
        data_question = self.content[self.content['Question'] == data["question"]]
        states = set(data_question['LocationDesc'])
        result = {}
        count = {}
        states = sorted(states)
        for i in states:
            data_state = data_question[data_question['LocationDesc'] == i]
            stratification = set(data_state['StratificationCategory1'])
            for j in stratification:
                data_stratification = data_state[data_state['StratificationCategory1'] == j]
                for k in data_stratification.iterrows():
                    tup = (i, j, k[1]['Stratification1'])
                    if str(tup) not in result:
                        result[str(tup)] = k[1]['Data_Value']
                    else:
                        result[str(tup)] += k[1]['Data_Value']
                    if str(tup) not in count:
                        count[str(tup)] = 1
                    else:
                        count[str(tup)] += 1
        for key, value in result.items():
            result[key] = value / count[key]
        return json.dumps(result)
    def mean_by_category_state(self, data):
        """
        Extracting the mean for a specific question, state and stratification category
        """
        self.logger1.info("mean_by_category_state called" + str(data))
        data_question = self.content[self.content['Question'] == data["question"]]
        data_state = data_question[data_question['LocationDesc'] == data["state"]]
        data_stratification_set = set(data_state['Stratification1'])
        state = data['state']
        stratification = {}
        stratification[state] = {}
        count_stratification = {}
        count_stratification[state] = {}
        for i in data_stratification_set:
            for j in data_state.iterrows():
                if j[1]['Stratification1'] == i:
                    tup = (j[1]['StratificationCategory1'], i)
                    if str(tup) not in stratification[state]:
                        stratification[state][str(tup)] = j[1]['Data_Value']
                    else:
                        stratification[state][str(tup)] += j[1]['Data_Value']
                    if str(tup) not in count_stratification[state]:
                        count_stratification[state][str(tup)] = 1
                    else:
                        count_stratification[state][str(tup)] += 1
        for key, value in stratification[state].items():
            stratification[state][key] = value / count_stratification[state][key]
        return json.dumps(stratification)
    