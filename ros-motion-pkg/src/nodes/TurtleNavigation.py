#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class TurtlebotNavigation:
    def __init__(self):
        rospy.init_node('publisher', anonymous=True)

        # Publisher to publish the command velocity
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

        # Subscriber to get the turtle's current pose
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose', Pose, self.update_pose)

        self.pose = Pose()
        self.rate = rospy.Rate(1000)

    """
    This function updates the turtlebot's current pose
    """
    def update_pose(self, data):
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    """
    Function to calculate distance between goal and target
    """
    def get_distance(self, goal_pose):
        return abs(goal_pose.x - self.pose.x)
    
    def move_to_goal(self):
        target_x = 10.0000
        goal_pose = Pose()
        goal_pose.x = target_x
        distance_tolerance = 0.01

        vel_msg = Twist()

        while self.get_distance(goal_pose) >= distance_tolerance and not rospy.is_shutdown():
            vel_msg.linear.x = 2
            self.velocity_publisher.publish(vel_msg)
            self.rate.sleep()

        # Stop movement once goal reached
        vel_msg.linear.x = 0
        self.velocity_publisher.publish(vel_msg)
        rospy.loginfo("Goal reached!")

if __name__ == '__main__':
    try:
        x = TurtlebotNavigation()
        x.move_to_goal()
    except rospy.ROSInterruptException:
        pass
    