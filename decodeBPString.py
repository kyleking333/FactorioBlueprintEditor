import sys
import json
import base64
import zlib
from DataTypes import *
import csv

if len(sys.argv) != 2:
    print("Syntax: python3 decodeBPString.py stringfilename")
    exit()

with open(sys.argv[1], "r") as f:
    txt = f.read()

bpjson = base64.b64decode(txt[1:])
bpjson = zlib.decompress(bpjson)

bpjson = json.loads(bpjson)


if "blueprint" not in bpjson:
    print("Invalid JSON format: expected upper level 'blueprint' string to be found (mods may change)")
    exit(1)


# Metadata
if "item" in bpjson["blueprint"]:
    bpName = bpjson["blueprint"]["item"]
else:
    bpName = "blueprint"

if "label" in bpjson["blueprint"]:
    bpName = bpjson["blueprint"]["label"]  # overwrites above

if "label_color" in bpjson["blueprint"]:
    #bpColor is tuple (r,g,b, a)
    bpColor = Color(dic=bpjson["blueprint"]["label_color"])
else:
    bpColor = Color(r=255,g=255,b=255, a=255)

if "version" in bpjson["blueprint"]:
    mapVersion = int(bpjson["blueprint"]["version"])
else:
    mapVersion = 0

# Lists of data
entities = []
if "entities" in bpjson["blueprint"]:
    entitiesJson = bpjson["blueprint"]["entities"]
    for entity in entitiesJson:
        entities.append(Entity(entity))

tiles = []
if "tiles" in bpjson["blueprint"]:
    tilesJson = bpjson["blueprint"]["tiles"]
    for tile in tilesJson:
        tiles.append(Tile(tile))

icons = []
if "icons" in bpjson["blueprint"]:
    iconsJson = bpjson["blueprint"]["icons"]
    for icon in iconsJson:
        icons.append(Icon(icon))

schedules = []
if "schedules" in bpjson["blueprint"]:
    schedulesJson = bpjson["blueprint"]["schedules"]
    for schedule in schedulesJson:
        schedules.append(Schedule(schedule))

# Display metadata
print(f"Name: {bpName}, Color: {bpColor}, Map Version #: {mapVersion}")

with open("out.csv", "w", newline='') as csvfile:
    # this csv will have quotes around every field
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    if entities:
        writer.writerow(["Entities"])
        writer.writerow([a for a in entities[0].__dict__])
        for e in entities:
            writer.writerow([a for a in e.__dict__.values()])
    if tiles:
        writer.writerow(["Tiles"])
        writer.writerow([a for a in tiles[0].__dict__])
        for t in tiles:
            writer.writerow([a for a in t.__dict__.values()])
    if icons:
        writer.writerow(["Icons"])
        writer.writerow([a for a in tiles[0].__dict__])
        writer.writerow([a for a in icons[0].__dict__])
        for i in icons:
            writer.writerow([a for a in i.__dict__.values()])

    if schedules:
        writer.writerow(["Schedules"])
        writer.writerow([a for a in schedules[0].__dict__])
        for s in schedules:
            writer.writerow([a for a in s.__dict__.values()])

