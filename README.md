# ezFreeCAD
Python wrapper for interfacing with FreeCAD it make it easier to draw 3D objects programmatically

## Installation

### Windows
1. Install [git](https://git-scm.com/downloads) using the default install options
1. Install [WinPython](https://github.com/winpython/winpython/releases/tag/1.2.20151029) with python 2.7
1. Install the latest release of [FreeCAD](https://github.com/FreeCAD/FreeCAD/releases)
1. In a `WinPython Command Prompt.exe` terminal session, run `pip install --upgrade git+https://github.com/AFMD/ezFreeCAD.git`

### Ubuntu
As it turns out, it's not so "ez" to get this library working in Ubuntu. It requires a version of FreeCAD's geometry kernel that I haven't found packaged for Debian, so you have to build the required geometry kernel and also FreeCAD yourself before you're able to use this project. Here are the steps for that:
#### 15.10
```
mkdir ezFreeCAD-stuff
cd ezFreeCAD-stuff
sudo apt-get install tcl-vtk6 ftgl-dev libvtk6-dev tk-dev libxmu-dev mesa-common-dev libxi-dev autoconf libtool automake checkinstall libgl2ps-dev quilt libtbb-dev libfreeimage-dev cmake
wget https://users.physics.ox.ac.uk/~christoforo/opencascade/src-tarballs/opencascade-6.9.1.tgz
tar -xvf opencascade-*.tgz
cd opencascade-*
sed -i -e '$aINCLUDE(CPack)' CMakeLists.txt
mkdir -p build
cd build
flags=""
flags="$flags -DCMAKE_BUILD_TYPE=Release"
#flags="$flags 3RDPARTY_VTK_INCLUDE_DIR=/opt/vtk6/include"
#flags="$flags 3RDPARTY_VTK_LIBRARY_DIR=/opt/vtk6/lib"
#flags="$flags -DUSE_GL2PS=ON"
#flags="$flags -DUSE_FREEIMAGE=ON"
#flags="$flags -DUSE_TBB=ON"
#flags="$flags -DUSE_VTK=ON"
#flags="$flags -DUSE_TBB=OFF"
#flags="$flags -DUSE_TBB=ON"
cmake $flags ..
#./build_configure
#./configure --with-vtk-include=/usr/include/vtk-6.2 --with-vtk-library=/usr/lib --disable-debug --enable-production #--with-ftgl=/usr/include/FTGL --prefix=/usr --with-tbb-include=/usr/include/tbb --with-tbb-library=/usr/lib #--with-gl2ps=/usr/include --with-freeimage=/usr/include
make -j4 #<-- -j# there specifies how many CPU cores to use for compilation
#checkinstall -D
cpack -D CPACK_GENERATOR="DEB" -D CPACK_PACKAGE_CONTACT="none" -D CPACK_DEBIAN_PACKAGE_VERSION="6.9.1"


cd ..
apt-get source freecad
sudo apt-get build-dep freecad
cd freecad-*
sed -i 's,-DOCC_INCLUDE_DIR="/usr/include/oce" \\,-DOCC_INCLUDE_DIR="/tmp/occt/inc" -DOCC_LIBRARY_DIR="/tmp/occt/lib" \\,g' debian/rules
dpkg-buildpackage -rfakeroot -uc -b
sudo dpkg -i ../freecad_*.deb

sudo apt-get install python2.7 python-pip git
pip2 install --upgrade git+https://github.com/AFMD/ezFreeCAD.git #<-- install this library
```
### Arch
```
pacman -S freecad pip2 git
pip2 install --upgrade git+https://github.com/AFMD/ezFreeCAD.git #<-- install this library
```
## Usage
The FreeCAD python module must be imported before `import ezFreeCAD` will work.  
`import FreeCAD` will import directly from the FreeCAD.so (FreeCAD.dll in Windows) file that's distributed with your FreeCAD package. The only catch here is that the directory containing your FreeCAD.so or FreeCAD.dll file must be in your `sys.path` python variable before you try to `import FreeCAD`.  
Here are some of the default locations for the FreeCAD.so file that I'm aware of:  

OS | Directory containing FreeCAD.so
---|---
Ubuntu | /usr/lib/freecad/lib
Arch | /usr/lib/freecad
Windows | C:\\Users\\${USER}\\Downloads\\FreeCAD_0.17.7451_x64_dev_win\\bin

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
