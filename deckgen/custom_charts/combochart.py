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
        
        self.color_palette = kwargs.get('palette', 'pastel') 
        self.y1_label = kwargs.get('ylabel1', 'ylabel1')
        self.y2_label = kwargs.get('ylabel2', 'ylabel2')
        self.x_label = kwargs.get('xlabel', 'xlabel')
        self.y1_label_size = kwargs.get('y1label_size', 8)
        self.y2_label_size = kwargs.get('y2label_size', 8)
        self.x_label_size = kwargs.get('xlabel_size', 8)
        self.bar_label_size = kwargs.get('bar_label_size', 4)
        self.line_label_size = kwargs.get('line_label_size', 4)
        self.title = kwargs.get('Title', 'Title')
        self.line_color = kwargs.get('line_color', 'black')
        self.legend_x1 = kwargs.get('legendX1', .35)
        self.legend_x2 = kwargs.get('legendX2', .35)
        self.bscale = kwargs.get('bscale', 1)
        self.label_skew = kwargs.get('label_skew', .5)
        return 
    
    def plot(self, **kwargs): 
        # Pivot for bar plot
        bar_data = self.data.melt(id_vars=[self.XAxis], value_vars=self.bar_cols,  var_name=self.measureLabel)

        # Set figure and axis
        _, ax1 = plt.subplots(figsize=self.size)

        # Clustered barplot with seaborn
        sns.barplot(data=bar_data, x=self.XAxis, y='value', hue=self.measureLabel, ax=ax1, palette=self.color_palette)

            # Add labels to each bar
        for c in ax1.containers:
            ax1.bar_label(c, fmt='{:,.1f}M'.format, 
                          labels=[ round(val / self.bscale, 1) if val > 0 else '' for val in c.datavalues ],
                          fontsize=self.bar_label_size, 
                          label_type='center')

        # Calculate line values (averages across groups for each category here, you can customize)
        line_data = self.data.groupby(self.XAxis)[self.line_col].sum().reset_index()

        # Plot line on same axis
        ax2 = ax1.twinx()
        sns.lineplot(data=line_data, x=self.XAxis, y=self.line_col, ax=ax2, color=self.line_color, marker='o', linewidth=1, label=self.line_col)
        # Add labels to each point
        for _, row in self.data.iterrows():
            ax2.text(row[self.XAxis], round(row[self.line_col] + self.label_skew, 1), round(row[self.line_col] + 1, 1), ha='center', fontsize=self.line_label_size)




        plt.rcParams["ytick.labelsize"] = self.y1_label_size
        ax1.tick_params(axis='x', labelrotation=45, size=self.x_label_size) 

        # Align legends
        ax1.set_xlabel(self.x_label,fontsize=self.x_label_size)
        
        ax1.legend(loc='lower center',  bbox_to_anchor=(self.legend_x1, -.6), fontsize='x-small',ncol=3, frameon=False)
        ax2.legend(loc='lower right',  bbox_to_anchor=(self.legend_x2, -.6), fontsize='x-small',ncol=1, frameon=False)
        # Labels and title
        ax1.set_ylabel(self.y1_label, fontsize=self.y1_label_size)
        
        ax2.set_ylabel(self.y2_label, fontsize=self.y2_label_size)
        plt.title(self.title)



        img_path = self.save_file((8,2.5))
        return img_path