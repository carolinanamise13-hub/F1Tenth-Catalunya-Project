#!/usr/bin/env python3

import time

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry


class LapCounter(Node):
    def __init__(self):
        super().__init__('lap_counter')

        self.odom_sub = self.create_subscription(
            Odometry,
            '/ego_racecar/odom',
            self.odom_callback,
            10
        )

        self.start_x = None
        self.start_y = None

        self.lap_count = 0
        self.start_time = None
        self.best_lap = None
        self.total_time = 0.0

        self.was_near_start = False
        self.left_start_zone = False

        self.start_radius = 0.8
        self.min_distance_to_activate = 3.0

        self.get_logger().info("Contador iniciado. La posición inicial será la meta.")

    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        if self.start_x is None:
            self.start_x = x
            self.start_y = y
            self.start_time = time.time()

            self.get_logger().info(
                f"Meta guardada en x={self.start_x:.2f}, y={self.start_y:.2f}"
            )
            return

        distance_to_start = (
            (x - self.start_x) ** 2 +
            (y - self.start_y) ** 2
        ) ** 0.5

        if distance_to_start > self.min_distance_to_activate:
            self.left_start_zone = True

        near_start = distance_to_start < self.start_radius

        if near_start and self.left_start_zone and not self.was_near_start:
            current_time = time.time()
            lap_time = current_time - self.start_time
            self.start_time = current_time

            self.total_time += lap_time

            if self.best_lap is None or lap_time < self.best_lap:
                self.best_lap = lap_time

            self.lap_count += 1
            self.left_start_zone = False

            self.get_logger().info("")
            self.get_logger().info("=" * 40)
            self.get_logger().info(f"VUELTA {self.lap_count}")
            self.get_logger().info(f"Tiempo de vuelta : {lap_time:.2f} s")
            self.get_logger().info(f"Mejor vuelta     : {self.best_lap:.2f} s")
            self.get_logger().info("=" * 40)

            if self.lap_count >= 10:
                promedio = self.total_time / self.lap_count

                self.get_logger().info("")
                self.get_logger().info("*" * 45)
                self.get_logger().info("10 VUELTAS COMPLETADAS")
                self.get_logger().info(f"Tiempo total : {self.total_time:.2f} s")
                self.get_logger().info(f"Mejor vuelta : {self.best_lap:.2f} s")
                self.get_logger().info(f"Promedio     : {promedio:.2f} s")
                self.get_logger().info("*" * 45)

        self.was_near_start = near_start


def main(args=None):
    rclpy.init(args=args)
    node = LapCounter()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()