= Packages =

== dymo-cups-drivers-1.2.0.tar.gz ==

This is Dymos' CUPS Driver including support for the LabelWriter 450.

=== Installation ===

tar xfvz dymo-cups-drivers-1.2.0.tar.gz
cd dymo-cups-drivers-1.2.0
patch -p1 < ../dymo-cups-drivers-1.2.0-stdlib.patch
./configure  --datadir=/usr --prefix=/usr --localstatedir=/var --sysconfdir=/etc
make
sudo make install
