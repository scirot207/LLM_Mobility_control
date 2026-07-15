from geometry_msgs.msg import TwistStamped
import math

LINEAR_SPEED = 0.3      # m/s
ANGULAR_SPEED = 1.0     # rad/s


def parse(data, node):

    motions = []

    for command in data.get("commands", []):

        action = command.get("action", "").upper()
        value = command.get("value", 0)

        msg = TwistStamped()

        msg.header.stamp = node.get_clock().now().to_msg()
        msg.header.frame_id = "base_link"

        duration = 0.0

        if action == "FORWARD":
            msg.twist.linear.x = LINEAR_SPEED
            duration = value / LINEAR_SPEED

        elif action == "BACKWARD":
            msg.twist.linear.x = -LINEAR_SPEED
            duration = value / LINEAR_SPEED

        elif action == "LEFT":
            msg.twist.angular.z = ANGULAR_SPEED
            duration = math.radians(value) / ANGULAR_SPEED

        elif action == "RIGHT":
            msg.twist.angular.z = -ANGULAR_SPEED
            duration = math.radians(value) / ANGULAR_SPEED

        elif action == "STOP":
            duration = 0.0

        else:
            print(f"Unknown action: {action}")
            continue

        motions.append((msg, duration))

    return motions
