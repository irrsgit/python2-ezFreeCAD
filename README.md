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
sudo apt-get install tcl-vtk6 ftgl-dev libvtk6-dev tk-dev libxmu-dev mesa-common-dev libxi-dev autoconf libtool automake libgl2ps-dev quilt libtbb-dev libfreeimage-dev cmake devscripts
wget https://users.physics.ox.ac.uk/~christoforo/opencascade/src-tarballs/opencascade-6.9.1.tgz
tar -xvf opencascade-*.tgz
cd opencascade-*
sed -i -e '$aINCLUDE(CPack)' CMakeLists.txt
mkdir -p build
cd build
flags=""
flags="$flags -DCMAKE_BUILD_TYPE=Release"
flags="$flags -DCPACK_PACKAGE_VERSION_MAJOR=6"
flags="$flags -DCPACK_PACKAGE_VERSION_MINOR=9"
flags="$flags -DCPACK_PACKAGE_VERSION_PATCH=1"
#flags="$flags -DINSTALL_PREFIX=/usr"
#flags="$flags -DINSTALL_LIB_DIR=lib/"'$(DEB_HOST_MULTIARCH)'
#flags="$flags -DCMAKE_PLATFORM_IMPLICIT_LINK_DIRECTORIES=/lib/"'$(DEB_HOST_MULTIARCH)'";/usr/lib/"'$(DEB_HOST_MULTIARCH)'
flags="$flags -DINSTALL_DIR=/opt/occt"
#flags="$flags 3RDPARTY_VTK_INCLUDE_DIR=/opt/vtk6/include"
#flags="$flags 3RDPARTY_VTK_LIBRARY_DIR=/opt/vtk6/lib"
#flags="$flags -DUSE_GL2PS=ON"
#flags="$flags -DUSE_FREEIMAGE=ON"
#flags="$flags -DUSE_TBB=ON"
#flags="$flags -DUSE_VTK=ON"
#flags="$flags -DUSE_TBB=OFF"
#flags="$flags -DUSE_TBB=ON"
cmake $flags ..
make -j4 #<-- "-j4" directs the system to use four compilation threads (don't use more than your number of logical CPU cores)
cpack -D CPACK_GENERATOR="DEB" -D CPACK_PACKAGE_CONTACT="none"
sudo dpkg -i OCCT-*.deb
sudo su -c 'echo "source /opt/occt/env.sh" > /etc/profile.d/occt.sh'
source /opt/occt/env.sh

cd ..
apt-get source freecad
#sudo apt-get build-dep freecad
cd freecad-*
sed -i '/liboce-foundation-dev,/d' debian/control
sed -i '/liboce-modeling-dev,/d' debian/control
sed -i '/liboce-ocaf-dev,/d' debian/control
sed -i '/liboce-visualization-dev,/d' debian/control
sed -i '/oce-draw,/d' debian/control
mk-build-deps
sudo dpkg -i freecad-build-deps* #<-- Errors here, that's fine we'll fix them in the next step
sudo apt-get -f install
sed -i 's,-DOCC_INCLUDE_DIR="/usr/include/oce" \\,-DOCC_INCLUDE_DIR="/opt/occt/inc" \\\n-DOCC_LIBRARY_DIR="/opt/occt/lin64/gcc/lib" \\,g' debian/rules
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
