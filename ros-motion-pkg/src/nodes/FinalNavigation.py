#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time

# Global variables for turtle position
x = 0.0
y = 0.0
yaw = 0.0

def poseCallback(pose_message):
    global x, y, yaw
    x = pose_message.x
    y = pose_message.y
    yaw = pose_message.theta

def move(speed, distance, is_forward):
    velocity_message = Twist()
    
    x0 = x
    y0 = y

    if is_forward:
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message.linear.x = -abs(speed)

    loop_rate = rospy.Rate(10) 
    
    while not rospy.is_shutdown():
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        
        distance_moved = math.sqrt(((x - x0) ** 2) + ((y - y0) ** 2))
        if distance_moved >= (distance - 0.05): # Soft tolerance boundary
            break
    
    # Stop the robot
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)
    
def rotate(angular_speed_degree, relative_angle_degree, clockwise):
    velocity_message = Twist()
    angular_speed = math.radians(abs(angular_speed_degree))

    if clockwise:
        velocity_message.angular.z = -abs(angular_speed)
    else:
        velocity_message.angular.z = abs(angular_speed)

    # Track displacement safely relative to the initial orientation jump
    start_yaw = yaw
    loop_rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        velocity_publisher.publish(velocity_message)
        
        angle_turned = abs(math.atan2(math.sin(yaw - start_yaw), math.cos(yaw - start_yaw)))
        if angle_turned >= (math.radians(relative_angle_degree) - 0.02):
            break
            
        loop_rate.sleep()

    # Stop the rotation
    velocity_message.angular.z = 0
    velocity_publisher.publish(velocity_message)

def go_to_goal(x_goal, y_goal):
    velocity_message = Twist()
    loop_rate = rospy.Rate(10) 

    while not rospy.is_shutdown():
        K_linear = 0.5 
        distance = math.sqrt(((x_goal - x) ** 2) + ((y_goal - y) ** 2))
        linear_speed = distance * K_linear

        K_angular = 4.0
        desired_angle_goal = math.atan2(y_goal - y, x_goal - x)
        
        angle_diff = desired_angle_goal - yaw
        angle_diff = math.atan2(math.sin(angle_diff), math.cos(angle_diff))
        angular_speed = angle_diff * K_angular

        velocity_message.linear.x = linear_speed
        velocity_message.angular.z = angular_speed

        velocity_publisher.publish(velocity_message)

        if distance < 0.1: 
            break
            
        loop_rate.sleep()

    velocity_message.linear.x = 0
    velocity_message.angular.z = 0
    velocity_publisher.publish(velocity_message)

def setDesiredOrientation(desired_angle_radians):
    relative_angle_radians = desired_angle_radians - yaw
    relative_angle_radians = math.atan2(math.sin(relative_angle_radians), math.cos(relative_angle_radians))
    
    clockwise = relative_angle_radians < 0
    rotate(30, math.degrees(abs(relative_angle_radians)), clockwise)

def gridClean():
    rospy.loginfo("Starting Absolute Grid Cleaning Routine...")
    # 1. Start safely out of the bottom-left corner
    go_to_goal(1.5, 1.5)
 
    # 2. Sweep 1: Face East (0 rad) and sweep right
    setDesiredOrientation(0.0)
    move(2.0, 7.5, True)
    
    # Shift Up: Face North (pi/2) and step up
    setDesiredOrientation(math.radians(90))
    move(2.0, 1.5, True)
    
    # 3. Sweep 2: Face West (pi rad) and sweep left
    setDesiredOrientation(math.radians(180))
    move(2.0, 7.5, True)
    
    # Shift Up: Face North (pi/2) and step up
    setDesiredOrientation(math.radians(90))
    move(2.0, 1.5, True)
    
    # 4. Sweep 3: Face East (0 rad) and sweep right
    setDesiredOrientation(0.0)
    move(2.0, 7.5, True)
    rospy.loginfo("Grid cleaning finished successfully!")

if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_motion_pose', anonymous=True)

        cmd_vel_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
        
        position_topic = "/turtle1/pose"
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback) 
        
        time.sleep(1)
        gridClean()
       
    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated.")