#
# DataManager is a class that will provide clients with methods to connect to any data source.
#
import urllib3
import socket
class DataManager(object):

    def __init__(self):
        pass

    # Determines if we're connected to firebase.
    def _IsConnected(self):
        # This method will see if we're connected online.
       try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("firebase.google.com", 80))
        return True
       except OSError:
        return False

