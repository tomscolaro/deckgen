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
    
    def plot(self):
        # Pivot for bar plot
        bar_data = self.data.melt(self.data, id_vars=[self.XAxis], value_vars=[self.bar_cols],   var_name=self.measureLabel, value_name=self.valSelector)

        # Set figure and axis
        fig, ax1 = plt.subplots(figsize=self.size)

        # Clustered barplot with seaborn
        sns.barplot(data=bar_data, x=self.XAxis, y=self.measureLabel, hue=self.valSelector, ax=ax1, palette='muted')

        # Calculate line values (averages across groups for each category here, you can customize)
        line_data = self.data.groupby(self.XAxis)[self.line_col].sum().reset_index()

        # Plot line on same axis
        ax2 = ax1.twinx()
        sns.lineplot(data=line_data, x=self.XAxis, y=self.line_col, ax=ax2, marker='o', color='black', linewidth=2, label=self.line_col)

        # Align legends
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Labels and title
        ax1.set_ylabel("Bar Value")
        ax2.set_ylabel("Line Value")
        plt.title("Combo Chart: Clustered Bars + Line")



        
        img_path = self.save_file()
        return img_path