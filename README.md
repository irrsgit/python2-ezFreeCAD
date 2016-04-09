# ezFreeCAD
Python wrapper for interfacing with FreeCAD it make it easier to draw 3D objects programmatically

## Installation

### Ubuntu
#### 15.10
```
sudo apt-get install python2.7 freecad python-pip git freecad
pip2 install --upgrade git+https://github.com/AFMD/ezFreeCAD.git
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
