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
        
    # debug output
    self.logger.debug("Translation:\n{0}".format(trans))
    self.logger.debug("Rotation in Quaternions:\n{0}".format(rot))
    euler_angles = tf.transformations.euler_from_quaternion(rot, "sxyz")
    self.logger.debug("Rotation in Euler angles:\n{0}".format(euler_angles))
    
    trans_matrix = tf.transformations.translation_matrix(trans)
    rot_matrix = tf.transformations.quaternion_matrix(rot)
    concat_matrix = tf.transformations.concatenate_matrices(trans_matrix, rot_matrix)
 
    outputs["transformation_matrix"] = list(concat_matrix)
    outputs["time"] = stamp
    self.logger.info("transformation_matrix:")
    self.logger.info(":\n"+str(concat_matrix))

    return 0
