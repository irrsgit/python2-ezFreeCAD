#!/usr/bin/env python2
from __future__ import division
FREECADPATH = '/usr/lib/freecad' # path to your FreeCAD.so or FreeCAD.dll file
import sys
sys.path.append(FREECADPATH)
import FreeCAD
import Part
import importDXF
mydoc = FreeCAD.newDocument("mydoc")


# returns a rectangular face given x and y dims
def rectangle(xDim,yDim):
    return Part.makePlane(xDim,yDim)

# reutns a circular face given a radius
def circle(radius):
    circEdge = Part.makeCircle(radius)
    circWire = Part.Wire(circEdge)
    circFace = Part.Face(circWire)
    return circFace

# only tested/working with solid+solid and face+face unions
def union(thingA,thingB,tol=1e-5):
    if (thingA.ShapeType == 'Face') and (thingB.ShapeType == 'Face'):
        u = thingA.multiFuse([thingB],tol).removeSplitter().Faces[0]
    elif (thingA.ShapeType == 'Solid') and (thingB.ShapeType == 'Solid'):
        u = thingA.multiFuse([thingB],tol).removeSplitter().Solids[0]
    else:
        u = []
    return u

# TODO: this cut is leaving breaks in circles, try to upgrade it to fuzzy logic with tolerance
# also remove splitter does nothing here
def difference(thingA,thingB):
    if (thingA.ShapeType == 'Face') and (thingB.ShapeType == 'Face'):
        d = thingA.cut(thingB).removeSplitter().Faces[0]
    elif (thingA.ShapeType == 'Solid') and (thingB.ShapeType == 'Solid'):
        d = thingA.cut(thingB).removeSplitter().Solids[0]
    else:
        d = []
    return d

# sends a projection of an object's edges onto the z=0 plane to a dxf file
def save2DXF (thing,outputFilename):
    tmpPart = mydoc.addObject("Part::Feature")
    tmpPart.Shape = thing
    importDXF.export([tmpPart], outputFilename)
    mydoc.removeObject(tmpPart.Name)
    return

# sends a solid object to a step file
def solid2STEP (solid,outputFilename):
    solid.exportStep(outputFilename)
    return

# extrudes a face to make a 3d solid
def extrude (face,direction):
    return face.extrude(FreeCAD.Vector(direction))

# moves an object
def translate (obj,direction):
    tobj = obj.copy()
    tobj.translate(FreeCAD.Vector(direction))
    return tobj

# given a solid and a z value, returns a set of edges 
def section (solid,height="halfWay"):
    bb = solid.BoundBox
    if height == "halfWay":
        zPos = bb.ZLength/2
    else:
        zPos = height
    slicePlane = rectangle(bb.XLength, bb.YLength)
    slicePlane.translate(FreeCAD.Vector(bb.XMin,bb.YMin,zPos))
    sectionShape = solid.section(slicePlane)
    return sectionShape

