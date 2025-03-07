from taipy.gui import Markdown
import pandas as pd
import os
carData = os.path.join("Models","seattle.sample.daily.csv")


data = pd.read_csv(carData)



table_md = Markdown("""
                      
# Extracted Vehicle Flow Data
                    
<|{data}|table|page_size=14|filter=true|>          
""")



    