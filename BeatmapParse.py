

import re


# only reads the necessary data for viewing the beatmap not playing
#returns a tuple containing (metadata, diff data, audiofile, bgfile)
def shallowRead(beatmapPath):


    cSection = ""
    parsed = ["AudioFilename","Metadata","Difficulty"]
    data = {}
    with open(beatmapPath, 'r', encoding='utf-8') as cBeatmap:

        for line in cBeatmap:
            if line == "\n":
                continue
            tempSearch = re.search(r"\[([A-Za-z0-9_]+)\]", line)
            try:
                cSection = tempSearch.group(1)
                if len(parsed) == 0:
                    return data
                continue
            except AttributeError:
                pass

            if cSection == "General" and line.startswith("AudioFilename"):
                parsed.remove("AudioFilename")
                line = line.split(":")
                data.update({"AudioFilename":line[1].strip()})
            elif cSection == "Metadata" or cSection == "Difficulty":
                line = line.split(":")
                try:
                    data.update({line[0].strip():line[1].strip()})
                except IndexError:
                    print("line" + str(line))
                try:
                    parsed.remove(cSection)
                except:
                    pass

            








# reads the full file ready to be parsed
def fullParse():


    print("Parse")
