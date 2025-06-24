
import pandas as pd
import  numpy as np
from datetime import datetime, timedelta
from collections import defaultdict

from utils import read_csvs_to_dfs


class DataGenerator:
    def __init__(self):
        self.filters = {}

    def get_data(self, slide, chart, dataName='Data'):
        if dataName == -1:
            return 
        data  = self.data[dataName]      
        query_str = self._generate_query_str(slide, chart)
        
        if query_str:
            data = data.query(query_str)
    
        return data


    def _generate_query_str(self, slide, chart):
        filter_str = ''
        print("Generate Query Str: Filter Dict {}".format(self.filters[slide][chart]))

        for  hold in self.filters[slide][chart]:

            for idx, filter_dict in enumerate(hold.get('AND', [])):
                filter_lines = len(hold.get('AND', []))

                match filter_dict['Type']:
                    case "=":
                        filter_str += filter_dict['Column'] + ' == "{}"'.format(filter_dict['Value'])
                    case "!=":
                        filter_str += filter_dict['Column'] + ' != "{}"'.format(filter_dict['Value'])
                    case ">=":
                        filter_str += filter_dict['Column'] + ' >= "{}"'.format(filter_dict['Value'])
                    case "<=":
                        filter_str += filter_dict['Column'] + ' <= "{}"'.format(filter_dict['Value'])

                
                if idx < (filter_lines-1):
                    filter_str += ' & '

            if hold.get('OR'):
                filter_str += '&'

            for idx, filter_dict in enumerate(hold.get('OR', [])):
                filter_lines = len(hold.get('OR', []))
                
                match filter_dict['Type']:
                    case "=":
                        filter_str += filter_dict['Column'] + ' ==  "{}"'.format(filter_dict['Value'])
                    case "!=":
                        filter_str += filter_dict['Column'] + ' != "{}"'.format(filter_dict['Value'])
                    case ">=":
                        filter_str += filter_dict['Column'] + ' >= "{}"'.format(filter_dict['Value'])
                    case "<=":
                        filter_str += filter_dict['Column'] + ' <= "{}"'.format(filter_dict['Value'])


                if idx < (filter_lines- 1):
                    filter_str += ' | '


        print("Filter Str {}".format(filter_str))
        return filter_str

    def register_filters(self, slideIdx, chart_config):
        filterConfig = defaultdict(list)
        for filter in chart_config.get('Filters', []):
            chart_no = chart_config.get(
                'Location', -1
            )

            if chart_no != -1:
                filterConfig[chart_no].append(filter)

        self.filters[slideIdx] = filterConfig
        return
    

class CsvDataGenerator(DataGenerator):
    def __init__(self, data_config ):
        super().__init__()
        print("Reading in your CSV file. Hang Tight.")
        print("Processing DataFrame.. One Moment..")
        self.data = read_csvs_to_dfs(data_config)


class TestDataGenerator(DataGenerator):
    def __init__(self, dataName='TestData', num_cats=1, num_measures=1, num_personas=3, rows=100, include_timeseries=False):
        super().__init__()

        self.num_cats = num_cats
        self.num_measures = num_measures

        self.num_personas = num_personas
        self.num_rows = rows
        self.include_timeseries = include_timeseries

        self.data = { dataName:self._generate_data()
                     }

    def _generate_data(self):    
        # Generate category columns
        data = {}
        for i in range(self.num_cats):
            data[f'cat_{i}'] = np.random.choice([f'group_{j}' for j in range(self.num_personas)], size=self.num_rows)

        # Generate measure columns
        for i in range(self.num_measures):
            data[f'measure_{i}'] = np.random.randn(self.num_rows) * 100

        # Optionally include a timeseries
        if self.include_timeseries:
            start_time = datetime.now()
            data['timestamp'] = [start_time + timedelta(minutes= np.random.randint(10, 10000) * i) for i in range(self.num_rows)]

        return pd.DataFrame(data)

if __name__ == '__main__':
    generator = TestDataGenerator(num_cats=2, num_measures=3, num_personas=10, rows=1000, include_timeseries=True)
    df = generator.get_data('TestData')
    print(df.head())
    print("############################################################################################")
    generator = TestDataGenerator(num_cats=2, num_measures=3, include_timeseries=True)
    df = generator.get_data('TestData')

    df.to_csv('test/test.csv', index=False)

    print(df.head())