from constants import JOINT_IDS

def get_joint_id(joint_name):
    return JOINT_IDS[joint_name]

def get_joint_data(joints, joint_name):
    joint_id = get_joint_id(joint_name)
    return joints[joint_id]