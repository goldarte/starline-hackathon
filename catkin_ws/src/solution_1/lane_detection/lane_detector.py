#!/usr/bin/env python
import cv2
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from dynamic_reconfigure.server import Server
from solution_1.cfg import lane_detector_Config

class ThresholdParams:

    params_default_dict = {
        "function": 1,
        "max_val": 255,
        "thr_val": 127,
        "thr_type": cv2.THRESH_BINARY,
        "thr_type_flag": 0,
        "a_thr_type": cv2.THRESH_BINARY,
        "a_thr_method": cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        "a_thr_blocksize": 11,
        "a_thr_C": 2,
    }

    def __init__(self):
        for key, value in self.params_default_dict.items():
            setattr(self, key, value)

cv_bridge = CvBridge()
thr_params = ThresholdParams()
last_image = None

def image_callback(msg):
    global last_image
    last_image = msg

def dyn_param_callback(dyn_params, level):
    for key, value in dyn_params.items():
        setattr(thr_params, key, value)
    print(thr_params.thr_val)
    return dyn_params

def threshold(cv2_image, thr_params):
    try:
        if thr_params.function == 0:
            _, thr_image = cv2.threshold(cv2_image, thr_params.thr_val, thr_params.max_val, thr_params.thr_type+thr_params.thr_type_flag)
        elif thr_params.function == 1:
            thr_image = cv2.adaptiveThreshold(cv2_image, thr_params.max_val, thr_params.a_thr_method, thr_params.a_thr_type, thr_params.a_thr_blocksize, thr_params.a_thr_C)
    except cv2.error as e:
        rospy.logerr("Can't threshold image. Error: {}".format(e))
        return cv2_image
    return thr_image

if __name__ == "__main__":
    rospy.init_node('lane_detector')
    srv = Server(lane_detector_Config, dyn_param_callback)

    _ns = rospy.get_namespace()
    _rate = rospy.get_param('~rate', 30.0)

    image_sub = rospy.Subscriber('image_raw', Image, image_callback)
    image_pub = rospy.Publisher('threshold', Image, queue_size=1)

    rate = rospy.Rate(_rate)

    while not rospy.is_shutdown():
        rate.sleep()

        if last_image is None:
            continue

        header = last_image.header

        last_image_cv2 = cv_bridge.imgmsg_to_cv2(last_image)

        gray = cv2.cvtColor(last_image_cv2, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)

        th = threshold(blur, thr_params)

        if image_pub.get_num_connections() > 0:
            m = cv_bridge.cv2_to_imgmsg(th)
            m.header.stamp.secs = header.stamp.secs
            m.header.stamp.nsecs = header.stamp.nsecs
            image_pub.publish(m)

    '''
    matrix, distortions = get_matrix_and_distortions_ros(args.namespace+'/camera_info')

    print matrix
    print distortions

    image_sub = rospy.Subscriber(args.namespace+'/image_raw', Image, image_callback)
    '''