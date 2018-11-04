import copy
import tf.transformations as trafo
from geometry_msgs.msg import PoseStamped

def execute(self, inputs, outputs, gvm):
  first_pose_stamped = inputs["first_pose_stamped"]
  second_pose_stamped = inputs["second_pose_stamped"]

  result_pose_stamped = copy.deepcopy(first_pose_stamped)

  first_pose = first_pose_stamped.pose
  second_pose = second_pose_stamped.pose

  position = [first_pose.position.x, first_pose.position.y, first_pose.position.z]
  first_translation = trafo.translation_matrix(position)
  orientation = [first_pose.orientation.x, first_pose.orientation.y, first_pose.orientation.z, first_pose.orientation.w]
  first_rotation = trafo.quaternion_matrix(orientation)
  first_matrix = trafo.concatenate_matrices(first_translation, first_rotation)

  position = [second_pose.position.x, second_pose.position.y, second_pose.position.z]
  second_translation = trafo.translation_matrix(position)
  orientation = [second_pose.orientation.x, second_pose.orientation.y, second_pose.orientation.z, second_pose.orientation.w]
  second_rotation = trafo.quaternion_matrix(orientation)
  second_matrix = trafo.concatenate_matrices(second_translation, second_rotation)

  result_matrix = trafo.concatenate_matrices(first_matrix, second_matrix)

  position = trafo.translation_from_matrix(result_matrix)
  result_pose_stamped.pose.position.x = float(position[0])
  result_pose_stamped.pose.position.y = float(position[1])
  result_pose_stamped.pose.position.z = float(position[2]) 
  orientation = trafo.quaternion_from_matrix(result_matrix)
  result_pose_stamped.pose.orientation.x = orientation[0]
  result_pose_stamped.pose.orientation.y = orientation[1]
  result_pose_stamped.pose.orientation.z = orientation[2]
  result_pose_stamped.pose.orientation.w = orientation[3] 

  outputs["result_pose_stamped"] = result_pose_stamped

  self.logger.info("Concatenating pose stamped:")
  self.logger.info("First pose:\n{0}".format(str(first_pose_stamped)))
  self.logger.info("Second pose:\n{0}".format(str(second_pose_stamped)))
  self.logger.info("Result pose:\n{0}".format(str(result_pose_stamped)))
  
  return 0
