from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx_config import get_chart_type  

import seaborn as sns
import matplotlib.pyplot as plt
import tempfile


# Function to get the chart type object from a string
class ChartHandler:
    def __init__(self, slide_idx, chartConfig, dataGenerator):
    # self.config = self.config_to_dict(config_path)
        print(chartConfig)
        dataGenerator.register_filters(slide_idx, chartConfig)
        chartIdx= chartConfig['Location']
        chartDataNameRef= chartConfig['DataNameRef']

        self.chartType = chartConfig['Type']
        self.measure = chartConfig['Measure']
        self.dimension = chartConfig['Dimension']

        self.data = dataGenerator.get_data(slide_idx, chartIdx, chartDataNameRef)
        return


    def insertChart(self, placeholder):
        plt.figure()

        dimension = self.dimension
        measure = self.measure
        data = self.data

        complex_plot = None
        if self.chartType == 'bar':
            sns.barplot(x=dimension, y=measure, data=data)
        elif self.chartType == 'line':
            sns.lineplot(x=dimension, y=measure, data=data)
        elif self.chartType == 'scatter':
            sns.scatterplot(x=dimension, y=measure, data=data)
        elif self.chartType == 'box':
            sns.boxplot(x=dimension, y=measure, data=data)
        elif self.chartType == 'violin':
            sns.violinplot(x=dimension, y=measure, data=data)
        elif self.chartType == 'hist':
            sns.histplot(data=data, x=measure, hue=dimension, multiple="stack")
        elif self.chartType == 'strip':
            sns.stripplot(x=dimension, y=measure, data=data)
        elif self.chartType == 'swarm':
            sns.swarmplot(x=dimension, y=measure, data=data)
        elif self.chartType == 'kde':
            sns.kdeplot(data=data, x=measure, hue=dimension, fill=True)
        elif self.chartType == 'count':
            sns.countplot(x=dimension, data=data)
        elif self.chartType == 'lm':
            sns.lmplot(x=dimension, y=measure, data=data)
            complex_plot = 'lm'
        elif self.chartType == 'pairplot':
            sns.pairplot(data)
            complex_plot = 'pairplot'
        else:
            raise ValueError(f"Unsupported chart_type: {self.chartType}")

        plt.title(f'{measure} by {dimension}')
        # plt.tight_layout()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:    
            if complex_plot:
                plt.close()  # Close original
                plt.figure()  # Dummy figure to avoid issues
                # For pairplot/lmplot which create their own fig
                plot = sns.pairplot(data) if self.chartType == 'pairplot' else sns.lmplot(x=dimension, y=measure, data=data)
                plot.savefig(tmpfile.name)
            else:
                plt.title(f'{self.chartType.capitalize()} plot of {measure} by {dimension}')
                plt.tight_layout()
                plt.savefig(tmpfile.name)
                plt.close()
            img_path = tmpfile.name


        placeholder.insert_picture(img_path)

    def insertExcelChart(self,placeholder):
    # Formatting based on the chart type
        chart_type = get_chart_type(self.chartType)
        chart_data = CategoryChartData()
        
        chart_data.categories = self.data[self.dimension]
        chart_data.add_series(self.measure, (self.data[self.measure].tolist()))  # Multiply by 100 to convert to percentage

    
        chart_frame = placeholder.insert_chart(chart_type, chart_data)
        chart = chart_frame.chart

        if chart_type in (XL_CHART_TYPE.BAR_CLUSTERED, XL_CHART_TYPE.COLUMN_CLUSTERED, XL_CHART_TYPE.LINE_MARKERS):
            for series in chart.series:
                fill = series.format.fill
                fill.solid()
                # fill.fore_color.rgb = RGBColor(0x14, 0x60, 0x82)  # Default blue color

                # Add data labels formatted as percentages with no decimal points
                series.has_data_labels = True
                for point in series.points:
                    # point.data_label.number_format = '0%'
                    point.data_label.font.size = Pt(10)
                    point.data_label.font.color.rgb = RGBColor(0x00, 0x00, 0x00)  # Black font color
                    
                # Remove the chart title and legend
                chart.has_title = False
                chart.has_legend = False

                # Remove the chart axis
                chart.value_axis.visible = False
                chart.category_axis.visible = True

            # Remove gridlines for all charts
            if chart.category_axis and chart.category_axis.has_major_gridlines:
                chart.category_axis.major_gridlines.format.line.fill.background()

            if chart.value_axis and chart.value_axis.has_major_gridlines:
                chart.value_axis.major_gridlines.format.line.fill.background()

        return
