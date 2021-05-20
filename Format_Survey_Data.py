import pandas as pd
from dateutil.relativedelta import relativedelta
from pyproj import Proj, transform
import re


## ADDED NEW FIELD Set_Type
# Name change to feature class to search for change in script

download_number  = 0

input_data_paths  = [r"C:\Users\darle\Documents\Assets_2021\Downloading_Data\Downloaded_Survey_Data\SWRCMP_Defences_Survey_Results.csv",
                     r"C:\Users\darle\Documents\Assets_2021\Downloading_Data\Downloaded_Survey_Data\SWRCMP_Structures_Survey_Results.csv"]


def format_surevy_data(path):

    data = pd.read_csv(path
        ,
        delimiter=",")

    df = pd.DataFrame(data)

    # removing columns not necessary for upload to postgres

    # drop blank column
    df = df.drop("Unnamed: 0", axis=1)


    # variable holding the asset type, defence or structure
    asset_type = df.Set_Type.unique()[0]

    df =df.drop("Set_Type", axis= 1)

    # remove creation date, this is when survey uploaded not conducted
    df = df.drop("CreationDate", axis=1)

    # this the old last inspection date
    df = df.drop("last_inspect", axis=1)

    # remove arcgis tracking data, not needed
    df = df.drop("EditDate", axis=1)
    df = df.drop("Editor", axis=1)
    df = df.drop("Creator", axis=1)


    # remove surveyor name, not needed in final database useful if data is incorrect and need a contact
    df = df.drop("Surveyor_Name", axis=1)

    # drop arc global id
    df = df.drop("globalid", axis=1)

    # drop has sub-typed changed, probably use this to qc the database history logs
    df = df.drop("has_subtype_changed", axis=1)

    # next due is calculated in the app, not a field in the database (probably should be), don't need old cond.
    df = df.drop("last_cond", axis=1)
    df = df.drop("next_due_string", axis=1)

    #
    # df = df.drop("SHAPE", axis=1)

    # Points have no length property
    if asset_type == "Defence":
        df = df.drop("Shape__Length", axis=1)



    #df = df.drop("line_coords", axis=1)

    df = df.drop("objectid", axis=1)

    df = df.drop("Current_Description", axis=1)

    # calculate next due inspection
    df["Date_of_Last_Assessment_T98"] = pd.to_datetime(df['Date_of_Last_Assessment_T98'])
    due_dates = []
    frequencies = []
    for i in df["Frequency_Modifer"]:
        frequencies.append(i)

    count = 0
    for x in df["Date_of_Last_Assessment_T98"]:
        due_date = x + relativedelta(months=frequencies[count])
        due_dates.append(due_date)
        count += 1

    df["date_next_inspection_due"] = due_dates

    df['Location'] = df['Location'].str.replace(',', ' ')
    df['Comments'] = df["Comments"].str.replace(',', ' ')

    df["source_date"] = df["Date_of_Last_Assessment_T98"]

    # renaming columns to match the postgres table names
    df1 = df.rename(columns={"Alert_Inspection": "alert_inspection",
                             "Alert_Not_Able_To_Inspect": "alert_not_able_to_inspect",
                             "Alert_Transition": "alert_transition",
                             "Assessed_Weighted_Condition": "assessed_weighted_condition",
                             "Asset_ID": "asset_id",
                             "Asset_Sub_Type": "asset_sub_type",
                             "Asset_Type": "asset_type",
                             "Comments": "asset_comments",
                             "DQI_Condition": "dqi_condition",
                             "Date_of_Last_Assessment_T98": "date_of_last_assessment_t98",
                             # app returns as survey date taken
                             "Description": "description",
                             "Element_1": "element_1_type",
                             "Element_1_Current_Condition": "element_1_condition",
                             "Element_1_Material": "element_1_material",
                             "Element_2": "element_2_type",
                             "Element_2_Current_Condition": "element_2_condition",
                             "Element_2_Material": "element_2_material",
                             "Element_3": "element_3_type",
                             "Element_3_Current_Condition": "element_3_condition",
                             "Element_3_Material": "element_3_material",
                             "Element_4": "element_4_type",
                             "Element_4_Current_Condition": "element_4_condition",
                             "Element_4_Material": "element_4_material",
                             "Element_5": "element_5_type",
                             "Element_5_Current_Condition": "element_5_condition",
                             "Element_5_Material": "element_5_material",
                             "Element_6": "element_6_type",
                             "Element_6_Current_Condition": "element_6_condition",
                             "Element_6_Material": "element_6_material",
                             "Element_7": "element_7_type",
                             "Element_7_Current_Condition": "element_7_condition",
                             "Element_7_Material": "element_7_material",
                             "Element_8": "element_8_type",
                             "Element_8_Current_Condition": "element_8_condition",
                             "Element_8_Material": "element_8_material",
                             "Element_9": "element_9_type",
                             "Element_9_Current_Condition": "element_9_condition",
                             "Element_9_Material": "element_9_material",
                             "Element_ID": "element_id",
                             "Frequency_Modifer": "assessment_frequency_t98",
                             "Inspected_CondItion": "inspected_condition",
                             "Location": "location",
                             "NI_Element_1": "alert_element_1_not_inspected",
                             "NI_Element_2": "alert_element_2_not_inspected",
                             "NI_Element_3": "alert_element_3_not_inspected",
                             "NI_Element_4": "alert_element_4_not_inspected",
                             "NI_Element_5": "alert_element_5_not_inspected",
                             "NI_Element_6": "alert_element_6_not_inspected",
                             "NI_Element_7": "alert_element_7_not_inspected",
                             "NI_Element_8": "alert_element_8_not_inspected",
                             "NI_Element_9": "alert_element_9_not_inspected",
                             "Object_ID": "objectid",
                             "SHAPE": "shape",
                             "SWRCMP_ID": "swrcmp_id",
                             "Surveyor_Company": "source_supplier",
                             "Target_Condition": "target_condition_last_t98",
                             "cal_weighting_Element_1": "element_1_weighting",
                             "cal_weighting_Element_2": "element_2_weighting",
                             "cal_weighting_Element_3": "element_3_weighting",
                             "cal_weighting_Element_4": "element_4_weighting",
                             "cal_weighting_Element_5": "element_5_weighting",
                             "cal_weighting_Element_6": "element_6_weighting",
                             "cal_weighting_Element_7": "element_7_weighting",
                             "cal_weighting_Element_8": "element_8_weighting",
                             "cal_weighting_Element_9": "element_9_weighting",

                             })

    # fill alert inpection nans with None, this is the default.
    df1['alert_inspection'] = df1["alert_inspection"].fillna(value="None")

    # fill materials nans with none
    df1[["element_1_material", "element_2_material", "element_3_material",
         "element_4_material", "element_5_material", "element_6_material",
         "element_7_material", "element_8_material", "element_9_material"]] = df1[
        ["element_1_material", "element_2_material", "element_3_material",
         "element_4_material", "element_5_material", "element_6_material",
         "element_7_material", "element_8_material", "element_9_material"]].fillna(value="none")

    # fill materials nans with none
    df1[["element_1_condition", "element_2_condition", "element_3_condition",
         "element_4_condition", "element_5_condition", "element_6_condition",
         "element_7_condition", "element_8_condition", "element_9_condition"]] = df1[
        ["element_1_condition",
         "element_2_condition",
         "element_3_condition",
         "element_4_condition",
         "element_5_condition",
         "element_6_condition",
         "element_7_condition",
         "element_8_condition",
         "element_9_condition"]].fillna(
        value=int(0))

    # WHere nans filled to 0 making the columns floats, this converts:



    # add a if it is a defence format geom like this, if not format like that

    if asset_type == "Defence":
        new_shape = []
        # format coordinates into a linestring format ('LINESTRING(-5.8427265 43.3678474,-5.8421236 43.3677908)', 4326));

        for row in df1["shape"]:
            ssrd = row.split(":")[-1].strip("{").strip("}")
            forrmat_1 = \
            row.replace("[", "").replace("]", "").replace("{", "").replace("}", "").replace("paths': ", "").split("'")[
                1].replace("'", "").replace(" ", "")
            format_2 = forrmat_1.split(",")

            adjust_commas = re.sub('(,[^,]*),', r'\1 ', ","+str(format_2))
            format_coords = adjust_commas.replace(",['","").replace(", '']","").replace("'","")
            string_split = format_coords.split(',')

            print(string_split)

            converted_coordinates = []
            for set in string_split:
                format_set = set.lstrip()
                set_split = format_set.split(' ')
                x = float(set_split[0].replace("'", ""))
                y = float(set_split[2].replace("'", ""))
                inProj = Proj(init='epsg:4326')
                outProj = Proj(init='epsg:3857')
                x1, y1 = x, y
                x2, y2 = transform(inProj, outProj, x1, y1)
                d = x2, y2
                d_formatted = str(d).replace(",", "")
                converted_coordinates.append(d_formatted)

            coordinates_formatted = str(converted_coordinates).strip('[').strip(']').replace('(', '').replace(')',
                                                                                                              "").replace(
                "'", "")
            linestring = "MULTILINESTRING((" + coordinates_formatted + "))"

            print(linestring)

            new_shape.append(linestring)

        df1["shape"] =new_shape
        outpath  = r"C:\Users\darle\Documents\Assets_2021\Processing\processed_defences.csv"


    else:
        new_shape = []
        for row in df1["shape"]:
            # format coordinates into Point format ('POINT(0 0)')


            format_1 = row.split(':')
            x = format_1[1].strip("'y'").strip().strip(',')
            y = format_1[2].strip(" 'spatialReference'").strip(',')

            # change projection from wgs1984 wgs1984 web mecator
            inProj = Proj(init='epsg:4326')
            outProj = Proj(init='epsg:3857')
            x1, y1 = x, y
            x2, y2 = transform(inProj, outProj, x1, y1)
            d = x2, y2
            d = str(d).replace(",", "")
            pointstring = "POINT" + d
            new_shape.append(pointstring)

            print(pointstring)
        df1["shape"] = new_shape
        outpath = r"C:\Users\darle\Documents\Assets_2021\Processing\processed_structures.csv"

    df1.to_csv(outpath, index=False, float_format='%.f',
               sep='>')


format_surevy_data(input_data_paths[download_number])