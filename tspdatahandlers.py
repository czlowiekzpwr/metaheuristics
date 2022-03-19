import numpy as np


def nodeCoord(spec, file):
    nodesnum = int(spec["DIMENSION"])

    if "NODE_COORD_TYPE" in spec:
        if spec["NODE_COORD_TYPE"] == "NO_COORDS":
            raise ValueError()
        elif spec["NODE_COORD_TYPE"] == "TWOD_COORDS":
            nodescoords = np.empty((nodesnum, 2), dtype=np.float64)
        elif spec["NODE_COORD_TYPE"] == "THREED_COORDS":
            nodescoords = np.empty((nodesnum, 3), dtype=np.float64)
    else:
        nodescoords = np.empty((nodesnum, 2), dtype=np.float64)

    
    for i in range(nodesnum):
        inline = file.readline().split()
        for dim in range(nodescoords.shape[1]):
            nodescoords[int(inline[0])-1][dim] = float(inline[dim+1])
    return nodescoords

def fixedEdges(spec, file):
    fixededges = []
    reading = True
    while reading:
        inline = file.readline().split()
        if int(inline[0]) == -1:
            reading = False
            break
        else:
            fixededges.append((int([inline[0]], int(inline[1]))))
    return fixededges

def displayData(spec, file):
    if spec["DISPLAY_DATA_TYPE"] != "TWOD_DISPLAY":
        raise ValueError()

    nodesnum = int(spec["DIMENSION"])
    nodesdisplay = np.empty((nodesnum, 2), dtype=np.float64)
    
    for i in range(nodesnum):
        inline = file.readline().split()
        for dim in range(nodesdisplay.shape[1]):
            nodesdisplay[int(inline[0])-1][dim] = float(inline[dim+1])
    return nodesdisplay

def tourData(spec, file):
    tours = []
    curtour = []
    reading = True
    while reading:
        inline = [int(x) for x in file.readline().split()]
        for x in range(len(inline)):
            if inline[x] == -1:
                if len(curtour) > 0:
                    tours.append(curtour)
                curtour = []
                if x != len(inline)-1:
                    continue
                curfpos = file.tell()
                nextline = file.readline()
                file.seek(curfpos)
                try:
                    testint = int(nextline.split()[0])
                except (ValueError):
                    reading = False
                    break
            else:
                curtour.append(inline[x])
    return tours

def edgeWeigths(spec, file):
    nodesnum = int(spec["DIMENSION"])
    weighttype = spec["EDGE_WEIGHT_FORMAT"]
    result = np.empty((nodesnum, nodesnum), dtype=np.uint64)
    if weighttype == "LOWER_DIAG_ROW":
        toread = (nodesnum*(nodesnum+1))/2
    elif weighttype == "FULL_MATRIX":
        toread = nodesnum*nodesnum
    loaded = 0
    xcoord = 0
    ycoord = 0
    while loaded < toread:
        inline = [int(x) for x in file.readline().split()]
        for num in inline:
            result[xcoord][ycoord] = num
            if weighttype == "LOWER_DIAG_ROW":
                result[ycoord][xcoord] = num
            loaded += 1
            xcoord += 1
            if weighttype == "LOWER_DIAG_ROW" and xcoord > ycoord:
                xcoord = 0
                ycoord += 1
            if weighttype == "FULL_MATRIX" and xcoord == nodesnum:
                xcoord = 0
                ycoord += 1
    return result
            
section_fmap = {
    "NODE_COORD_SECTION": nodeCoord,
    "FIXED_EDGES_SECTION": fixedEdges,
    "DISPLAY_DATA_SECTION": displayData,
    "TOUR_SECTION": tourData,
    "EDGE_WEIGHT_SECTION": edgeWeigths
}
