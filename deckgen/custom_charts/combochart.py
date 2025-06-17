
class combochart:
    def __init__(self, ):
        self.data = None
        return
    
    def add_data(self, df):
        self.data = df

    def data_prep(self):    


        return 
    
    def plot(self):
                
        # Pivot for bar plot
        bar_data = self.data.pivot(index='Category', columns='Group', values='Value').reset_index()

        # Set figure and axis
        fig, ax1 = plt.subplots(figsize=(8, 5))

        # Clustered barplot with seaborn
        sns.barplot(data=data, x='Category', y='Value', hue='Group', ax=ax1, palette='muted')

        # Calculate line values (averages across groups for each category here, you can customize)
        line_data = data.groupby('Category')['LineValue'].mean().reset_index()

        # Plot line on same axis
        ax2 = ax1.twinx()
        sns.lineplot(data=line_data, x='Category', y='LineValue', ax=ax2, marker='o', color='black', linewidth=2, label='LineValue')

        # Align legends
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')

        # Labels and title
        ax1.set_ylabel("Bar Value")
        ax2.set_ylabel("Line Value")
        plt.title("Combo Chart: Clustered Bars + Line")

        plt.tight_layout()
        plt.show()