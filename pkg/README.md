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
make distclean

Now install the printer on your machine.
To access CUPS remotely:

ssh -L 6311:localhost:631 <remote_ip>

Point your browser to: http://localhost:6311

Add printer, username is the regular user you used to install the machine.

After sucessfully configuring the Printer Make sure it's either Default OR get it's name to print afterwards:

$ sudo cat /etc/cups/printers.conf |grep \<Printer
<Printer DYMO_LabelWriter_450>

…

(lpr -P DYMO_LabelWriter_450 … )
