""" ---------- OSU MODULES ---------- """
import config
import HitObject
""" ---------- PYTHON MODULES ---------- """
import re


"""
Only parses the necessary information for displaying the beatmap
beatmapPath: path to the beatmap
"""
def shallowRead(beatmapPath, basePath):

    # stores the current section of the beatmap that is being parsed
    cSection = ""
    # handles what is left to be parsed
    parsed = ["General","Metadata","Difficulty", "Events"]
    # actual data that will be returned
    data = {}
    with open(beatmapPath, 'r', encoding='utf-8') as cBeatmap:

        # add the path of the beatmap to the data
        data.update({"BasePath":basePath,"osuPath":beatmapPath})

        # loop through all the lines in the beatmap .osu
        for line in cBeatmap:
            # ignore if the line is whitespace
            if line == "\n":
                continue
            # gets the string in between the [] if applicable
            tempSearch = re.search(r"\[([A-Za-z0-9_]+)\]", line)
            # try to get the string
            try:
                # make the previous section the current section
                prevS = cSection
                #update the current section
                cSection = tempSearch.group(1)
                # if events has been parsed then return data
                if prevS == "Events":
                    return data
                # alternatively if all parsed values are gone return data
                if len(parsed) == 0:
                    return data
                continue
            except AttributeError:
                pass
            # if the current section matches one, the data is layed out as dataname:data
            # split the line by ":" and then update the dictionary with the data
            if cSection == "Metadata" or cSection == "Difficulty" or cSection == "General":
                line = line.split(":")
                try:
                    data.update({line[0].strip():line[1].strip()})
                except IndexError:
                    print("line" + str(line))
                try:
                    parsed.remove(cSection)
                except:
                    pass
            # add the background image to the data so that it can be rendered
            elif cSection == "Events" and ".jpg" in line:
                data.update({"BackgroundImage":line.split(",")[2].replace('"','')})
                try:
                    parsed.remove(cSection)
                except:
                    pass

            
"""
Reads all the necessary data for the song to be played
"""
def fullParse(beatmapPath):

    reading = False         # initializes the reading state to false
    cSection = ""           # initializes the current section
    combo = 0               # initializes the current combo

    hitObjects = []         # initializes the hitObjects array

    # open the beatmap file with utf-8 encoding 
    with open(beatmapPath, 'r', encoding='utf-8') as cBeatmap:

        # loop through the .osu file
        for line in cBeatmap:
            # get the value between the [] (if applicable)
            tempSearch = re.search(r"\[([A-Za-z0-9_]+)\]", line)

            try:
                # if there was a value to be found, set it to the current section and skip the line
                cSection = tempSearch.group(1)
                continue
            except:
                # else keep reading
                pass
            # if the line being read is under the HitObjects header
            if cSection == "HitObjects":
                # split the csv
                tempObj = [i.strip() for i in line.split(",")]
                
                # split the bytecode that defines information about the hit object
                osType = "{0:b}".format(int(tempObj[3]))
                # get the type of the hitObject
                osType = osType[::-1]
                # initialize the object parameters
                objectParams = []
                # loop through the values in the type 
                for i in range(len(osType)):
                    # if the index is positive (1)
                    if osType[i] == "1":
                        # add the index to the object parameters
                        objectParams.append(i)
                if 0 in objectParams:                                   # 0 denotes a hit circle object
                    hitObjects.append(HitObject.hitCircle(tempObj))
                elif 1 in objectParams:                                 # 1 denotes a slider object
                    hitObjects.append(HitObject.slider(tempObj))
                elif 3 in objectParams:                                 # 3 denotes a spinner object
                    hitObjects.append(HitObject.spinner(tempObj))
    # return the hit objects array
    return hitObjects

            
"""
Parse the beatmap for use within the 
"""
def aiParse(beatmapPath):

    reading = False
    cSection = ""
    combo = 0

    hitObjects = []


    with open(beatmapPath, 'r', encoding='utf-8') as cBeatmap:

        for line in cBeatmap:
            tempSearch = re.search(r"\[([A-Za-z0-9_]+)\]", line)

            try:
                cSection = tempSearch.group(1)
                continue
            except:
                pass

            if cSection == "HitObjects":
                # split the csv
                tempObj = [i.strip() for i in line.split(",")]
                
                osType = "{0:b}".format(int(tempObj[3]))
                osType = osType[::-1]
                objectParams = []
                for i in range(len(osType)):
                    if osType[i] == "1":
                        objectParams.append(i)
                tempObj = [int(i) for i in tempObj[0:3]]
                if 1 in objectParams:
                    tempObj.append(1)
                else:
                    tempObj.append(0)
                
                if 3 in objectParams:
                    tempObj.append(1)
                else:
                    tempObj.append(0)
                hitObjects.append(tempObj)
    
    return hitObjects
        
    
