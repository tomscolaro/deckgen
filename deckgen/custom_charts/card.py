import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile


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
        print(self.data)
        self.data = self.data[self.data['KPI'] == kwargs['kpi']]
        self.kpi_title = self.data[kwargs['kpi_title']].values[0]
        self.kpi_value = self.data[kwargs['kpi_value']].values[0]
        self.kpi_delta = self.data[kwargs['kpi_delta']].values[0]
        self.kpi_text = self.data[kwargs['kpi_text']].values[0]
        self.delta_color = self.data[kwargs['delta_color']].values[0]

    
        return 
    
    def plot(self, size=(1,1)):
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

        # plt.tight_layout()
        # plt.show()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:    
                # plt.title(f'{self.chartType.capitalize()} plot of {measure} by {dimension}')
                plt.tight_layout(pad=3.0)
                plt.savefig(tmpfile.name)
                plt.close()


        img_path = tmpfile.name


        return img_path