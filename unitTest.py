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
osThingy2 = osThingy
osThingy2 = translate(osThingy2, 70, 0, 0)
osThingys = [osThingy,osThingy2]
osThingys = translate(osThingys, 0, 10, 0)

thingySlice = section(osThingys[0])
save2DXF(thingySlice, "osThingySlice.dxf")

solid2STEP(osThingys[0], "osThingy.step")
solid2STEP(osThingys[1], "osThingy2.step")

osThingy3 = STEP2Solid("osThingy.step")

osThingys = circArray(osThingy, 3, 0, -50, 0, 0, 0, 1)

solid2STEP(osThingys[0], "osThingyA.step")
solid2STEP(osThingys[1], "osThingyB.step")
solid2STEP(osThingys[2], "osThingyC.step")