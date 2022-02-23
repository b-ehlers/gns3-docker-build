# nicer alpine appliance

The alpine appliance has two major annoyances:
- It doesn't stop immediately
- It tries to use localhost for DNS lookup, when no resolver is defined

This appliance fixes that by using two programs:
- dumb-init, see https://github.com/Yelp/dumb-init
- nodnsd

Additionally it adds:
- package busybox-extras, provides dnsd, fakeidentd, ftpd, ftpget, ftpput,
  httpd, inetd, telnet, telnetd, tftp, tftpd and udhcpd.
- creates user gns3, password gns3
