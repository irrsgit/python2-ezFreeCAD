#!/usr/bin/env python2
import FreeCAD
import Part
import importDXF
mydoc = FreeCAD.newDocument("mydoc")

def cylinder (radius,height):
    return Part.makeCylinder(radius,height)

def sphere(radius):
    return Part.makeSphere(radius)

def cone(r1,r2,height):
    return Part.makeCone(r1,r2,height)

# returns a rectangular face given x and y dims
def rectangle(xDim,yDim):
    return Part.makePlane(xDim,yDim)

# returns a circular face given a radius
def circle(radius):
    circEdge = Part.makeCircle(radius)
    circWire = Part.Wire(circEdge)
    circFace = Part.Face(circWire)
    return circFace

# r can accept a salar or a list or tuple with 4 radii
def roundedRectangle(xDim,yDim,r=None):
    if r is None:
        radii=(0,0,0,0)
    elif (type(r) is float) or (type(r) is int):
        radii=(r,r,r,r)
    elif (type(r) is list) or (type(r) is tuple) and len(r) is 4:
        radii=(r[0],r[1],r[2],r[3])
    else:
        print("Invalid value for r in roundedRectangle function")
        return None
    if (radii[0] + radii[3] > xDim) or (radii[1] + radii[2] > xDim) or (radii[0] + radii[1] > yDim) or (radii[3] + radii[2] > yDim):
        print("This rounded rectangle is impossible to draw!")
        return None
    
    p0 = FreeCAD.Vector(radii[0],yDim,0)
    p1 = FreeCAD.Vector(xDim-radii[1],yDim,0)
    p2 = FreeCAD.Vector(xDim,yDim-radii[1],0)
    p3 = FreeCAD.Vector(xDim,radii[2],0)
    p4 = FreeCAD.Vector(xDim-radii[2],0,0)
    p5 = FreeCAD.Vector(radii[3],0,0)
    p6 = FreeCAD.Vector(0,radii[3],0)
    p7 = FreeCAD.Vector(0,yDim-radii[0],0)
    
    polygonWire=Part.makePolygon([p0,p1,p2,p3,p4,p5,p6,p7],True)
    polygonFace=Part.Face(polygonWire)
    
    circles = []
    if radii[0]>0:
        circles.append(translate(circle(radii[0]),radii[0],yDim-radii[0],0))
    if radii[1]>0:
        circles.append(translate(circle(radii[1]),xDim-radii[1],yDim-radii[1],0))    
    if radii[2]>0:
        circles.append(translate(circle(radii[2]),xDim-radii[2],radii[2],0))  
    if radii[3]>0:
        circles.append(translate(circle(radii[3]),radii[3],radii[3],0))  
    
    if len(circles) > 0:
        roundedGuy = polygonFace.multiFuse(circles,1e-5).removeSplitter().Faces[0]
    else:
        roundedGuy = polygonFace;

    return roundedGuy

# only tested/working with solid+solid and face+face unions
def union(thingA,thingsB,tol=1e-5):
    if type(thingsB) is not list:
        thingsB = [thingsB]
    if (thingA.ShapeType == 'Face') and (thingsB[0].ShapeType == 'Face'):
        u = thingA.multiFuse(thingsB,tol).removeSplitter().Faces[0]
    elif (thingA.ShapeType == 'Solid') and (thingsB[0].ShapeType == 'Solid'):
        u = thingA.multiFuse(thingsB,tol).removeSplitter().Solids[0]
    else:
        u = []
    return u

# TODO: this cut is leaving breaks in circles, try to upgrade it to fuzzy logic with tolerance
# also I think remove splitter does nothing here
def difference(thingsA,thingsB):
    if type(thingsA) is not list:
        thingsA = [thingsA]    
    if type(thingsB) is not list:
        thingsB = [thingsB]
    
    robjs=[]
    for thingA in thingsA:
        d = thingA
        for thingB in thingsB:
            if (d.ShapeType == 'Face') and (thingB.ShapeType == 'Face'):
                d = d.cut(thingB).removeSplitter().Faces[0]
            elif (d.ShapeType == 'Solid') and (thingB.ShapeType == 'Solid'):
                d = d.cut(thingB).removeSplitter().Solids[0]
            else:
                return []
        robjs.append(d)
    if len(robjs) is 1:
        return robjs[0]
    else:
        return robjs    
    return d

