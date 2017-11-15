"""
This is the main file of our project
"""


"""
This function returns a list of dictionaries corresponding to an access point
"""
def find_access_points () :

"""
This function finds the access points that are not using WPS for authentication
"""
def filter_non_wps (aps) :

"""
This function finds the devices connected to specfic access point
"""
def find_connected_devices (ap) :

"""
This function spoofs a mac address and tries to connect to Google without a redirect
"""
def connect (mac) : 


access_points = find_access_points()
filtered_access_points = filter_non_wps(access_points)
connected = False

for ap in filtered_access_points :
    devices = find_connected_devices(ap)
    for dev in devices :
        if connect(dev) :
            connected = True
            break
    if connected :
        break
else :
    #couldn't find a connected user