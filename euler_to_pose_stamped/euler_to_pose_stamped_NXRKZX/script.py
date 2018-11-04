import tf
import rospy
from geometry_msgs.msg import PoseStamped

def execute(self, inputs, outputs, gvm):
    euler_pose = inputs["euler_pose"]

    pose_stamped = PoseStamped()
    pose_stamped.header.frame_id = inputs["frame_id"]
    
    if inputs["time"] is None:
        self.logger.debug("no time set -- setting to now")
        stamp = rospy.Time.now()
    else:
        stamp = inputs["time"]
    pose_stamped.header.stamp = stamp
    
    pose_stamped.pose.position.x = euler_pose[0]
    pose_stamped.pose.position.y = euler_pose[1]
    pose_stamped.pose.position.z = euler_pose[2]

    quaternion = tf.transformations.quaternion_from_euler(
        euler_pose[3],
        euler_pose[4],
        euler_pose[5],
        axes="sxyz"
        )

    pose_stamped.pose.orientation.x = quaternion[0]
    pose_stamped.pose.orientation.y = quaternion[1]
    pose_stamped.pose.orientation.z = quaternion[2]
    pose_stamped.pose.orientation.w = quaternion[3]
    
    self.logger.info("Translation:\n{0}".format(pose_stamped.pose.position))
    self.logger.info("Orientation:\n{0}".format(pose_stamped.pose.orientation))

    outputs["pose_stamped"] = pose_stamped;
    return 0

