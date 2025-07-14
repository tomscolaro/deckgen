
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile
import polars as pl
from great_tables import GT, md, html


class DefaultChart:
    def __init__(self):
        self.data = None
        self.palette ='magma'
        self.chartType = None
        return
    
    def add_data(self, data=-1):
        self.data = data

    def prep_args(self, **kwargs):
        self.chartType = kwargs['chartType']
        self.measure = kwargs['measure']
        self.dimension = kwargs['dimension']

        self.second_measure = kwargs.get('second_measure', None)
        self.palette = kwargs.get('palette', 'magma')

        self.ax = sns.set_style(style=None, rc=None )
        self.fig, self.ax = plt.subplots(figsize= kwargs['size'])
        return 
    
    def save_file(self):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:   
            if self.chartType:
                plt.title(f'{self.chartType.capitalize()} plot of {self.measure} by {self.dimension}')
            # plt.tight_layout(pad=3.0)
            plt.gcf().set_size_inches(5, 2)
            plt.savefig(tmpfile.name, dpi=400, bbox_inches='tight', pad_inches=1.5)
            plt.close()
            image_path = tmpfile.name
        return image_path

    def plot_second_axis(self):
        self.ax2 = self.ax.twinx()
        sns.lineplot(data = self.data, x=self.dimension, y=self.second_measure, palette=self.palette, alpha=0.8, ax=self.ax2)

        return
    
class BarPlot(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()

    def plot(self, **kwargs):
        sns.barplot(x=self.dimension, y=self.measure, data=self.data, palette=self.palette, ax=self.ax)

        if self.second_measure:
            self.plot_second_axis()

        image_path = self.save_file()
        return image_path

class Table(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()

    def plot(self, **kwargs):
            # sns.pairplot(data, palette=self.palette)
        self.data = pl.from_pandas(self.data).sort(self.measure, descending=True).head(10)
        gt_tbl = GT(self.data).tab_header(
            title="Top {} by {}".format(self.dimension, self.measure),
            # subtitle=""
        )

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:   
            gt_tbl.save(file=tmpfile.name, web_driver='firefox', window_size=(4000,2000 ))

        return tmpfile.name

class LinePlot(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()

    def plot(self, **kwargs):
        #include double axis logic
        sns.lineplot(x=self.dimension, y=self.measure, data=self.data, palette=self.palette, ax=self.ax)
        if self.second_measure:
            self.plot_second_axis()


        image_path = self.save_file()
        return image_path

class ScatterPlot(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()

    def plot(self, **kwargs):

         
        sns.scatterplot(x=self.dimension, y=self.measure, data=self.data, palette=self.palette, ax=self.ax)
        if self.second_measure:
            self.plot_second_axis()

        image_path = self.save_file()

        return image_path

class BoxPlot(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()

    def plot(self, **kwargs):
        sns.boxplot(x=self.dimension, y=self.measure, data=self.data, palette=self.palette, ax=self.ax)        
        if self.second_measure:
            self.plot_second_axis()


        image_path = self.save_file()
        return image_path

class ViolinPlot(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()

    def plot(self, **kwargs):
        sns.violinplot(x=self.dimension, y=self.measure, data=self.data, palette=self.palette, ax=self.ax)
    
        image_path = self.save_file()
        return image_path

class HistPlot(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()

    def plot(self, **kwargs):
   
        sns.histplot(data=self.data, x=self.measure, hue=self.dimension, multiple="stack", palette=self.palette, ax=self.ax)
        if self.second_measure:
            self.plot_second_axis()

        image_path = self.save_file()
        return image_path

class StripPlot(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()

    def plot(self, **kwargs):   
        sns.stripplot(x=self.dimension, y=self.measure, data=self.data, palette=self.palette, ax=self.ax) 
        image_path = self.save_file()
        return image_path
        
class SwarmPlot(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()

    def plot(self, **kwargs): 
        sns.swarmplot(x=self.dimension, y=self.measure, data=self.data, palette=self.palette, ax=self.ax)
        image_path = self.save_file()

        return image_path

class KdePlot(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()

    def plot(self, **kwargs):
        sns.kdeplot(data=self.data, x=self.measure, hue=self.dimension, fill=True, palette=self.palette, ax=self.ax) 
        image_path = self.save_file()
        return image_path

class CountPlot(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()

    def plot(self, **kwargs): 
        sns.countplot(x=self.dimension, data=self.data, palette=self.palette, ax=self.ax)
    
        if self.second_measure:
            self.plot_second_axis()

        image_path = self.save_file()
        return image_path



class LmPlot(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()

    def plot(self, **kwargs):

        sns.lmplot(x=self.dimension, y=self.measure, data=self.data, palette=self.palette, ax=self.ax)
        if self.second_measure:
            self.plot_second_axis()

        image_path = self.save_file()
        return image_path

class PairPlot(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()

    def plot(self, **kwargs): 
        sns.pairplot(self.data, palette=self.palette, ax=self.ax)
        image_path = self.save_file()
        return image_path
    

charts = {
    "table":Table,
    "bar":BarPlot,
    "line":LinePlot,
    "hist":HistPlot,
    "scatter":ScatterPlot,
    "box":BoxPlot,
    "count":CountPlot,
    "pairplot":PairPlot,
  
}


