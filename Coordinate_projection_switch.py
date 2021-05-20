from pyproj import Proj, transform
string = "-4.15902168699995  50.334540964, -4.15505389499998  50.3336348280001, -4.14177842499993  50.332943051, -4.13741434199994  50.333577172"
string_split  = format_coords.split(',')

print(string_split)

converted_coordinates = []
for set in string_split:
    format_set = set.lstrip()
    set_split  = format_set.split(' ')
    x= float(set_split[0].replace("'", ""))
    y = float(set_split[2].replace("'", ""))
    inProj = Proj(init='epsg:4326')
    outProj =Proj(init='epsg:3857')
    x1,y1 = x,y
    x2,y2 = transform(inProj,outProj,x1,y1)
    d= x2, y2
    d_formatted =  str(d).replace(",","")
    converted_coordinates.append(d_formatted)

coordinates_formatted  = str(converted_coordinates).strip('[').strip(']').replace('(','').replace(')',"").replace("'","")
linestring  = "MULTILINESTRING(("+coordinates_formatted +"))"

print(linestring)

