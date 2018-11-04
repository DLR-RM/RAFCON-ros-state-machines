import rospy
import tf
import math

EPSILON=0.01

def check_float_equality(num1, num2):
    if math.fabs(num1 - num2) < EPSILON:
        return True
    else:
        return False
        
def check_pose_equality(p1_tuple, p2_tuple, logger):
    for i in range(3):  # check all translation values
        if not check_float_equality(p1_tuple[0][i], p2_tuple[0][i]):
            logger.warning("translation not correct: {0} not equal to {1}".format(p1_tuple[0][i], p2_tuple[0][i]))
            return False
    for i in range(4):  # check all quaternion values
        if not check_float_equality(p1_tuple[1][i], -p2_tuple[1][i]):
            if not check_float_equality(p1_tuple[1][i], p2_tuple[1][i]):
                logger.warning("rotation not correct: {0} not equal to {1}".format(p1_tuple[1][i], p2_tuple[1][i]))
                return False
    return True
       
def execute(self, inputs, outputs, gvm):

    vcp = inputs["euler_pose"] # validity check pose#
    vcp_t = vcp[0:3]
    vcp_quat = tf.transformations.quaternion_from_euler(vcp[3], vcp[4], vcp[5], axes='sxyz')
    self.logger.debug("target pose: t: {0}, rot: {1}".format(vcp_t, vcp_quat))
    listener = tf.TransformListener()
    hz = 1.0
    max_loops = hz * inputs["timeout"]
    loop_counter = 0.0
    rate = rospy.Rate(hz)
    # request_time = rospy.Time.now()

    while not rospy.is_shutdown():

        try:
            (t, rot) = listener.lookupTransform(inputs["parent_frame_id"], inputs["child_frame_id"], rospy.Time(0))
            self.logger.debug("received pose: t: {0}, rot: {1}".format(t, rot))
            if check_pose_equality((t, rot), (vcp_t, vcp_quat), self.logger):
                break
            else:
                self.logger.error("Poses do not match")
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            # did not find the transformation yet, try another time
            pass

        loop_counter += 1
        if loop_counter > max_loops:
            self.logger.error("Transform not found!")
            return -1

        rate.sleep()

    return 0