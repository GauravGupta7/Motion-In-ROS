#!/usr/bin/env python
"""
    In this script we are trying to set the orientation of the robot. This is different from the rotate function.
    In rotate, if we first rotate the robot by 10 degree and then by 20 degree, the robot will face an angle 30 degree. 
    However, here is we pass the goal orientation as 10 and then 20 degrees, the robot will finally be facing the 20 degree angle. 
    It can be assumed as the Turn-To-Angle functionality.
"""

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class TurtleBot:
    def __init__(self): 
        # Initialize the node
        rospy.init_node("Node_SetDesiredOrientation", anonymous=True)

        # Create the publisher
        self.publisher=rospy.Publisher(
            name='/turtle1/cmd_vel',
            data_class=Twist,
            queue_size=10
        )

        # Create the subscriber
        self.velocity_subscriber=rospy.Subscriber(
            name='/turtle1/pose',
            data_class= Pose,
            callback=self.update_pose
        )

        self.pose=Pose()
        self.rate=rospy.Rate(10000)



    def update_pose(self, data):
        self.pose.theta=data.theta



    def rotate(self, anglular_speed_degree, relative_angle_degree, is_clockwise):
        velocity_message=Twist()

        anglular_speed = math.radians(abs(anglular_speed_degree))

        if is_clockwise:
            velocity_message.angular.z=-abs(anglular_speed)
        else:
            velocity_message.angular.z=abs(anglular_speed)

        #loop_rate=rospy.Rate(10000) # Publishing at the rate of 10Hz (10 times per sec.)
        t0=rospy.Time.now().to_sec()

        while True:
            rospy.loginfo("Turtle rotates...")
            self.publisher.publish(velocity_message)

            t1=rospy.Time.now().to_sec()
            current_angle_degree=(t1-t0)*anglular_speed_degree
            self.rate.sleep()

            if current_angle_degree>relative_angle_degree:
                rospy.loginfo("Orientation reached!!")
                break

        velocity_message.angular.z=0.0
        self.publisher.publish(velocity_message)




    def setDesiredOrientation(self, speed_in_degree, desired_angle_degree):
        relative_angle_radians=math.radians(desired_angle_degree)-self.pose.theta
        
        if relative_angle_radians<0:
            clockwise=1
        else:
            clockwise=0

        self.rotate(speed_in_degree, math.degrees(relative_angle_radians), clockwise)


if __name__=="__main__":
    try:
        x=TurtleBot()
        x.setDesiredOrientation(30, 90)
    except rospy.ROSInterruptException:
        pass
