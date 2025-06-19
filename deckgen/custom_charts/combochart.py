import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class combochart:
    def __init__(self, ):
        self.data = None
        return
    
    def add_data(self, df):
        self.data = df

    def prep_data(self, **kwargs):    
        self.XAxis = kwargs['XAxis']
        self.labelFilter = kwargs['labelIndicator']
        self.label = kwargs['label']
        self.val = kwargs['value']
        self.secondVal = kwargs['secondValue']

        self.size = kwargs['size']
        return 
    
    def plot(self):
                
        # Pivot for bar plot
        bar_data = self.data.pivot(index=self.XAxis, columns=self.label, values=self.val).reset_index()

        # Set figure and axis
        fig, ax1 = plt.subplots(figsize=self.size)

        # Clustered barplot with seaborn
        sns.barplot(data=self.data, x=self.XAxis, y=self.val, hue=self.label, ax=ax1, palette='muted')

        # Calculate line values (averages across groups for each category here, you can customize)
        line_data = self.data.groupby(self.XAxis)[self.secondVal].sum().reset_index()

        # Plot line on same axis
        ax2 = ax1.twinx()
        sns.lineplot(data=line_data, x=self.XAxis, y=self.secondVal, ax=ax2, marker='o', color='black', linewidth=2, label=self.secondVal)

        # Align legends
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Labels and title
        ax1.set_ylabel("Bar Value")
        ax2.set_ylabel("Line Value")
        plt.title("Combo Chart: Clustered Bars + Line")

        plt.tight_layout()
        plt.show()