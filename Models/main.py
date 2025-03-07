from taipy.gui import Gui
from pages.results import results_md
from pages.mapping import mapping_md
from pages.table import table_md
from pages.results import googlemaps_md

def main(): #Initializing all the variables in the constructor function in the following class 
    
    
    pages = {"home":mapping_md, "data": table_md, "results":results_md, "/": "<center><|navbar|></center>", "map":googlemaps_md}
    Gui(pages=pages).run()

if __name__ == '__main__':
    main()