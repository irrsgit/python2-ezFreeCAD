#!/usr/bin/env python2

from __future__ import division
import ezFreeCAD


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
background = roundedRectangle(50, 50,r=(2,5,7,9),drillCorners=(False,True,True,True),ear=True)
background = extrude(background, 0, 0, -5)
background = translate(background, -25, 0, -15+3+2)
osThingy = union(osThingy, background)
osThingy2 = osThingy
osThingy2 = translate(osThingy2, 70, 0, 0)
osThingys = [osThingy,osThingy2]
osThingys = translate(osThingys, 0, 10, 0)

drillCylinder = cylinder(5/2, 300)
drillCylinder = rotate(drillCylinder, 0, 90, 0)
drillCylinder = translate(drillCylinder, -300/2, 50/2, -5)
drillCylinder2 = translate(drillCylinder, 0, 20, 0)
drillCylinders = [drillCylinder, drillCylinder2]

osThingys = difference(osThingys, drillCylinders)

thingySlice = section(osThingys[0])
save2DXF(thingySlice, "osThingySlice.dxf")

sliceReadBack = loadDXF("osThingySlice.dxf") # this writes to a layer named "0"
solid2STEP(sliceReadBack["0"], "sliceWriteout.step")


solid2STEP(osThingys[0], "osThingy.step")
solid2STEP(osThingys[1], "osThingy2.step")

osThingy3 = STEP2Solid("osThingy.step")

osThingys = circArray(osThingy, 3, 0, -50, 0, 0, 0, 1)

solid2STEP(osThingys[0], "osThingyA.step")
solid2STEP(osThingys[1], "osThingyB.step")
solid2STEP(osThingys[2], "osThingyC.step")

# multicut test:

parent= rectangle(10,10)
child1 = translate(rectangle(1,10),1,0,0)
child2 = translate(rectangle(1,10),4,0,0)
child3 = translate(rectangle(10,1),0,5,0)
result = multiCut(parent, [child1,child2,child3])


print "break"
