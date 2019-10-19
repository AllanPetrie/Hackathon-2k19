import math

def getDistance(p1,p2):
        heading_x = p2[0] - p1[0]
        heading_y = p2[1] - p1[1]
        return(math.sqrt((heading_x*heading_x) + (heading_y*heading_y)))

def getAng(p1,p2):
        t1 = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
        t1 = t1*(180/math.pi)
        t1 = (t1-360)%360
        return(360-t1)

