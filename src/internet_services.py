#!/usr/bin/env python
#
#Copyright (C) 2012 Thecorpora SL
#
#This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import roslib; roslib.load_manifest('qbo_internet_services')
import rospy
from qbo_internet_services.srv import InternetService

import httplib


def server_request(server,url,method="GET"):
    connection = httplib.HTTPConnection(server)
    connection.request(method,url)
    resp=connection.getresponse()
    print "Server:"+server+"|method:"+method+"|url:"+url
    if resp.status==200:
        result=resp.read()
        print "Remote response:"+result
    else:
        print "Server:"+server+"|method:"+method+"|url:"+url
        print "Status:"+resp.status
        print "Reason:"+resp.reason
        result=-1
    return result

def geoip_Location():
    location=server_request("api.hostip.info","/get_html.php")
    location_split=location.split('\n');
    for component in location_split:
        component_split=component.split(": ")
        if component_split[0]=="Country":
            country=component_split[1]
        elif component_split[0]=="City":
            city=component_split[1]

    formated_loc=city+"|"+country
    return formated_loc
    
 
def handle_service(req):
    print "Service called:"+req.service
    print "Param1:"+req.param1
    if req.service=="location":
        response="1"
        response=geoip_Location()
    else:
        print "Service doesn't exist"
        response="-1"
    print "Processed response:"+response
    return response

def init_server():
    rospy.init_node('Internet_Services')
    s = rospy.Service('/internetservices', InternetService, handle_service)
    rospy.spin()

if __name__ == "__main__":
    init_server()

