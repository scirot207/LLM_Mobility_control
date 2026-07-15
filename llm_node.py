import threading
import time

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TwistStamped

from .llm_api import ask_llm
from .command_parser import parse

import math
from sensor_msgs.msg import LaserScan


class LLMController(Node):

    def __init__(self):

        super().__init__("llm_controller")

        self.publisher = self.create_publisher(
            TwistStamped,
            "/cmd_vel",
            10
        )

        self.scan_subscriber = self.create_subscription(
            LaserScan,
            "/scan",
            self.scan_callback,
            10
        )

        self.scan_summary = {
            "front": None,
            "left": None,
            "right": None
        }

        self.get_logger().info("LLM Controller Started")

        thread = threading.Thread(target=self.input_loop)
        thread.daemon = True
        thread.start()

    def input_loop(self):

        while rclpy.ok():

            user_input = input("\n사용자 : ")

            lidar_info = f"""
            Current LiDAR

            Front : {self.scan_summary["front"]:.2f} m
            Left  : {self.scan_summary["left"]:.2f} m
            Right : {self.scan_summary["right"]:.2f} m
            """
            
            llm_result = ask_llm(user_input, lidar_info)

            print("LLM :", llm_result)

            motions = parse(llm_result, self)

            if not motions:
                print("Unknown LLM Output")
                continue

            for msg, duration in motions:

                self.publisher.publish(msg)

                #print(f"Published ({duration:.2f}s)")
                time.sleep(duration)
                stop_msg = TwistStamped()

                stop_msg.header.stamp = self.get_clock().now().to_msg()
                stop_msg.header.frame_id = "base_link"

                self.publisher.publish(stop_msg)

                #print("STOP")

                time.sleep(0.1)

    def get_sector_distance(self, ranges):

        valid = [
            r for r in ranges
            if math.isfinite(r) and r > 0.05
        ]

        if len(valid) == 0:
            return float("inf")

        valid.sort()

        k = min(5, len(valid))

        return sum(valid[:k]) / k



    def scan_callback(self, msg):

        ranges = list(msg.ranges)

        # 전방 ±10도
        front = ranges[-10:] + ranges[:10]

        # 좌측
        left = ranges[80:100]

        # 우측
        right = ranges[260:280]

        self.scan_summary["front"] = self.get_sector_distance(front)
        self.scan_summary["left"] = self.get_sector_distance(left)
        self.scan_summary["right"] = self.get_sector_distance(right)

def main():

    rclpy.init()

    node = LLMController()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":

    main()
