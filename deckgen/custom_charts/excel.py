
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from charts.default import DefaultChart
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import matplotlib.colors as mcolors


class ExcelPlot(DefaultChart):
    def __init__(self, **kwargs):
        super().__init__()


    def prep_args(self,  **kwargs):    
        # self.data = ''
        self.size = kwargs['size']
        self.color = eval(kwargs['color'])

        return 

    def plot(self, **kwargs): 
        sl = kwargs['slide']
        pl = kwargs['placeholder']
        left = pl.left - Inches(.05)
        top = pl.top - Inches(.05)
        width = pl.width + Inches(.1)
        height = pl.height

        rows = self.data.shape[0]+1
        cols =  self.data.shape[1]

        table_shape = sl.shapes.add_table(rows, cols, left, top, width, height)
        table = table_shape.table
        

        # Write column headers
        for col_idx, col_name in enumerate(self.data.columns):
            table.cell(0, col_idx).text = str(col_name)

        # Write data rows
        for row_idx, row in self.data.iterrows():
            for col_idx, value in enumerate(row):
                cell = table.cell(row_idx + 1, col_idx)
                cell.text = str(value)

                for para in cell.paragraphs:
                    for run in para.runs:
                        run.font.size =   Pt(10)


        # pl.remove()
        for col_idx in range(cols):
            cell = table.cell(0, col_idx)
            fill = cell.fill
            fill.solid()  # Use solid fill
            # colors =  mcolors.to_rgb(self.color)
            # print(colors)
            fill.fore_color.rgb = RGBColor(self.color[0], self.color[1], self.color[2])  # Dark blue
                

        for row_idx in range(1, rows):
            for col_idx in range(cols):
                cell = table.cell(row_idx, col_idx)
                fill = cell.fill
                fill.solid()
                if row_idx % 2 == 0:
                    fill.fore_color.rgb = RGBColor(242, 242, 242)  # Light gray
                else:
                    fill.fore_color.rgb = RGBColor(255, 255, 255)  # White

    
        return