import sys
from FactorioTypes import Blueprinter

if len(sys.argv) != 2:
    print("Syntax: python3 modifyBlueprint.py stringfilename")
    exit()

# Read in blueprint string file
bp = Blueprinter(inputStrFile=sys.argv[1])

# Read/modify loaded data
# class/field names from https://wiki.factorio.com/Blueprint_string_format), with some exceptions.
# check FactorioTypes.py for details
for entity in bp.entities:
    print(entity.name)

# Alright, now output it
bp.toCSV("newBP.csv")  # if you want an easy to read csv to view/edit
bp.toStrFile("newBP.txt")  # if you want to reimport your blueprint

#with open(sys.argv[1], "r") as f:
#    txt = f.read()
#
#bpjson = base64.b64decode(txt[1:])
#bpjson = zlib.decompress(bpjson)
#
#bpjson = json.loads(bpjson)
#
#
#if "blueprint" not in bpjson:
#    print("Invalid JSON format: expected upper level 'blueprint' string to be found (mods may change)")
#    exit(1)
#
#
## Metadata
#if "item" in bpjson["blueprint"]:
#    bpItem = bpjson["blueprint"]["item"]
#else:
#    bpItem = "blueprint"
#
#if "label" in bpjson["blueprint"]:
#    bpName = bpjson["blueprint"]["label"]  # overwrites above
#else:
#    bpName = "blueprint"
#
#if "label_color" in bpjson["blueprint"]:
#    #bpColor is tuple (r,g,b, a)
#    bpColor = Color(dic=bpjson["blueprint"]["label_color"])
#else:
#    bpColor = Color(r=255,g=255,b=255, a=255)
#
#if "version" in bpjson["blueprint"]:
#    mapVersion = int(bpjson["blueprint"]["version"])
#else:
#    mapVersion = 0
#
## Lists of data
#entities = []
#if "entities" in bpjson["blueprint"]:
#    entitiesJson = bpjson["blueprint"]["entities"]
#    for entity in entitiesJson:
#        entities.append(Entity(entity))
#
#tiles = []
#if "tiles" in bpjson["blueprint"]:
#    tilesJson = bpjson["blueprint"]["tiles"]
#    for tile in tilesJson:
#        tiles.append(Tile(tile))
#
#icons = []
#if "icons" in bpjson["blueprint"]:
#    iconsJson = bpjson["blueprint"]["icons"]
#    for icon in iconsJson:
#        icons.append(Icon(icon))
#
#schedules = []
#if "schedules" in bpjson["blueprint"]:
#    schedulesJson = bpjson["blueprint"]["schedules"]
#    for schedule in schedulesJson:
#        schedules.append(Schedule(schedule))
#
## Display metadata
#print(f"Name: {bpName}, Color: {bpColor}, Map Version #: {mapVersion}")
#
#with open("out.csv", "w", newline='') as csvfile:
#    # this csv will have quotes around every field
#    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
#
#    if entities:
#        writer.writerow(["Entities"])
#        writer.writerow([a for a in entities[0].__dict__])
#        for e in entities:
#            writer.writerow([a for a in e.__dict__.values()])
#    if tiles:
#        writer.writerow(["Tiles"])
#        writer.writerow([a for a in tiles[0].__dict__])
#        for t in tiles:
#            writer.writerow([a for a in t.__dict__.values()])
#    if icons:
#        writer.writerow(["Icons"])
#        writer.writerow([a for a in tiles[0].__dict__])
#        writer.writerow([a for a in icons[0].__dict__])
#        for i in icons:
#            writer.writerow([a for a in i.__dict__.values()])
#
#    if schedules:
#        writer.writerow(["Schedules"])
#        writer.writerow([a for a in schedules[0].__dict__])
#        for s in schedules:
#            writer.writerow([a for a in s.__dict__.values()])
#
##with open("tmp.txt", "w") as f:
##    f.write(str(bpjson))
#with open("out.txt", "w") as f:
#    res = {}
#    res["blueprint"] = {}
#
#    #write metadata
#    res["blueprint"]["item"] = bpItem
#    res["blueprint"]["label"] = bpName
#    res["blueprint"]["label_color"] = toDict(bpColor)
#    res["blueprint"]["version"] = mapVersion
#    #write data lists 
#    if entities:
#        res["blueprint"]["entities"] = [toDict(e) for e in entities]
#    if tiles:
#        res["blueprint"]["tiles"] = [toDict(t) for t in tiles]
#    if icons:
#        res["blueprint"]["icons"] = [toDict(e) for e in icons]
#    if schedules:
#        res["blueprint"]["schedules"] = [toDict(e) for e in schedules]
#
#    # convert to json
#    resjson = json.dumps(res)
#    # compress
#    compressed_res = zlib.compress(bytes(resjson, 'utf-8'))
#    #encode base 64
#    f.write("0"+base64.b64encode(compressed_res).decode('utf-8'))
#
