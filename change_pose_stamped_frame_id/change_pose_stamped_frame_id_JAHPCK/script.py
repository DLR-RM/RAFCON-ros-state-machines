
def execute(self, inputs, outputs, gvm):
    new_frame_id = inputs["frame_id"]
    pose_stamped_in = inputs["pose_stamped_in"]
    pose_stamped_out = pose_stamped_in
    pose_stamped_out.header.frame_id = new_frame_id
    outputs["pose_stamped_out"] = pose_stamped_out  
    self.logger.debug("Changed pose stamped frame id to %s" % new_frame_id)
    return 0
