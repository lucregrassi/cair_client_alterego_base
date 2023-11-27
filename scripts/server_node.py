#!/usr/bin/env python

import rospy
import os
import random
from cairclient_alterego_base.srv import GestureService, GestureServiceResponse
import rospkg
import time
import yaml
import math
from rosbag.bag import Bag


rp = rospkg.RosPack()
package_path = rp.get_path('cairclient_alterego_base')
folder_path = package_path + "/bag" 

def handle_gesture_service(req):
	filename = req.filename
	filename = os.path.join(folder_path, req.filename)
	offset = req.offset
	duration = req.duration
	
	rospy.loginfo("Received service request: %s, %f, %f", filename, offset, duration)
	
	info_dict = yaml.load(Bag(filename, 'r')._get_yaml_info())
	rosbag_duration = info_dict["duration"]
	
	# compute how many times should i reproduce the rosbag
	n_loops = math.ceil((offset + duration)/rosbag_duration)
	if n_loops == 1:
		os.system("rosbag play -s {} -u {} {}".format(offset, duration, filename))
		offset = offset + duration
	else:
		for i in range(0, n_loops-1):
			os.system("rosbag play {}".format(filename))
		offset = duration - (rosbag_duration-offset) - rosbag_duration*(n_loops-2)
		duration = offset
		os.system("rosbag play -s {} -u {} {}".format(offset, duration, filename))
		

	rospy.loginfo("Server processing complete: new offset %f", offset)
    # The server returns a boolean
	return offset

def gesture_service_server():
	rospy.init_node('gesture_service_server', anonymous=False)
	service = rospy.Service('gesture_service', GestureService, handle_gesture_service)
	rospy.loginfo("Gesture service server is ready.")
	rospy.spin()

if __name__ == '__main__':
	gesture_service_server()

