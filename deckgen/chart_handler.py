import seaborn as sns
import matplotlib.pyplot as plt
from custom_charts.custom import custom
from charts.default import charts


# Function to get the chart type object from a string
class ChartHandler:
    def __init__(self, slide_idx, chartConfig, dataGenerator):
        print(chartConfig)
        self.chartConfig = chartConfig
       
        self.chartType = chartConfig['Type']
        self.size = eval(chartConfig['Size'])
        self.args = chartConfig['Args']
        chartIdx= chartConfig['Location']
        chartDataNameRef= chartConfig.get('DataNameRef', -1) 

        dataGenerator.register_filters(slide_idx, chartConfig)
        self.data = dataGenerator.get_data(slide_idx, chartIdx, chartDataNameRef)

        return


    def insertChart(self, placeholder):
       
        if self.chartType == "custom":
            customChartObj = custom[self.args['chartType']]()
            customChartObj.add_data(data=self.data)
            customChartObj.prep_args(size=self.size,  **self.args)
            img_path = customChartObj.plot()

        else:
            chartObj = charts[self.chartType]()
            chartObj.add_data(data=self.data)
            chartObj.prep_args(size=self.size, chartType=self.chartType, **self.args)
            img_path = chartObj.plot()
        
        
        placeholder.insert_picture(img_path)
        return
   

if __name__ == '__main__':    
    print(custom)