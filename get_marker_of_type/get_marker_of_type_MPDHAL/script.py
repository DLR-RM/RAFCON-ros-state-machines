import rospy
import tf
from geometry_msgs.msg import Pose, Quaternion

from visualization_msgs.msg import MarkerArray, Marker


def execute(self, inputs, outputs, gvm):

    marker_list = inputs["marker_list"]
    marker_type = inputs["type"]

    self.logger.debug("Get object of type %s" % str(marker_type))
    
    # the last marker of the requested type is the best fit
    marker_of_type_found = False
    
    for marker in marker_list:
        if marker.type == marker_type:
            p = marker.pose
            numpy_quaternion = [p.orientation.x, p.orientation.y, p.orientation.z, p.orientation.w]
            euler = list(tf.transformations.euler_from_quaternion(numpy_quaternion, "sxyz"))
            outputs["euler_pose"] = [p.position.x, p.position.y, p.position.z, euler[0], euler[1], euler[2]]
            marker_of_type_found = True

    if marker_of_type_found:
        self.logger.info("Marker of requested type found!")
        return 0

    self.logger.error("NO marker of requested type found!")
    return 1
