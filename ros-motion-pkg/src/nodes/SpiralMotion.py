#!/usr/bin/env python

import time
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt

class TurtleBot:

    def __init__(self): 
        # Initialize the node
        rospy.init_node("Node_SpiralMotion", anonymous=True)

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


    def go_spiral(self, wk, rk):
        message=Twist()

        while((self.pose.x<10.0) and (self.pose.y<10.0)):
            rk=rk+0.5
            message.linear.x=rk
            message.linear.y=0.0
            message.linear.z=0.0
        
            message.angular.x=0.0
            message.angular.y=0.0
            message.angular.z=wk

            self.velocity_publisher.publish(message)
            self.rate.sleep()
            
            
        # Stop the robot after the desired motion is complete
        message.linear.x=0.0
        message.angular.z=0.0
        self.velocity_publisher.publish(message)

        rospy.spin()


if __name__=="__main__":
    try:
        x=TurtleBot()
        x.go_spiral(15.0,0)
    except rospy.ROSInterruptException:
        pass