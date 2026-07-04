#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import numpy as np

from sensor_msgs.msg import LaserScan
from ackermann_msgs.msg import AckermannDriveStamped


class GapFollow(Node):
    def __init__(self):
        super().__init__('gap_follow_node')

        self.lidar_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10
        )

        self.drive_pub = self.create_publisher(
            AckermannDriveStamped,
            '/drive',
            10
        )

        self.get_logger().info("Follow Gap Catalunya Pro")

        self.max_range = 8.0
        self.safety_distance = 1.0

        self.max_steering_angle = 0.52

        self.previous_steering = 0.0

        self.max_speed = 6.0
        self.min_speed = 2.2
        self.current_speed = 0.0

    def preprocess_lidar(self, ranges):
        ranges = np.array(ranges, dtype=float)
        ranges[np.isnan(ranges)] = 0.0
        ranges[np.isinf(ranges)] = self.max_range
        ranges = np.clip(ranges, 0.0, self.max_range)

        kernel = np.ones(5)/5
        return np.convolve(ranges, kernel, mode='same')

    def find_max_gap(self, free_space):
        start = None
        gaps = []

        for i, value in enumerate(free_space):
            if value > self.safety_distance and start is None:
                start = i
            elif value <= self.safety_distance and start is not None:
                gaps.append((start, i-1))
                start = None

        if start is not None:
            gaps.append((start, len(free_space)-1))

        if len(gaps) == 0:
            return 0, len(free_space)-1

        return max(gaps, key=lambda x: x[1]-x[0])

    def find_best_point(self, start, end, ranges):
        if end <= start:
            return (start + end)//2

        indices = np.arange(start, end+1)
        weights = ranges[start:end+1]

        if np.sum(weights) <= 0:
            return (start + end)//2

        return int(np.average(indices, weights=weights))

    def lidar_callback(self, data):

        ranges = self.preprocess_lidar(data.ranges)

        start_angle = -np.deg2rad(100)
        end_angle = np.deg2rad(100)

        start_idx = int((start_angle-data.angle_min)/data.angle_increment)
        end_idx = int((end_angle-data.angle_min)/data.angle_increment)

        start_idx = max(0,start_idx)
        end_idx = min(len(ranges)-1,end_idx)

        front = ranges[start_idx:end_idx+1].copy()

        closest = np.argmin(front)
        closest_distance = front[closest]

        if closest_distance < 1.0:
            bubble = 28
        elif closest_distance < 2.0:
            bubble = 20
        else:
            bubble = 12

        b0 = max(0,closest-bubble)
        b1 = min(len(front)-1,closest+bubble)
        front[b0:b1+1] = 0.0

        gap_start,gap_end = self.find_max_gap(front)
        best = self.find_best_point(gap_start,gap_end,front)

        real = start_idx + best

        steering = data.angle_min + real*data.angle_increment

        steering = np.clip(
            steering,
            -self.max_steering_angle,
            self.max_steering_angle
        )

        steering = (
            0.6*self.previous_steering +
            0.4*steering
        )

        self.previous_steering = steering

        center = len(front)//2

        forward_distance = np.mean(
            front[max(0,center-15):min(len(front),center+15)]
        )

        curve_factor = abs(steering)/self.max_steering_angle
        curve_factor = np.clip(curve_factor,0.0,1.0)

        distance_factor = np.clip(forward_distance/5.0,0.0,1.0)

        speed = (
            self.min_speed +
            (self.max_speed-self.min_speed)
            * (1-curve_factor)
            * distance_factor
        )

        if forward_distance < 0.7:
            speed = min(speed,2.0)

        alpha = 0.25

        self.current_speed = (
            (1-alpha)*self.current_speed +
            alpha*speed
        )

        msg = AckermannDriveStamped()
        msg.drive.steering_angle = float(steering)
        msg.drive.speed = float(self.current_speed)

        self.drive_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = GapFollow()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()