#!/usr/bin/env python

import rospy
import os
from cairclient_alterego_base.srv import GestureService, GestureServiceResponse
import rospkg
import yaml
from rosbag.bag import Bag

rp = rospkg.RosPack()
package_path = rp.get_path('cairclient_alterego_base')
folder_path = package_path + "/bag"


def handle_gesture_service(req):
    filename = req.filename
    filename = os.path.join(folder_path, req.filename)
    offset = req.offset
    gesture_duration = req.gesture_duration

    rospy.loginfo("Received service request: %s, %f, %f", filename, offset, gesture_duration)

    info_dict = yaml.load(Bag(filename, 'r')._get_yaml_info())
    rosbag_duration = info_dict["duration"]

    remaining_time = gesture_duration
    while remaining_time > 0:
        if remaining_time < (rosbag_duration - offset):
            play_time = remaining_time - offset
        else:
            play_time = rosbag_duration - offset
        os.system("rosbag play -s {} -u {} {}".format(offset, play_time, filename))
        remaining_time = remaining_time - play_time
        offset = (offset + play_time) % rosbag_duration

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
