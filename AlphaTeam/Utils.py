import math

def getDistance(x1,y1,x2,y2):
        heading_x = x2-x1
        heading_y = y2-y1
        return(math.sqrt((heading_x*heading_x) + (heading_y*heading_y)))

def getAng(x1,y1,x2,y2):
        t1 = math.atan2(y1-y2, x1-x2)
        t1 = (t1*180)/math.pi
        t1 = (t1-360)%360
        return(360-t1)
