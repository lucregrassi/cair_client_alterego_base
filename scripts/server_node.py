#!/usr/bin/env python

import rospy
import os
import random
from cairclient_alterego_base.srv import GestureService, GestureServiceResponse
import rospkg
import time

rp = rospkg.RosPack()
package_path = rp.get_path('cairclient_alterego_base')
folder_path = package_path + "/bag" 

def handle_gesture_service(req):
	filename = req.filename
	filename = os.path.join(folder_path, req.filename)
	offset = req.offset
	duration = req.duration
	
	rospy.loginfo("Received service request: %s, %f, %f", filename, offset, duration)
	
	elapsed_time = 0
	while(elapsed_time < duration):
		start = time.time()
		os.system("rosbag play -s {} -u {} {}".format(offset, duration, filename))
		end = time.time()
		elapsed_time = end-start-0.5
		if(elapsed_time < duration):
			offset = 0.0
			duration = duration - elapsed_time
		else:
			offset = elapsed_time	

	rospy.loginfo("Server processing complete: new offset %f", offset)
    # The server returns a boolean
	return offset

def gesture_service_server():
	rospy.init_node('gesture_service_server', anonymous=True)
	service = rospy.Service('gesture_service', GestureService, handle_gesture_service)
	rospy.loginfo("Gesture service server is ready.")
	rospy.spin()

if __name__ == '__main__':
	gesture_service_server()

