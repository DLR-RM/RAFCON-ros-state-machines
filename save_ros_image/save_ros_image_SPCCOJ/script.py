# From http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython

import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def execute(self, inputs, outputs, gvm):
    
    topic = inputs["topic"]
    format = inputs["format"]
    filename = inputs["filename"]
    
    try:
        image = rospy.wait_for_message(topic, Image, timeout=10)
        bridge = CvBridge()
        cv_image = bridge.imgmsg_to_cv2(image, format)
        cv2.imwrite(filename, cv_image)
    except(rospy.ROSException), e:
        self.logger.error("Image topic " + topic + " not available, aborting...")
        return -1
    
    self.logger.info("Sucessfully written image from " + topic + " to " + filename + " in " + format)
    
    return 0
