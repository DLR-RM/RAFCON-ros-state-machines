import rospy
import tf


def execute(self, inputs, outputs, gvm):
    
    if inputs["time"] is None:
        self.logger.debug("no time set -- setting to now")
        stamp = rospy.Time.now()
    else:
        stamp = inputs["time"]
        
    if inputs["parent_frame_id"] is None or inputs["parent_frame_id"] == "":
        outputs["euler_pose"] = [0, 0, 0, 0, 0, 0]
        outputs["time"] = stamp
        return 0

    listener = gvm.get_variable("tf_listener")
    hz = inputs['hz']
    max_loops = hz * inputs['max_wait']  # wait maximal 10 seconds
    loop_counter = 0.0
    rate = rospy.Rate(hz)

    while not rospy.is_shutdown():

        try:
            (trans, rot) = listener.lookupTransform(inputs["parent_frame_id"], inputs["child_frame_id"], stamp)
            break
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            # did not find the transformation yet, try another time
            pass

        loop_counter += 1
        if loop_counter > max_loops:
            self.logger.error("Transform not found!")
            return -1

        rate.sleep()
        
    self.logger.info("Translation:\n{0}".format(trans))
    self.logger.info("Rotation in Quaternions:\n{0}".format(rot))

    euler_angles = tf.transformations.euler_from_quaternion(rot, "sxyz")
    self.logger.info("Rotation in Euler angles:\n{0}".format(euler_angles))
 
    outputs["euler_pose"] = [trans[0], trans[1], trans[2], euler_angles[0], euler_angles[1], euler_angles[2]]
    outputs["time"] = stamp
    self.logger.debug(euler_angles)

    return 0
