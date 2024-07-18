import numpy as np

# update to mt algorithm
def triangle_voxalize(triangle, color):
    trix = []
    triy = []
    triz= []
    triangle = list(triangle)

    #corners of triangle in array formats
    p0 = triangle[0]
    p1 = triangle[1]
    p2 = triangle[2]

    #vectors and the plane of the triangle
    v0 = p1 - p0
    v1 = p2 - p1
    v2 = p0 - p2
    v3 = p2 - p0
    plane = np.cross(v0,v3)

    #minimun and maximun coordinates of the triangle
    for i in range(3):
        trix.append(triangle[i][0])
        triy.append(triangle[i][1])
        triz.append(triangle[i][2])
    minx, maxx = int(np.floor(np.min(trix))), int(np.ceil(np.max(trix)))
    miny, maxy = int(np.floor(np.min(triy))), int(np.ceil(np.max(triy)))
    minz, maxz = int(np.floor(np.min(triz))), int(np.ceil(np.max(triz)))

    #save the points that are inside triangle
    points = []
    point_colour = []
    #go through each point in the box of minimum and maximum x,y,z
    for x in range (minx,maxx+1):
        for y in range(miny,maxy+1):
            for z in range(minz,maxz+1):
                #check the diagnals of each voxel cube if they are inside triangle
                if LinePlaneCollision(triangle,plane,p0,[1,1,1],[x-0.5,y-0.5,z-0.5],[x,y,z]):
                    points.append([x,y,z])
                    point_colour.append(np.mean(color, axis=0))
                elif LinePlaneCollision(triangle,plane,p0,[-1,-1,1],[x+0.5,y+0.5,z-0.5],[x,y,z]):
                    points.append([x,y,z])
                    point_colour.append(np.mean(color, axis=0))
                elif LinePlaneCollision(triangle,plane,p0,[-1,1,1],[x+0.5,y-0.5,z-0.5],[x,y,z]):
                    points.append([x,y,z])
                    point_colour.append(np.mean(color, axis=0))
                elif LinePlaneCollision(triangle,plane,p0,[1,-1,1],[x-0.5,y+0.5,z-0.5],[x,y,z]):
                    points.append([x,y,z])
                    point_colour.append(np.mean(color, axis=0))
                #check edge cases and if the triangle is completly inside the box
                elif intersect(triangle,[x,y,z],v0,p0):
                    points.append([x,y,z])
                    point_colour.append(np.mean(color, axis=0))
                elif intersect(triangle,[x,y,z],v1,p1):
                    points.append([x,y,z])
                    point_colour.append(np.mean(color, axis=0))
                elif intersect(triangle,[x,y,z],v2,p2):
                    points.append([x,y,z])
                    point_colour.append(np.mean(color, axis=0))
    #return the points that are inside the triangle
    # print('points',len(points))
    # print('point_colour',len(point_colour))
    return points, point_colour

def intersect(triangle,point,vector,origin):
    x,y,z = point[0],point[1],point[2]
    origin = np.array(origin)
    #check the x faces of the voxel point
    for xcube in np.arange(x, x+2):
        xcube -= 0.5
        if LinePlaneCollision(triangle,[1,0,0], [xcube,y,z], vector, origin,[x,y,z]):
            return(True)
    for ycube in np.arange(y, y+2):
        ycube -= 0.5
        if LinePlaneCollision(triangle,[0,1,0], [x,ycube,z], vector, origin,[x,y,z]):
            return(True)
    for zcube in np.arange(z, z+2):
        zcube -= 0.5
        if LinePlaneCollision(triangle,[0,0,1], [x,y,zcube], vector, origin,[x,y,z]):
            return(True)

    #check if the point is inside the triangle (in case the whole tri is in the voxel point)
    if origin[0] <= x+0.5 and origin[0] >= x-0.5:
        if origin[1] <= y+0.5 and origin[1] >= y-0.5:
            if origin[2] <= z+0.5 and origin[2] >= z-0.5:
                return(True)

    return(False)

# I modified this file to suit my needs:
# https://gist.github.com/TimSC/8c25ca941d614bf48ebba6b473747d72
#check if the cube diagnals cross the triangle in the cube
def LinePlaneCollision(triangle,planeNormal, planePoint, rayDirection, rayPoint,point, epsilon=1e-6):
    planeNormal = np.array(planeNormal)
    planePoint = np.array(planePoint)
    rayDirection = np.array(rayDirection)
    rayPoint = np.array(rayPoint)


    ndotu = planeNormal.dot(rayDirection)
    if abs(ndotu) < epsilon:
        return(False)

    w = rayPoint - planePoint
    si = -planeNormal.dot(w) / ndotu
    Psi = w + si * rayDirection + planePoint

    #check if they cross inside the voxel cube
    if np.abs(Psi[0]-point[0]) <= 0.5 and np.abs(Psi[1]-point[1]) <= 0.5 and np.abs(Psi[2]-point[2]) <= 0.5:
        #check if the point is inside the triangle and not only on the plane
        if PointInTriangle(Psi, triangle):
            return (True)
    return (False)

# read for explanation
# https://blackpawn.com/texts/pointinpoly#:~:text=A%20common%20way%20to%20check,triangle%2C%20otherwise%20it%20is%20not.
#check if point is inside triangle
def SameSide(p1,p2, a,b):
    cp1 = np.cross(b-a, p1-a)
    cp2 = np.cross(b-a, p2-a)
    if np.dot(cp1, cp2) >= 0:
        return (True)
    return (False)
# used for voxelization
def PointInTriangle(p, triangle):
    a = triangle[0]
    b = triangle[1]
    c = triangle[2]
    if SameSide(p,a, b,c) and SameSide(p,b, a,c) and SameSide(p,c, a,b):
        return (True)
    return (False)
