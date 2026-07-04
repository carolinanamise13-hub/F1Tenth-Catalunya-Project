# 🏎️ F1Tenth Catalunya Autonomous Racing Project

Autonomous racing project developed using ROS 2 Humble, the F1Tenth simulator, and the Follow the Gap algorithm on the Catalunya circuit.

## 📌 Project Overview

This project focuses on the development of an autonomous racing controller for an F1Tenth vehicle.

The vehicle uses LiDAR data to detect free space and navigate through the circuit using the Follow the Gap algorithm.

The main simulation environment is the Catalunya circuit.

## 🎯 Objectives

The project includes four main challenges:

1. Complete 10 consecutive laps without collision.
2. Achieve the lowest possible lap time.
3. Complete 10 consecutive laps with 5 static obstacles.
4. Complete 10 consecutive laps with 2 additional moving robots acting as dynamic obstacles.

## 🛠️ Technologies

- Ubuntu 22.04
- ROS 2 Humble
- Python 3
- F1Tenth Gym
- RViz
- LiDAR
- Ackermann Steering
- Follow the Gap Algorithm

## 🗺️ Circuit

The main track used in this project is:

- Catalunya Circuit

Map files:

```text
src/f1tenth_gym_ros/maps/Catalunya_map.png
src/f1tenth_gym_ros/maps/Catalunya_map.yaml

# Lab 01 — Environment Setup

## Objective

Configure the development environment required to run the F1Tenth autonomous racing project using ROS 2 Humble on Ubuntu 22.04.

---

## System Requirements

The project was developed using:

- Ubuntu 22.04
- ROS 2 Humble
- Python 3
- Git
- colcon
- RViz
- Visual Studio Code
- F1Tenth Gym ROS

---

## 1. Update the System

Open a terminal and run:

```bash
sudo apt update
sudo apt upgrade -y
```

---

## 2. Install Git

Install Git using:

```bash
sudo apt install git -y
```

Verify the installation:

```bash
git --version
```

Expected output:

```text
git version 2.x.x
```

---

## 3. Verify ROS 2 Humble

Load the ROS 2 environment:

```bash
source /opt/ros/humble/setup.bash
```

Verify the active ROS distribution:

```bash
printenv ROS_DISTRO
```

Expected output:

```text
humble
```

---

## 4. Install colcon

Install the ROS 2 build tools:

```bash
sudo apt install python3-colcon-common-extensions -y
```

---

## 5. Create the Workspace

Create the F1Tenth workspace:

```bash
mkdir -p ~/f1tenth_ws/src
cd ~/f1tenth_ws
```

The workspace structure is:

```text
f1tenth_ws/
└── src/
```

---

## 6. Build the Workspace

Run:

```bash
cd ~/f1tenth_ws
colcon build
```

---

## 7. Source the Workspace

After compilation:

```bash
source /opt/ros/humble/setup.bash
source ~/f1tenth_ws/install/setup.bash
```

---

## 8. Optional Permanent ROS 2 Setup

To automatically load ROS 2 Humble when opening a terminal:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

After the workspace has been successfully built:

```bash
echo "source ~/f1tenth_ws/install/setup.bash" >> ~/.bashrc
```

Reload the terminal configuration:

```bash
source ~/.bashrc
```

---

## Expected Result

At the end of this laboratory:

- ROS 2 Humble is available.
- Git is installed.
- colcon is available.
- The `f1tenth_ws` workspace exists.
- ROS 2 packages can be compiled successfully.

---

# Lab 02 — F1Tenth Simulator and Catalunya Track

## Objective

Configure and launch the F1Tenth simulator using the Catalunya circuit.

---

## Project Structure

The simulator package is located at:

```text
src/f1tenth_gym_ros/
```

The track maps are located at:

```text
src/f1tenth_gym_ros/maps/
```

---

## Catalunya Track Files

The Catalunya circuit uses the following files:

```text
Catalunya_map.png
Catalunya_map.yaml
```

Inside the repository:

```text
src/f1tenth_gym_ros/maps/Catalunya_map.png
src/f1tenth_gym_ros/maps/Catalunya_map.yaml
```

---

## 1. Verify the Map Files

Run:

```bash
ls ~/f1tenth_ws/src/f1tenth_gym_ros/maps
```

The output should include:

```text
Catalunya_map.png
Catalunya_map.yaml
```

---

## 2. Map Configuration

The YAML file defines the map configuration.

Example structure:

```yaml
image: Catalunya_map.png
resolution: 0.05
origin: [0.0, 0.0, 0.0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.196
```

The exact values must match the Catalunya map configuration used in the project.

---

## 3. Simulator Configuration

The main simulator configuration file is located at:

```text
src/f1tenth_gym_ros/config/sim.yaml
```

This configuration must point to the Catalunya map used by the simulator.

---

## 4. Build the Workspace

Run:

```bash
cd ~/f1tenth_ws
colcon build
```

---

## 5. Source ROS 2

Run:

```bash
source /opt/ros/humble/setup.bash
source ~/f1tenth_ws/install/setup.bash
```

---

## 6. Launch the Simulator

Run:

```bash
ros2 launch f1tenth_gym_ros gym_bridge_launch.py
```

---

## Expected Result

RViz should display:

- The Catalunya circuit
- The F1Tenth vehicle
- The occupancy map
- LiDAR information
- The vehicle position
- The simulation environment

---

## Visual Evidence

Simulation screenshots are stored in:

```text
img/simulador/
```

Example:

```markdown
![F1Tenth Simulator on Catalunya](../../img/simulador/rviz_catalunya.png)
```

---

## Troubleshooting

### Map file not found

Verify that both files exist:

```bash
ls ~/f1tenth_ws/src/f1tenth_gym_ros/maps
```

### Package not found

Rebuild and source the workspace:

```bash
cd ~/f1tenth_ws
colcon build
source install/setup.bash
```

---

# Lab 03 — Follow the Gap Controller

## Objective

Implement an autonomous racing controller based on LiDAR information using the Follow the Gap algorithm.

The controller is designed to navigate the Catalunya circuit while avoiding collisions with the track boundaries.

---

## ROS 2 Package

The custom package is located at:

```text
src/gap_follow/
```

The main controller is located at:

```text
src/gap_follow/gap_follow/gap_node.py
```

---

## Package Structure

```text
gap_follow/
├── gap_follow/
│   ├── __init__.py
│   ├── gap_node.py
│   └── lap_counter.py
├── resource/
├── test/
├── package.xml
├── setup.cfg
└── setup.py
```

---

## Follow the Gap Overview

The controller processes LiDAR measurements to identify the largest collision-free region in front of the vehicle.

The general algorithm is:

```text
LiDAR Scan
    |
    v
Preprocess Ranges
    |
    v
Find Closest Obstacle
    |
    v
Create Safety Bubble
    |
    v
Find Largest Free Gap
    |
    v
Select Best Point
    |
    v
Calculate Steering Angle
    |
    v
Calculate Dynamic Speed
    |
    v
Publish Drive Command
```

---

## 1. LiDAR Subscription

The controller receives LiDAR measurements from:

```text
/scan
```

Message type:

```text
sensor_msgs/msg/LaserScan
```

Example:

```python
self.lidar_sub = self.create_subscription(
    LaserScan,
    '/scan',
    self.lidar_callback,
    10
)
```

---

## 2. Drive Publisher

The controller publishes commands to:

```text
/drive
```

Message type:

```text
ackermann_msgs/msg/AckermannDriveStamped
```

Example:

```python
self.drive_pub = self.create_publisher(
    AckermannDriveStamped,
    '/drive',
    10
)
```

---

## 3. LiDAR Preprocessing

Raw LiDAR data may contain:

- Infinite values
- NaN values
- Very large distances
- Noisy measurements

The controller preprocesses the scan before searching for a free gap.

Conceptually:

```python
ranges = np.array(scan_msg.ranges)

ranges = np.nan_to_num(
    ranges,
    nan=0.0,
    posinf=self.max_range,
    neginf=0.0
)

ranges = np.clip(
    ranges,
    0.0,
    self.max_range
)
```

---

## 4. Closest Obstacle Detection

The controller searches for the nearest relevant obstacle.

Conceptually:

```python
closest_index = np.argmin(ranges)
```

This point is used to define a safety region.

---

## 5. Safety Bubble

A safety bubble is created around the closest obstacle.

Example parameter:

```python
self.bubble_radius = 18
```

The purpose of the bubble is to prevent the vehicle from selecting a target point too close to an obstacle.

---

## 6. Largest Free Gap

After removing the dangerous region, the controller searches for the largest consecutive free-space interval.

Conceptually:

```text
Blocked | Free Free Free Free | Blocked | Free Free
          <--- largest gap --->
```

---

## 7. Best Point Selection

Inside the largest free gap, the controller chooses a target point.

This target determines the desired steering direction.

---

## 8. Steering Calculation

The selected LiDAR index is converted into an angle.

The controller then limits the steering command to the maximum permitted value.

Example project parameter:

```python
self.max_steering_angle = 0.42
```

---

## 9. Dynamic Speed Control

The vehicle speed changes according to the steering demand.

General behavior:

```text
Small steering angle
        |
        v
Higher speed

Large steering angle
        |
        v
Lower speed
```

This allows the vehicle to:

- Accelerate on straights
- Reduce speed in medium curves
- Slow down in sharp curves

The exact speed values must match the current parameters defined in:

```text
src/gap_follow/gap_follow/gap_node.py
```

---

## 10. Build the Package

Run:

```bash
cd ~/f1tenth_ws
colcon build --packages-select gap_follow
```

---

## 11. Source the Workspace

Run:

```bash
source /opt/ros/humble/setup.bash
source ~/f1tenth_ws/install/setup.bash
```

---

## 12. Run the Controller

Run:

```bash
ros2 run gap_follow gap_node
```

---

## Expected Result

The vehicle should:

- Follow the Catalunya circuit
- Avoid track walls
- React to LiDAR obstacles
- Reduce speed in sharp curves
- Increase speed on straights

---

## Controller Source Code

The complete implementation is available at:

```text
src/gap_follow/gap_follow/gap_node.py
```

---

# Lab 04 — Lap Counter and Lap Timing

## Objective

Implement an independent ROS 2 node capable of:

- Detecting completed laps
- Counting laps automatically
- Measuring individual lap times
- Identifying the fastest lap
- Monitoring progress toward 10 consecutive laps

This functionality is required to evaluate the autonomous racing controller.

---

## Why Use a Separate Node?

The autonomous controller and the experimental evaluation system have different responsibilities.

The controller:

```text
gap_node.py
```

is responsible for:

- LiDAR processing
- Gap detection
- Steering
- Speed control
- Obstacle avoidance

The lap monitoring node:

```text
lap_counter.py
```

is responsible for:

- Vehicle position monitoring
- Finish-zone detection
- Lap counting
- Lap timing
- Best-lap calculation

Keeping these functions separate makes the project easier to debug and maintain.

---

## Source File

The lap counter implementation is located at:

```text
src/gap_follow/gap_follow/lap_counter.py
```

---

## Package Structure

```text
gap_follow/
├── gap_follow/
│   ├── __init__.py
│   ├── gap_node.py
│   └── lap_counter.py
├── package.xml
├── setup.cfg
└── setup.py
```

---

# Part 1 — Lap Detection

## Finish Zone Concept

A specific region of the Catalunya circuit is used as the start/finish zone.

Conceptually:

```text
                 Catalunya Track

      -------------------------------
     /                               \
    /                                 \
   |                                   |
   |                                   |
    \                                 /
     \_________ FINISH ZONE _________/
```

The counter monitors the vehicle position and determines whether the vehicle enters this region.

---

## Finish-Zone Detection

Conceptually, the vehicle is considered inside the finish region when its position satisfies predefined limits.

Example logic:

```python
inside_finish_zone = (
    min_x <= x <= max_x and
    min_y <= y <= max_y
)
```

The exact finish-zone coordinates must match the values used in the current `lap_counter.py` implementation.

---

# Part 2 — Preventing Multiple Counts

## The Problem

ROS 2 callbacks run repeatedly.

When the vehicle enters the finish zone, it may remain there during several callback cycles.

Without protection, one physical crossing could incorrectly produce:

```text
Lap 1
Lap 2
Lap 3
Lap 4
```

---

## State Variable Solution

A state variable is used to remember whether the vehicle is already inside the finish zone.

Conceptually:

```python
self.in_finish_zone = False
```

When the vehicle enters the zone:

```python
if inside_finish_zone and not self.in_finish_zone:
    self.in_finish_zone = True
```

When it leaves:

```python
if not inside_finish_zone:
    self.in_finish_zone = False
```

This creates an edge-triggered event:

```text
Outside
   |
   v
Enter Finish Zone
   |
   v
Count Once
   |
   v
Remain Inside
   |
   v
Do Not Count Again
   |
   v
Exit Zone
   |
   v
Ready for Next Lap
```

---

# Part 3 — Lap Counter

The node stores the number of completed laps.

Conceptually:

```python
self.lap_count = 0
```

When a valid finish-line crossing occurs:

```python
self.lap_count += 1
```

Example terminal output:

```text
Lap 1 completed
Lap 2 completed
Lap 3 completed
```

The main project objective is:

```text
10 consecutive laps
0 collisions
```

---

# Part 4 — How Lap Time Is Measured

## ROS 2 Clock

The lap timer uses the ROS 2 node clock.

The current timestamp is obtained with:

```python
current_time = self.get_clock().now()
```

This provides the time associated with the ROS 2 execution environment.

---

## First Valid Crossing

At the beginning of the experiment, the timer needs a reference timestamp.

Conceptually:

```python
self.last_lap_time = self.get_clock().now()
```

The first reference marks the beginning of the timing interval.

---

## Completing a Lap

When the vehicle completes the next valid finish-zone crossing:

```python
current_time = self.get_clock().now()
```

The lap duration is calculated as:

```python
lap_duration = current_time - self.last_lap_time
```

Then the timestamp is updated:

```python
self.last_lap_time = current_time
```

The next lap starts timing immediately.

---

## Converting Time to Seconds

ROS 2 durations can be converted into seconds.

Conceptually:

```python
lap_seconds = lap_duration.nanoseconds / 1e9
```

This conversion is based on:

```text
1 second = 1,000,000,000 nanoseconds
```

Therefore:

```text
lap time in seconds
=
duration in nanoseconds / 1,000,000,000
```

---

## Complete Timing Logic

Conceptually:

```python
current_time = self.get_clock().now()

lap_duration = current_time - self.last_lap_time

lap_seconds = lap_duration.nanoseconds / 1e9

self.last_lap_time = current_time
```

The resulting value represents the duration of one completed lap.

---

## Example

Suppose:

```text
Previous crossing: 120.50 s
Current crossing: 144.85 s
```

Then:

```text
Lap time = 144.85 - 120.50
Lap time = 24.35 s
```

Terminal output:

```text
Lap 3 completed
Lap time: 24.35 s
```

---

# Part 5 — Fastest Lap

The node can store the best lap recorded during the experiment.

Conceptually:

```python
self.best_lap_time = None
```

After measuring a valid lap:

```python
if self.best_lap_time is None:
    self.best_lap_time = lap_seconds
```

For subsequent laps:

```python
elif lap_seconds < self.best_lap_time:
    self.best_lap_time = lap_seconds
```

---

## Fastest-Lap Logic

```text
New Lap Time
     |
     v
Is there a previous best?
     |
  No | Yes
     |   |
     v   v
 Save   Is new time smaller?
        |
     Yes|No
        |
        v
   Update Best Lap
```

---

## Example

Recorded times:

| Lap | Time |
|---|---:|
| 1 | 25.21 s |
| 2 | 24.88 s |
| 3 | 23.95 s |
| 4 | 24.17 s |

The best lap is:

```text
23.95 s
```

---

# Part 6 — Complete Experimental Output

The node may produce output similar to:

```text
Lap 1 completed
Lap time: 25.21 s
Best lap: 25.21 s
```

Then:

```text
Lap 2 completed
Lap time: 24.88 s
New best lap: 24.88 s
```

Then:

```text
Lap 3 completed
Lap time: 23.95 s
New best lap: 23.95 s
```

---

# Part 7 — Ten-Lap Objective

The counter continues until:

```python
self.lap_count >= 10
```

At that point the node can report:

```text
10 laps completed successfully
```

The complete evaluation objective is:

```text
Laps completed: 10
Collisions: 0
```

---

# Part 8 — Register the ROS 2 Executable

The lap counter must be registered in:

```text
src/gap_follow/setup.py
```

Inside `entry_points`, the package should contain:

```python
entry_points={
    'console_scripts': [
        'gap_node = gap_follow.gap_node:main',
        'lap_counter = gap_follow.lap_counter:main',
    ],
},
```

This allows ROS 2 to execute the node using:

```bash
ros2 run gap_follow lap_counter
```

---

# Part 9 — Build the Package

After creating or modifying `lap_counter.py`:

```bash
cd ~/f1tenth_ws
colcon build --packages-select gap_follow
```

---

# Part 10 — Source the Workspace

Run:

```bash
source /opt/ros/humble/setup.bash
source ~/f1tenth_ws/install/setup.bash
```

---

# Part 11 — Verify Executables

Run:

```bash
ros2 pkg executables gap_follow
```

Expected output:

```text
gap_follow gap_node
gap_follow lap_counter
```

---

# Part 12 — Run the Complete Experiment

## Terminal 1 — Simulator

```bash
source /opt/ros/humble/setup.bash
source ~/f1tenth_ws/install/setup.bash
ros2 launch f1tenth_gym_ros gym_bridge_launch.py
```

---

## Terminal 2 — Follow the Gap Controller

```bash
source /opt/ros/humble/setup.bash
source ~/f1tenth_ws/install/setup.bash
ros2 run gap_follow gap_node
```

---

## Terminal 3 — Lap Counter and Timer

```bash
source /opt/ros/humble/setup.bash
source ~/f1tenth_ws/install/setup.bash
ros2 run gap_follow lap_counter
```

---

# Expected Result

During the experiment:

1. The simulator runs the Catalunya circuit.
2. `gap_node` controls the autonomous vehicle.
3. `lap_counter` monitors valid finish-zone crossings.
4. Each valid crossing increments the lap counter.
5. The elapsed lap time is calculated.
6. The fastest lap is updated when necessary.
7. The experiment continues toward 10 consecutive laps.

---

## Results Storage

Lap-time results can be documented in:

```text
results/lap_times/
```

Recommended table:

| Lap | Lap Time | Best Lap | Collision |
|---|---:|---:|---|
| 1 | Pending | Pending | No |
| 2 | Pending | Pending | No |
| 3 | Pending | Pending | No |
| 4 | Pending | Pending | No |
| 5 | Pending | Pending | No |
| 6 | Pending | Pending | No |
| 7 | Pending | Pending | No |
| 8 | Pending | Pending | No |
| 9 | Pending | Pending | No |
| 10 | Pending | Pending | No |

---

## Source Code

The complete implementation is available at:

```text
src/gap_follow/gap_follow/lap_counter.py
```

---

