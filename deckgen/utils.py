import yaml
import pandas as pd


class ConfigController:
    def __init__(self, config_path):
        self.config = self.config_to_dict(config_path)

    def config_to_dict(self, path):
        with open(path, 'r') as file:
        # Read the entire content
            content = file.read()
        return yaml.safe_load(content)
    
    def display_config(self):
        print(self.config)

    def get_version(self):
        return self.config['ApiVersion']

    def get_data(self):
        return self.config['Presentation']['Data']
    
    def get_data_path(self):
        return self.config['Presentation']['Data']['Path']

    def get_slides(self):
        return self.config['Presentation']['Slides']

    def get_output_path(self):
        return self.config['Presentation']['Output']['Path']
    
    def get_template_path(self):
        return self.config['Presentation']['Template']['Path']
    
    def get_style(self):
        return self.config['Presentation']['Template']['ColorStyle']
    
    def get_presentation_title(self):
        return self.config['Presentation']['Output']['Name']

    def get_presentation_author(self):
        return self.config['Presentation']['Output']['Author']

# Function to find slide layout by name
def find_layout_by_name(prs, layout_name):
    for layout in prs.slide_layouts:
        if layout.name == layout_name:
            return layout
    return None





def chart_support():
    return




def read_csvs_to_dfs(data_config):
    return_dict = {}

    for _, data in enumerate(data_config):
        
        name = data['Name']
        path = data['Path']

        if data['Type'] == 'File':
            return_dict[name] = pd.read_csv(path)
            
    return return_dict