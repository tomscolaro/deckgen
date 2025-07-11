
import pandas as pd
import matplotlib.pyplot as plt
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
        palette = sns.color_palette("pastel", n_colors=len(stacked_pivot.columns))
        category_colors = dict(zip(stacked_pivot.columns, palette))

        # X positions
        x_stacked = [i - bar_width/2 for i in x]
        x_total = [i + bar_width/2 for i in x]

        # Plot stacked bars
        bottom = [0] * len(all_dates)
        for category in stacked_pivot.columns:
            values = stacked_pivot[category].tolist()
            ax.bar(
                x_stacked,
                values,
                bottom=bottom,
                width=bar_width,
                label=f'{category}',
                color=category_colors[category]
            )
            bottom = [b + v for b, v in zip(bottom, values)]

        # Plot total bars
        ax.bar(
            x_total,
            true_totals.tolist(),
            width=bar_width,
            label='Total Target',
            color=sns.color_palette("grey")[3]
        )
        # Final formatting
        ax.set_xticks(x,)
        ax.set_xticklabels(all_dates)
        ax.tick_params(axis='x', labelrotation=45, size=4) 
        ax.set_ylabel('Value')
        ax.set_title('Clustered Column Chart: Stacked + Total Bars')

        # Move legend to the bottom
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.5), fontsize='x-small',ncol=4, frameon=False)

        img_path = self.save_file()

        return img_path