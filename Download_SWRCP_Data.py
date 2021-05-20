from arcgis.gis import GIS

"""This script pulls data from AGOL, collecting the SWRCMP Database and storing as shp. files. It also grabs the 
   a CSV of the Survey results """

gis = GIS("https://swrcmp-pco.maps.arcgis.com//", "TDarley01", "Sugarpuff22")

types  = ["Defence", "Structure"]

# takes two types, Defence or Structure
run_for = types[0]


def GetSurvey_Data(asset_type):

    if asset_type == "Defence":
        search_item = "SWRCMP_Defences_Survey"
        file_extension  = "SWRCMP_Defences_Survey_Results.csv"
    else:
        search_item = "SWRCMP_Structures_Survey"
        file_extension = "SWRCMP_Structures_Survey_Results.csv"


    # Loading in Hosted Feature Collection
    search_result = gis.content.search(search_item,item_type='Feature Layer Collection')
    print(search_result)

    # Getting URLs for the hosted feature layers in the geodatabase
    feature_layers = search_result[0].layers

    # Query returns a feature set object which we can call, we return as a spatial DF object (sdf)
    SWRCMP_Survey_Results = feature_layers[0].query().sdf
    base_path  = r'C:\Users\darle\Documents\Assets_2021\Downloading_Data\Downloaded_Survey_Data'
    output_path  = base_path + "\\" + file_extension
    SWRCMP_Survey_Results.to_csv(output_path)

GetSurvey_Data(run_for)
