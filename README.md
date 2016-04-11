# ezFreeCAD
Python wrapper for interfacing with FreeCAD it make it easier to draw 3D objects programmatically

## Installation

### Ubuntu
#### 15.10
NOTE: THIS DOES NOT WORK (ubuntu needs opencascade)
This library uses a fairly new feature in FreeCAD (the multiFuse attribute of Part.TopoShape). At the time of this writing (April 2016) the version of FreeCAD in ubuntu 15.10 is too old. This can be fixed by insalling some packages from some of the freecad-maintainers' ppas:
```
sudo add-apt-repository ppa:freecad-maintainers/freecad-daily
sudo add-apt-repository 'deb http://ppa.launchpad.net/freecad-maintainers/oce-release/ubuntu vivid main'
sudo apt-get update #<-- update your package lists
sudo apt-get upgrade #<-- upgrade any packages that might have been impacted by the new software sources you added
sudo apt-get install python2.7 python-pip git freecad #<-- install the prerequisites
pip2 install --upgrade git+https://github.com/AFMD/ezFreeCAD.git #<-- install this library
```
## Usage
The FreeCAD python module must be imported before `import ezFreeCAD` will work.  
`import FreeCAD` will import this module directly from the FreeCAD.so (FreeCAD.dll in Windows) file that's distributed with your FreeCAD package. The only catch here is that the directory containing your FreeCAD.so or FreeCAD.dll file must be in your `sys.path` python variable before you try to `import FreeCAD`.  
Here are some of the default locations for the FreeCAD.so file that I'm aware of:  

OS | Directory containing FreeCAD.so
---|---
Ubuntu | /usr/lib/freecad/lib
Arch | /usr/lib/freecad

See [unitTest.py](/unitTest.py) for example usage, or add something like
```python
import sys
sys.path.append('/usr/lib/freecad') # path to directory containing your FreeCAD.so or FreeCAD.dll file
import FreeCAD
import ezFreeCAD
```
to your script and start using the functions defined [here](/ezFreeCAD/__init__.py) in your script.

## Hacking
```bash
git clone https://github.com/AFMD/ezFreeCAD.git
cd ezFreeCAD
# do hacking here
python2 setup.py install #<--install your hacked package
./unitTest.py #<--test your hacks
```
