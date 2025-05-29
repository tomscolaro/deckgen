from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx_config import get_chart_type  

import seaborn as sns
sns.color_palette("crest", as_cmap=True)
import matplotlib.pyplot as plt
import tempfile
import polars as pl
from great_tables import GT, md, html


# Function to get the chart type object from a string
class ChartHandler:
    def __init__(self, slide_idx, chartConfig, dataGenerator):
    # self.config = self.config_to_dict(config_path)
        print(chartConfig)
        self.palette ='magma'

        self.chartType = chartConfig['Type']

        if self.chartType == 'image':
              self.chartPath = chartConfig['ImagePath']
              self.size = eval(chartConfig['Size'])
        else:
            if self.chartType == 'table':
                self.chartSubTitle = chartConfig['Subtitle']

            dataGenerator.register_filters(slide_idx, chartConfig)
            chartIdx= chartConfig['Location']
            chartDataNameRef= chartConfig['DataNameRef']

      
            self.measure = chartConfig['Measure']
            self.dimension = chartConfig['Dimension']
            self.size = eval(chartConfig['Size'])

            self.data = dataGenerator.get_data(slide_idx, chartIdx, chartDataNameRef)

        self.containsSecondAxis = chartConfig.get('SecondaryMeasure', None) != None
        if self.containsSecondAxis:
            # self.secondaryDim =  chartConfig['SecondaryDimension']
            self.secondaryMeasure =  chartConfig['SecondaryMeasure']


        return


    def insertChart(self, placeholder):
       
        # plt.figure()
        if self.chartType == 'image':
            placeholder.insert_picture(self.chartPath, )
            return

        dimension = self.dimension
        measure = self.measure
        data = self.data

        complex_plot = None
        table_plot = None

        ax = sns.set_style(style=None, rc=None )

        fig, ax = plt.subplots(figsize=self.size)




        if self.chartType == 'bar':
            sns.barplot(x=dimension, y=measure, data=data, palette=self.palette, ax=ax)
        elif self.chartType == 'line':
            sns.lineplot(x=dimension, y=measure, data=data, palette=self.palette, ax=ax)
        elif self.chartType == 'scatter':
            sns.scatterplot(x=dimension, y=measure, data=data, palette=self.palette, ax=ax)
        elif self.chartType == 'box':
            sns.boxplot(x=dimension, y=measure, data=data, palette=self.palette, ax=ax)
        elif self.chartType == 'violin':
            sns.violinplot(x=dimension, y=measure, data=data, palette=self.palette, ax=ax)
        elif self.chartType == 'hist':
            sns.histplot(data=data, x=measure, hue=dimension, multiple="stack", palette=self.palette, ax=ax)
        elif self.chartType == 'strip':
            sns.stripplot(x=dimension, y=measure, data=data, palette=self.palette, ax=ax)
        elif self.chartType == 'swarm':
            sns.swarmplot(x=dimension, y=measure, data=data, palette=self.palette, ax=ax)
        elif self.chartType == 'kde':
            sns.kdeplot(data=data, x=measure, hue=dimension, fill=True, palette=self.palette, ax=ax)
        elif self.chartType == 'count':
            sns.countplot(x=dimension, data=data, palette=self.palette, ax=ax)
        elif self.chartType == 'lm':
            sns.lmplot(x=dimension, y=measure, data=data, palette=self.palette, ax=ax)
            complex_plot = 'lm'
        elif self.chartType == 'pairplot':
            sns.pairplot(data, palette=self.palette, ax=ax)
            complex_plot = 'pairplot'


        elif self.chartType == 'table':
            # sns.pairplot(data, palette=self.palette)
            data = pl.from_pandas(data).sort(measure, descending=True).head(10)
            gt_tbl = GT(data).tab_header(
                title="Top {} by {}".format(dimension, measure),
                # subtitle=""
            )
            table_plot = True
        
        else:
            raise ValueError(f"Unsupported chart_type: {self.chartType}")

        if self.containsSecondAxis:
            ax2 = ax.twinx()
            sns.lineplot(data = data, x=dimension, y=self.secondaryMeasure, palette=self.palette, alpha=0.8, ax=ax2)



        plt.title(f'{measure} by {dimension}')
        # plt.tight_layout()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:    
            if complex_plot:

                plt.close()  # Close original
                plt.figure(self.size)  # Dummy figure to avoid issues
                # plt.tight_layout()
                # For pairplot/lmplot which create their own fig
                plt.tight_layout(pad=3.0) 
                plot = sns.pairplot(data) if self.chartType == 'pairplot' else sns.lmplot(x=dimension, y=measure, data=data)
                plot.savefig(tmpfile.name)
            
            elif table_plot :
                gt_tbl.save(file=tmpfile.name, web_driver='firefox', window_size=(4000,2000 ))
                # gt_tbl.save(file="test.png", web_driver='edge', window_size=(1000,1000))
            else:
                plt.title(f'{self.chartType.capitalize()} plot of {measure} by {dimension}')
                plt.tight_layout(pad=3.0)
                plt.savefig(tmpfile.name)
                plt.close()


            img_path = tmpfile.name


        placeholder.insert_picture(img_path)

   