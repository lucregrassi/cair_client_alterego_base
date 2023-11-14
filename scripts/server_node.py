#!/usr/bin/env python

import rospy
import os
import random
from cairclient_base.srv import GestureService, GestureServiceResponse
import rospkg

rp = rospkg.RosPack()
package_path = rp.get_path('cairclient_base')
folder_path = package_path + "/bag" 

def handle_gesture_service(req):
    rospy.loginfo("Received service request: %s, %f", req.filename, req.duration)
    number = random.randint(0, 10)
    filename = os.path.join(folder_path, req.filename + str(number) + ".bag")
    print(filename)
    os.system("rosbag play -u {} {}".format(req.duration, filename))
    # Process the request (print what was received)
    rospy.loginfo("Server processing complete.")
    # The server doesn't reply, as per your requirement
    return GestureServiceResponse(True)

def gesture_service_server():
    rospy.init_node('gesture_service_server', anonymous=True)
    service = rospy.Service('gesture_service', GestureService, handle_gesture_service)
    rospy.loginfo("Gesture service server is ready.")
    rospy.spin()

if __name__ == '__main__':
    gesture_service_server()