# sends a projection of an object's edges onto the z=0 plane to a dxf file
def save2DXF (thing,outputFilename):
    tmpPart = mydoc.addObject("Part::Feature")
    tmpPart.Shape = thing
    importDXF.export([tmpPart], outputFilename)
    mydoc.removeObject(tmpPart.Name)
    return

# sends a solid object to a step file
def solid2STEP (solids,outputFilenames):
    if type(solids) is not list:
        solids=[solids]
        outputFilenames=[outputFilenames]
    for i in range(len(solids)):
        solids[i].exportStep(outputFilenames[i])
    return

# sends a solid object(or list of objects) to a stl file(s)
def solid2STL (solids,outputFilenames):
    if type(solids) is not list:
        solids=[solids]
        outputFilenames=[outputFilenames]
    for i in range(len(solids)):
        solids[i].exportStl(outputFilenames[i])
    return

# loads a file(or a list of filenames) (probably handles things other than just STEP) and returns a solid shape
def STEP2Solid(stepFilenames):
    if type(stepFilenames) is not list:
            stepFilenames=[stepFilenames]
    robjs=[]
    for stepFilename in stepFilenames:
        robjs.append(Part.read(stepFilename))
    if len(robjs) is 1:
        return robjs[0]
    else:
        return robjs

# extrudes a face (or list of faces) to make a 3d solid
def extrude (objs,x,y,z):
    if type(objs) is not list:
        objs=[objs]
    robjs=[]
    for obj in objs:
        robjs.append(obj.extrude(FreeCAD.Vector((x,y,z))))
    if len(robjs) is 1:
        return robjs[0]
    else:
        return robjs

# mirrors an object (or a list of objects) across a plane defined by a point and a vector
def mirror(objs,x,y,z,dirx,diry,dirz):
    if type(objs) is not list:
        objs=[objs]
    robjs=[]
    for obj in objs:
        robjs.append(obj.mirror(FreeCAD.Vector(x,y,z),FreeCAD.Vector(dirx,diry,dirz)))
    if len(robjs) is 1:
        return robjs[0]
    else:
        return robjs

# makes a circular array of objects around a point [px,py,pz]
# in a plane perpindicular to [dx,dy,dz]
def circArray(obj,n,px,py,pz,dx,dy,dz,fillAngle=360,startAngle=0):
    dTheta=fillAngle/n
    obj0 = obj.copy()
    if startAngle is not 0:
        obj0.rotate(FreeCAD.Vector(px,py,pz),FreeCAD.Vector(dx,dy,dz),dTheta-startAngle)
    objects=[obj0]
    for i in range (1,n):
        newObj= obj.copy()
        newObj.rotate(FreeCAD.Vector(px,py,pz),FreeCAD.Vector(dx,dy,dz),i*dTheta+startAngle)
        objects.append(newObj)
    return objects

# moves an object or a list of objects
def translate (objs,x,y,z):
    if type(objs) is not list:
        objs=[objs]
    robjs=[]
    for obj in objs:
        robj=obj.copy()
        robj.translate(FreeCAD.Vector((x,y,z)))
        robjs.append(robj)
    if len(robjs) is 1:
        return robjs[0]
    else:
        return robjs
    
# rotate (an) object(s) around a point: [px,py,pz]
# xDeg, yDeg and zDeg degreees about those axes
def rotate(objs,xDeg,yDeg,zDeg,px=0,py=0,pz=0):
    if type(objs) is not list:
        objs=[objs]
    robjs=[]
    for obj in objs:
        robj = obj.copy()
        robj.rotate(FreeCAD.Vector(px,py,pz),FreeCAD.Vector(1,0,0),xDeg)
        robj.rotate(FreeCAD.Vector(px,py,pz),FreeCAD.Vector(0,1,0),yDeg)
        robj.rotate(FreeCAD.Vector(px,py,pz),FreeCAD.Vector(0,0,1),zDeg)
        robjs.append(robj)
    if len(robjs) is 1:
        return robjs[0]
    else:
        return robjs

# given a solid and a z value, returns a set of edges 
def section (solid,height="halfWay"):
    bb = solid.BoundBox
    if height == "halfWay":
        zPos = bb.ZLength/2.0
    else:
        zPos = height
    slicePlane = rectangle(bb.XLength, bb.YLength)
    slicePlane.translate(FreeCAD.Vector(bb.XMin,bb.YMin,zPos+bb.ZMin))
    sectionShape = solid.section(slicePlane)
    return sectionShape

