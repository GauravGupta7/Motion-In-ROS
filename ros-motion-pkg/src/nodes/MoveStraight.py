#!/usr/bin/env python

import time
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

"""
    Function to move the robot in a straight line. 

    Parameters:
    * velocity_publisher: rospy.Publisher() type object to publish to topic
    * speed: Speed in m/s with which the robot is expected to move
    * distance: The ultimate distance that the robot needs to travel. 
    * is_forward: True if robot wants to go ahead, False otherwise. 
"""
def move_straight(velocity_publisher, speed, distance, is_forward):
    # Declare a Twist message to send velocity commands
    velocity_message=Twist()

    # Get current locations
    global x, y
    x0=x
    y0=y

    if is_forward:
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message.linear.x = -abs(speed)

    distance_moved = 0.0
    loop_rate = rospy.Rate(10000)

    while True:
        rospy.loginfo("Turtle moves forward")
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        distance_moved = abs(math.sqrt(((x-x0)**2) + ((y-y0)**2)))
        print(distance_moved)

        if not distance_moved<distance:
            rospy.loginfo("reached")
            break
    
    # finally stop the robot when the distance is moved
    velocity_message.linear.x=0
    velocity_publisher.publish(velocity_message)



"""
    Callback function which is invoked when the subscriber listens a message. 
    It reads a message of pose_message type and can be unpacked to get useful
    information. 
"""
def poseCallback(pose_message):
    global x, y, yaw
    x=pose_message.x
    y=pose_message.y
    yaw=pose_message.theta



"""
    Function to implement rotation in a robot.
    
    Parameters:
    * velocity_publisher: rospy.Publisher() type object
    * angluar_speed_degree: Angluar speed (in degree) with which the robot should rotate.
    * relative_angle_degree: The desired/target orientation.
    * is_clockwise: True if rotation should be clockwise, False otherwise.
"""
def rotate(velocity_publisher, anglular_speed_degree, relative_angle_degree, is_clockwise):
    velocity_message=Twist()

    anglular_speed = math.radians(abs(anglular_speed_degree))

    """
    In ROS and Robotics in general:
    -> Clockwise = -ve
    -> Antoclockwise = +ve
    """
    if is_clockwise:
        velocity_message.angular.z=-abs(anglular_speed)
    else:
        velocity_message.angular.z=abs(anglular_speed)

    loop_rate=rospy.Rate(10000) # Publishing at the rate of 10Hz (10 times per sec.)
    t0=rospy.Time.now().to_sec()

    while True:
        rospy.loginfo("Turtle rotates...")
        velocity_publisher.publish(velocity_message)

        t1=rospy.Time.now().to_sec()
        current_angle_degree=(t1-t0)*anglular_speed_degree
        loop_rate.sleep()

        if current_angle_degree>relative_angle_degree:
            rospy.loginfo("Orientation reached!!")
            break

    velocity_message.angular.z=0.0
    velocity_publisher.publish(velocity_message)



if __name__=="__main__":
    try:
        node_name="turtlesim_motion_pose"
        rospy.init_node('turtlesim_motion_pose', anonymous=True)

        # declare the velocity topic
        cmd_vel_topic='/turtle1/cmd_vel'
        velocity_publisher=rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

        position_topic="/turtle1/pose"
        pose_subscriber=rospy.Subscriber(position_topic, Pose, poseCallback)
        time.sleep(2)

        move_straight(velocity_publisher, 10.0, 4.0, True)
        rotate(velocity_publisher, 30, 90.0, True)
        move_straight(velocity_publisher, 10.0, 4.0, True)
        rotate(velocity_publisher, 30, 90.0, True)
        move_straight(velocity_publisher, 10.0, 4.0, True)
        rotate(velocity_publisher, 30, 90.0, True)
        move_straight(velocity_publisher, 10.0, 4.0, True)


    except rospy.ROSInterruptException:
        pass
        #print(f"fail to initialize node {node_name}")