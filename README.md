# **Motion-In-ROS**

## **1. Basics of robot motion**

Motion can be movement in a straight line, rotation at a fixed position or simultaneous rotation and linear motion. 

**A. Motion in straight line**

Linear:  
* x: *speed*  
* y: 0  
* z: 0

Angular:  
* X: 0
* Y: 0
* Z: 0


**B. Rotation in place**

Linear:  
* x: 0  
* y: 0  
* z: 0

Angular:  
* X: 0
* Y: 0
* Z: *speed*  (yaw)

**C. Go to goal**

In this case the motion should be smooth. To handle this, we implement a strategy where the speeds are a function of a distance in case of linear components and a function of an angle in case of angular component. 

Linear:  
* x = *f(distance)*
* y = 0
* z = 0

Angular: 
* X: 0
* Y: 0
* Z: *f(angle)*

**D. Spiral motion**    

The below mentioned configuration is used for implementing spiral motion in a robot: 

Linear:  
* x: *f(time)*
* y: 0
* z: 0

Angular: 
* X: 0
* Y: 0
* Z: *constant*


## **2. What are we implementing?**

We are trying to implement a cleaning robot that moves around in a bounded environment and cleans it. First let us take a look at the steps of implementation. 

**Step 1: Understanding topics and messages used.**

Since we will be testing the code on the turtle, we can check the topics used using the command ```rostopic list``` after the application is up and running. The exact topic that we will use for this purpose is the ```turtle/cmd_vel```. The message type of this topic is ```geometry_msgs/Twist``` and more information about it can be obtained using the command:

```bash
rosmsg show geometry_msgs/Twist
```

It will give the following output:

```bash
geometry_msgs/Vector3 linear
  float64 x
  float64 y
  float64 z
geometry_msgs/Vector3 angular
  float64 x
  float64 y
  float64 z
```

Another topic that we will consider while developing this application is the pose topic. The pose topic, ```/turtle1/pose``` , gives information about the robots location in the 2D space. It used the type ```turtlesim/Pose``` with the following contents: 

```bash
hello@hello-2222:~/catkin_ws$ rosmsg show turtlesim/Pose
float32 x
float32 y
float32 theta
float32 linear_velocity
float32 angular_velocity
```

## **3. The Divide and Conquer Approach.**

We will divide the entire cleaning application of the robot (basically the motion of the robot) into simpler elementary components such that the entire process can be completed using combinations of these elemntary components. The components are: 

* Step 1: Develop a function to move in a straight line for a certain distance, forward or backward.
* Step 2: Develop a function to rotate in place for a certain angle, CW or CCW. 
* Step 3: Develop a function to go to a goal location. 
* Step 4: Develop a function to move in a spiral shape. 
* Step 5: Integrate all together to develop the cleaning application. 