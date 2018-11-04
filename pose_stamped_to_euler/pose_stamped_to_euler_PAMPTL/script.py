import tf
from geometry_msgs.msg import PoseStamped

def execute(self, inputs, outputs, gvm):
    pose_stamped = inputs["pose_stamped"]

    quaternion = range(4)
    quaternion[0] = pose_stamped.pose.orientation.x
    quaternion[1] = pose_stamped.pose.orientation.y
    quaternion[2] = pose_stamped.pose.orientation.z
    quaternion[3] = pose_stamped.pose.orientation.w
    
    e = tf.transformations.euler_from_quaternion(
        quaternion,
        axes="sxyz"
        )

    p = pose_stamped.pose.position
    outputs["euler_pose"] = [p.x, p.y, p.z, e[0], e[1], e[2]]
    
    self.logger.info("Euler pose:\n{0}".format(outputs["euler_pose"]))

    return 0

