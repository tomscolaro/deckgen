import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class card:
    def __init__(self, ):
        self.data = None
        # KPI values
        self.kpi_title = ""
        self.kpi_value = ""
        self.kpi_delta = ""
        self.kpi_text = ""
        self.delta_color = ""  # green for positive, red if negative

        return
    
    def add_data(self, df):
        self.data = df
        return 
    
    def prep_data(self, **kwargs):
        self.kpi_title = self.data[kwargs['kpi_title']]
        self.kpi_value = self.data[kwargs['kpi_value']]
        self.kpi_delta = self.data[kwargs['kpi_delta']]
        self.kpi_text = self.data[kwargs['kpi_text']]
        self.delta_color = self.data[kwargs['delta_color']]

        self.size = kwargs['size']
        return 
    
    def plot(self):
        # Plot setup
        fig, ax = plt.subplots(figsize=self.size)
        fig.patch.set_facecolor('white')
        ax.axis('off')  # Hide axes

        # Add text
        ax.text(0, 0.95, self.kpi_title, fontsize=24, fontweight='bold', color='#34495e',  ha= 'center')
        ax.text(-.35, 0.6,  self.kpi_value, fontsize=28, fontweight='bold', color='#2c3e50', ha= 'center')
        ax.text(.35, 0.635, self.kpi_delta, fontsize=12, color= self.delta_color, ha= 'center')
        ax.text(.0, .2,  self.kpi_text, fontsize=12, fontweight='bold', color='#34495e', ha= 'center')

        # Optional: add border or shadow for card effect
        for spine in ax.spines.values():
            spine.set_visible(False)

        plt.tight_layout()
        plt.show()

        return