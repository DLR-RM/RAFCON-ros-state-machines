import rospy
import tf
from geometry_msgs.msg import PoseStamped


def execute(self, inputs, outputs, gvm):

    listener = gvm.get_variable("tf_listener")
    hz = inputs['hz']
    max_loops = hz * inputs['max_wait']  # wait maximal 10 seconds
    loop_counter = 0.0
    rate = rospy.Rate(hz)
    if inputs["time"]:
        stamp = inputs["time"]
    else:
        self.logger.debug("no time set -- setting to now")
        stamp = rospy.Time(0)

    while not rospy.is_shutdown():

        try:
            #if inputs["time"] is None:
            #    stamp = rospy.Time(0)
                

            (trans, rot) = listener.lookupTransform(inputs["parent_frame_id"], inputs["child_frame_id"], 
                                                    stamp)
            break
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            # did not find the transformation yet, try another time
            pass

        loop_counter += 1
        if loop_counter > max_loops:
            self.logger.error("Transform not found!")
            return -1

        rate.sleep()
        
    pose_stamped = PoseStamped()
    pose_stamped.header.frame_id = inputs["parent_frame_id"]
    pose_stamped.header.stamp = stamp
    
    pose_stamped.pose.position.x = trans[0]
    pose_stamped.pose.position.y = trans[1]
    pose_stamped.pose.position.z = trans[2]

    pose_stamped.pose.orientation.x = rot[0]
    pose_stamped.pose.orientation.y = rot[1]
    pose_stamped.pose.orientation.z = rot[2]
    pose_stamped.pose.orientation.w = rot[3]
        
    self.logger.debug("Translation: {0}".format(trans))
    self.logger.debug("Rotation: {0}".format(rot))

    outputs["pose_stamped"] = pose_stamped
    outputs["time"] = stamp

    return 0
