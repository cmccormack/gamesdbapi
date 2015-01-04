import os
import time

API_URL = "http://thegamesdb.net/api/"
query = "GetGame"

local_xml = query + '.xml'

# Check if cached xml exists, retrieved within the last hour

if os.path.isfile(local_xml):
    time_diff = time.time() - os.path.getmtime(local_xml)
    if time_diff < 3600:
        print "Found cached copy of {}, skipping API call. ".format(query),
        print "Last call {} minutes {} seconds ago.".format(
            int(time_diff/60), int(time_diff % 60))

    with open(local_xml) as input_xml:
        return input_xml.read()



# Cache a copy of the XML response locally
with open(local_xml, 'w') as output:
    output.write(query_response + '\n')