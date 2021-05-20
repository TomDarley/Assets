from arcgis.gis import GIS
import glob
import os

gis = GIS("https://swrcmp-pco.maps.arcgis.com//", "TDarley01", "Sugarpuff22")

def Extract_Photos():

    """This function grabs photos from agol renames them with asset IDs.  To change to collect structure photos on line
        16 chnage layers[0] to layers[1]

        Assumptions made: All assets surveyed will have a photo (set to required in survey form, if missing this
           will fail

        Because you can only download a photo giving a id of a folder and this id does not start at 1, the script
        loops over a range of possible ids line 50 trying everyone until found. This could cause issues, the folder id
        can be looked for by opening the photo in AGOL and checking the url for the folder number.

        """

    # Loading in Hosted geodatabase
    search_result = gis.content.search("SWRCMP_Defences_Survey",item_type="Feature Layer")

    # Getting URLs for the hosted feature layers in the geodatabase
    defences= search_result[0].layers[0]

    print(defences)
    print(type(defences))

    # photos dont have any asset id information so we get all the ids present in the defence feature class
    defence_query = defences.query()
    asset_ids = list(defence_query.sdf['SWRCMP_ID'])

    # list that the function returns which holds asset id in order of each photo that was downloaded

    photo_asset_ids  = []

    # this hold the attachment folder id
    id = []

    # this holds the length of attachment folder lists, the first photo is always one less than the
    # attachment folder id. So folder id 6, first photo inside folder will be 5 ,second 6 etc. Returning the length
    # of each attchment list gives us a range to pass photo id to download.

    photo_ids = []

    # set this range to something high, to catch all attachment folders
    for i in range(10):
        try:
            list_found = defences.attachments.get_list(i)
            # if list is populated append to id list
            if len(list_found) > 0:
                id.append(i)
                length_of_list = len(list_found)
                photo_ids.append(length_of_list)
                print(list_found)


        except Exception:
            continue

    count = 0
    for x in id:
        # we can set the asset id and append to a list, where each photo downloaded has a corresponding id
        set_asset_id  = asset_ids[count]

        number_of_photos = photo_ids[count]
        attach_id = x - 1
        attach_id = x
        count+=1
        for y in range(number_of_photos):

            # appending asset id for photo being downloaded
            photo_asset_ids.append(set_asset_id)
            print(attach_id)
            print(x)

            defences.attachments.download(oid=x, attachment_id=attach_id, save_path=r'C:\Users\darle\Documents\Assets_2021\Downloading_Data\Attachments')

            attach_id += 1

    # we return the list odf asset ids as a list
    return (photo_asset_ids)

ass_id = Extract_Photos()

def rename_photos():

    search_dir = r"C:\Users\darle\Documents\Assets_2021\Downloading_Data\Attachments"
    ordered_photo_files  =  []
    os.chdir(search_dir)
    files = glob.glob("*.jpg")
    files.sort(key=os.path.getmtime)

    files_str = list(files)
    for file in files_str:
        full_path  =  search_dir + "\\" + file
        ordered_photo_files.append(full_path)


    print(ordered_photo_files)
    count =0
    for ordered_file in ordered_photo_files:
        new_name  = search_dir  + "\\" +ass_id[count] + "_" + ordered_file.split("\\")[-1]
        print(new_name)
        count+=1
        os.rename(ordered_file, new_name)


rename_photos()











