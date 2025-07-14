import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from charts.default import DefaultChart


class combochart(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()
    
    def prep_args(self, **kwargs):    
        self.XAxis = kwargs['XAxis']
        self.bar_cols = kwargs['bar_measure']
        self.line_col = kwargs['line_measure']

        self.size = kwargs['size']
        self.measureLabel = kwargs.get('measureLabel', 'measure')
        self.valSelector = kwargs.get('valSelector', 'valSelector')
        return 
    
    def plot(self, **kwargs): 
        # Pivot for bar plot
        bar_data = self.data.melt(id_vars=[self.XAxis], value_vars=self.bar_cols,  var_name=self.measureLabel)

        # Set figure and axis
        fig, ax1 = plt.subplots(figsize=self.size)

        # Clustered barplot with seaborn
        sns.barplot(data=bar_data, x=self.XAxis, y=self.measureLabel, hue=self.measureLabel, ax=ax1, palette='muted')

        # Calculate line values (averages across groups for each category here, you can customize)
        line_data = self.data.groupby(self.XAxis)[self.line_col].sum().reset_index()

        # Plot line on same axis
        ax2 = ax1.twinx()
        sns.lineplot(data=line_data, x=self.XAxis, y=self.line_col, ax=ax2, marker='o', color='black', linewidth=2, label=self.line_col)

        ax1.tick_params(axis='x', labelrotation=45, size=10) 

        # Align legends
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Labels and title
        ax1.set_ylabel(" bar value", fontsize=10)
        
        ax2.set_ylabel(" value value", fontsize=10)
        plt.title("Combo Chart: Clustered Bars + Line")



        img_path = self.save_file((8,2.5))
        return img_path