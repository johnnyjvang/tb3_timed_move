# tb3_timed_move

A minimal ROS 2 (Jazzy) test node for TurtleBot3 that performs a timed forward motion and reports odometry-based displacement.

This package is intended as a low-level validation tool to verify base kinematics and encoder scaling independently of Nav2, SLAM, or localization systems.

---

## Purpose

Before debugging higher-level navigation stacks, the base motion chain must be verified:

cmd_vel → motor controller → wheels → encoders → odom

This node isolates and validates that pipeline.

---

## What This Node Does

1. Subscribes to `/odom`
2. Publishes forward velocity to `/cmd_vel`
3. Moves at a constant speed (0.10 m/s)
4. Stops after 3 seconds
5. Calculates and prints the distance traveled

Expected theoretical distance:

distance = velocity × time  
distance = 0.10 × 3.0 = 0.30 meters  

0.30 meters ≈ 1 foot

---

## Requirements

- ROS 2 Jazzy
- TurtleBot3 (Burger / Waffle / Waffle Pi)
- `turtlebot3_bringup` installed
- Active `/cmd_vel` and `/odom` topics

---

## Installation

Clone into any ROS 2 workspace:

```
cd ~/your_ros2_ws/src
git clone https://github.com/<your-username>/tb3_timed_move.git
```

Build:

```
cd ~/your_ros2_ws
colcon build
source install/setup.bash
```

---

## Running on Real Hardware

Terminal 1:
```
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_bringup robot.launch.py
```

Terminal 2:
```
cd ~/your_ros2_ws
source install/setup.bash
ros2 run tb3_timed_move timed_move
```

---

## Running in Simulation (Gazebo)

Terminal 1:
```
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Terminal 2:
```
cd ~/your_ros2_ws
source install/setup.bash
ros2 run tb3_timed_move timed_move
```

---

## Expected Output

After 3 seconds:

Finished. Distance traveled: 0.298 meters

Acceptable tolerance range:
0.28 – 0.32 meters

---

## Diagnostic Interpretation

| Observation | Likely Cause |
|-------------|-------------|
| ~0.30 m | Correct scaling |
| ~0.15 m | Wheel radius / encoder configuration error |
| ~0.60 m | Scaling doubled |
| Moves backward | Motor direction inverted |
| Y-axis drift | Wheel imbalance |
| Rotational drift | Mechanical asymmetry |

---

## Why This Test Matters

If this timed displacement test fails, higher-level systems such as:

- AMCL
- Nav2
- SLAM
- Costmaps

will behave incorrectly regardless of parameter tuning.

This node provides a deterministic baseline test for differential drive correctness.

---

## License

Apache License 2.0
