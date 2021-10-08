import re

import config


# only reads the necessary data for viewing the beatmap not playing
#returns a tuple containing (metadata, diff data, audiofile, bgfile)
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
            
            
# reads the full file ready to be parsed
def fullParse(beatmapPath):

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
                combo += 1
                tempObj = [i.strip() for i in line.split(",")]
                tempHitObject = [int(int(tempObj[0])*config.CURRENT_SCALING), int(int(tempObj[1])*config.CURRENT_SCALING), int(tempObj[2])]
                #print(tempHitObject)
                #print(tempObj)
                osType = "{0:b}".format(int(tempObj[3]))
                osType = osType[::-1]
                objectParams = []
                for i in range(len(osType)):
                    if osType[i] == "1":
                        objectParams.append(i)
                tempHitObject.append(objectParams)
                tempHitObject.append(combo)
                if 2 in objectParams:
                    combo = 1
                if 1 in objectParams:
                    # create data
                    sliderData = []
                    # split into temp data
                    tempSliderData = tempObj[5::]
                    # split the slider into it's type and points
                    sliderPoints = tempSliderData[0].split("|")
                    sliderData.append(sliderPoints.pop(0))
                    points = []
                    for point in sliderPoints:
                        pTemp = (point.split(":"))
                        points.append((int(int(pTemp[0])*config.CURRENT_SCALING), int(int(pTemp[1])*config.CURRENT_SCALING)))
                    sliderData.append(points)
                    #print(sliderData)
                    tempHitObject.append(sliderData)
                print(tempHitObject)
                hitObjects.append(tempHitObject)


    return hitObjects

            

        
    
