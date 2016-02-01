from __future__ import division
from __init__ import *

myCone = cone(10, 0, 30)
mySphere = sphere(10)
mySphere = translate(mySphere,0,0,25)
pawn = union(myCone,mySphere)
pawn = rotate(pawn,-90,0,0)
myCircle = circle(25)
myDisc = extrude(myCircle,0,0,-15)
#myDisc = rotate(myDisc,-90,0,0)
myDisc = translate(myDisc,0,25,3)
osThingy = difference(myDisc, pawn)
background = roundedRectangle(50, 50,r=(2,5,0,0))
background = extrude(background, 0, 0, -5)
background = translate(background, -25, 0, -15+3+2)
osThingy = union(osThingy, background)

solid2STEP(osThingy, "osThingy.step")

osThingy2 = STEP2Solid("osThingy.step")