#!/usr/bin/env python

import time
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt

class TurtleBot:

    def __init__(self): 
        # Initialize the node
        rospy.init_node("Node_GoToGoal", anonymous=True)

        # Create the publisher
        self.velocity_publisher=rospy.Publisher(
            '/turtle1/cmd_vel',
            Twist,
            queue_size=10
        )

        # Create the subscriber
        self.velocity_subscriber=rospy.Subscriber(
            '/turtle1/pose',
            Pose,
            self.update_pose
        )

        self.pose=Pose()
        self.rate=rospy.Rate(10)

    """
        Callback function
    """
    def update_pose(self, data):
        self.pose=data

        # rounding off the data to 4th decimal place
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)

    """
        Function to calculate Euclidean distance between 
        goal pose and current pose. 
    """
    def euclidean_distance(self, goal_pose):
        return (sqrt(pow((goal_pose.x - self.pose.x), 2) + 
                     pow((goal_pose.y - self.pose.y), 2)))
    
    """
        The linear velocity controller, here, is a proportionality 
        controller, as the value of the linear velocity is directly 
        proportional to euclidean distance between the goal and current
        position. 
    """
    def get_linear_velocity(self, goal_pose, velocity_constant=1.5):
        return velocity_constant*(self.euclidean_distance(goal_pose))
    
    """
        Function to calculate the steering angle of the robot:
        angle = tan_inverse((y2-y1)/(x2-x1))
        This provides the angle to which the robot has to rotate
        when the next set of command is published. 
    """
    def get_steering_angle(self, goal_pose):
        return atan2(goal_pose.y-self.pose.y, goal_pose.x-self.pose.x)
    
    """
        Proportional controlled angular speed calculation. The final
        angular speed is proportional to the difference between current 
        orientation and the target orientation. 
    """
    def get_angular_velocity(self, goal_pose, constant=6):
        return constant*(self.get_steering_angle(goal_pose)-self.pose.theta)
    
    """
        The ultimate function to implement the "Send to goal"
        functionality on the bot. 
    """
    def move2goal(self):
        goal_pose=Pose()

        # get the target inputs (x,y) from the user.
        goal_pose.x=float(input("Set your goal x: "))
        goal_pose.y=float(input("Set your goal y: "))

        # get the distance tollerance input from the user
        distance_tollerance=float(input("Set your distance tollerance: "))

        vel_msg=Twist()

        while self.euclidean_distance(goal_pose)>=distance_tollerance:
            vel_msg.linear.x=self.get_linear_velocity(goal_pose, 1.5)
            vel_msg.linear.y=0.0
            vel_msg.linear.z=0.0

            vel_msg.angular.x=0.0
            vel_msg.angular.y=0.0
            vel_msg.angular.z=self.get_angular_velocity(goal_pose, 6.0)

            # publish the message to the topic
            self.velocity_publisher.publish(vel_msg)

            self.rate.sleep()

        # Stop the robot after the desired motion is complete
        vel_msg.linear.x=0.0
        vel_msg.angular.z=0.0
        self.velocity_publisher.publish(vel_msg)

        rospy.spin()

if __name__=="__main__":
    try:
        x=TurtleBot()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass
