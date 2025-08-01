import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile
from charts.default import DefaultChart

class card(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()
    

    def prep_args(self, **kwargs):
        print(self.data)
        self.data = self.data[self.data['KPI'] == kwargs['kpi']]
        self.kpi_title = self.data[kwargs['kpi_title']].values[0]
        self.kpi_value = self.data[kwargs['kpi_value']].values[0]
        self.kpi_delta = self.data[kwargs['kpi_delta']].values[0]
        self.kpi_text = self.data[kwargs['kpi_text']].values[0]
        self.delta_color = self.data[kwargs['delta_color']].values[0]
        return 
    
    def plot(self, size=(4,2), **kwargs):
        # Plot setup
        fig, ax = plt.subplots(figsize=size)
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


        img_path = self.save_file()

        return img_path