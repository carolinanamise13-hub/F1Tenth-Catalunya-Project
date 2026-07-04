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