# **Motion-In-ROS**

## **1. Basics of robot motion**

Motion can be movement in a straight line, rotation at a fixed position or simultaneous rotation and linear motion. 

**Motion in straight line**

Linear:  
* x: *speed*  
* y: 0  
* z: 0

Angular:  
* X: 0
* Y: 0
* Z: 0


**Rotation in place**

Linear:  
* x: 0  
* y: 0  
* z: 0

Angular:  
* X: 0
* Y: 0
* Z: *speed*  (yaw)

**Go to goal**

In this case the motion should be smooth. To handle this, we implement a strategy where the speeds are a function of a distance in case of linear components and a function of an angle in case of angular component. 

Linear:  
* x = *f(distance)*
* y = 0
* z = 0

Angular: 
* X: 0
* Y: 0
* Z: *f(angle)*

**Spiral motion**  
The below mentioned configuration is used for implementing spiral motion in a robot: 

Linear:  
* x: *f(time)*
* y: 0
* z: 0

Angular: 
* X: 0
* Y: 0
* Z: *constant*