# FreeFi

Temp dev notes from Steve:
- wifite was very helpful in helping understand some of the gotchas around setting up the wifi device

- Renamed to FreeFi and set the !# bash interpreter line so it will auto-use python when running FreeFi like an executable, you might need to chmod +x it if exe bit not set

- THIS THIS THIS It looks like NetworkManager by default in Kali anonymizes and changes the mac address of at least the wifi card automatically every few minutes which is a problem as it conflicts with
our spoofing. Adding file /etc/NetworkManager/conf.d/{anyname}.conf to stop NetworkManager from changing mac addr constantl with contents:

[device]
wifi.scan-rand-mac-address=no

[connection]
ethernet.cloned-mac-address=preserve
wifi.cloned-mac-address=preserve

then 'service network-manager restart' if necessary

- IGNORE: might going to have to run airmon-ng check kill to kill things that interefere with our wireless tool, to restart wifi services after our tool run we might need to do:
service network-manager restart
service NetworkManager restart
service avahi-daemon restart
after adapter switched out of monitor mode
alternatively, might kill each bad process by PID and restart

- airmon-ng check kill 

- ethtool -P wlan0   to get permanent mac address

- airodumo power levels are negative, numbers closer to 0 have greater strength except for -1 which means
  either access point doesn't support signal level reporting OR client out of range
  