
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns
from charts.default import DefaultChart

class doubleCluster(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()

    def prep_args(self,  **kwargs):    
        # self.data = ''
        self.XAxis = kwargs['XAxis']
        self.dimension_filter_str = kwargs['dimension_filter_value']
        self.dimension = kwargs['dimension']
        self.val = kwargs['measure']
    
        self.size = kwargs['size']


        self.color_palette = kwargs.get('palette', 'pastel') 
        self.y_label = kwargs.get('ylabel', 'ylabel')
        self.x_label = kwargs.get('xlabel', 'xlabel')
        self.y_label_size = kwargs.get('ylabel_size', 8)
        self.x_label_size = kwargs.get('xlabel_size', 8)
        self.bar_label_size = kwargs.get('bar_label_size', 6)
        self.title = kwargs.get('Title', 'Title')
        self.scale = kwargs.get('scale', 1_000_000)
        return 
    
    def plot(self, **kwargs): 
        
        # Define time periods
        all_dates = sorted(self.data[self.XAxis].unique())
        x = range(len(all_dates))
        bar_width = 0.35

        # Separate condition types
        false_data = self.data[self.data[self.dimension] != self.dimension_filter_str]
        true_data = self.data[self.data[self.dimension] == self.dimension_filter_str]

        # Pivot table for stacked bars
        stacked_pivot = false_data.pivot_table(
            index=self.XAxis,
            columns=self.dimension,
            values=self.val,
            aggfunc='sum',
            fill_value=0
        ).reindex(all_dates, fill_value=0)

        # True totals
        true_totals = true_data.groupby(self.XAxis)[self.val].sum().reindex(all_dates, fill_value=0)

        # Plot with Seaborn style but Matplotlib logic
        fig, ax = plt.subplots(figsize=self.size)

        # Get colors from seaborn palette
        palette = sns.color_palette(self.color_palette, n_colors=len(stacked_pivot.columns))
        category_colors = dict(zip(stacked_pivot.columns, palette))

        # X positions
        x_stacked = [i - bar_width/2 for i in x]
        x_total = [i + bar_width/2 for i in x]

        ax.bar(
            x_total,
            true_totals.tolist(),
            width=bar_width,
            label='Total Target',
            color=sns.color_palette("grey")[3]
        )
        for c in ax.containers:
            ax.bar_label(c, fmt='{:,.1f}M'.format, labels=[ round(val / self.scale, 2) for val in c.datavalues], fontsize=self.bar_label_size)

        # Plot stacked bars
        bottom = [0] * len(all_dates)
        for category in stacked_pivot.columns:
            values = stacked_pivot[category].tolist()
            p = ax.bar(
                x_stacked,
                values,
                bottom=bottom,
                width=bar_width,
                label=f'{category}',
                color=category_colors[category]
            )
            bottom = [b + v for b, v in zip(bottom, values)]
            ax.bar_label(p, fmt='{:,.1f}M'.format, labels=[ round(val / self.scale, 2) for val in p.datavalues], fontsize=self.bar_label_size)


        # for c in ax.containers:
        #     ax.bar_label(c, fmt='{:,.1f}M'.format, labels=[int(val) / 1_000_000 for val in c.datavalues])
        # Plot total bars


        # # Final formatting
        # for c in ax.containers:
        #     ax.bar_label(c, fmt='{:.2f}M'.format, labels=[ round(val / self.scale, 2) for val in c.datavalues], fontsize=self.bar_label_size)
     

        plt.ticklabel_format(style='plain', axis='y')
        # Define a formatter function to add "mm"
        def mm_formatter(x, pos):
            if self.scale ==1000:
                return f"{x/ self.scale:.0f}k" # Format as integer with "mm"
            if self.scale ==1000000:
                return f"{x/ self.scale:.0f}mm" # Format as integer with "mm"
        # Apply the formatter to the y-axis
        plt.gca().yaxis.set_major_formatter(FuncFormatter(mm_formatter))

        plt.rcParams["ytick.labelsize"] = self.y_label_size
        ax.set_xticks(x,)
        ax.set_xticklabels(all_dates, fontsize=self.x_label_size)
        ax.tick_params(axis='x', labelrotation=45, size=self.x_label_size) 
       
        ax.set_ylabel(self.y_label, fontsize=self.y_label_size)
        # ax.tick_params(axis='y', size=4) 
        # ax.set_yticklabels(fontsize=4)
        ax.set_title(self.title, fontsize=16)

        # Move legend to the bottom
        ax.legend(loc='lower center',  bbox_to_anchor=(0.5, -.5), fontsize='x-small',ncol=4, frameon=False)

        img_path = self.save_file((12,2.5))
        return img_path