import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry
import math
import time

MOVE_TIME = 3.0        # seconds
FORWARD_SPEED = 0.10   # m/s


class TimedMove(Node):

    def __init__(self):
        super().__init__('timed_move')

        self.cmd_pub = self.create_publisher(
            TwistStamped,
            '/cmd_vel',
            10
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.start_x = None
        self.start_y = None
        self.start_time = None
        self.finished = False

        self.timer = self.create_timer(0.1, self.control_loop)

    def odom_callback(self, msg):
        if self.start_x is None:
            self.start_x = msg.pose.pose.position.x
            self.start_y = msg.pose.pose.position.y

        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y

    def control_loop(self):

        if self.start_x is None:
            return

        if self.start_time is None:
            self.start_time = time.time()
            self.get_logger().info("Starting 3 second movement")

        elapsed = time.time() - self.start_time

        twist = TwistStamped()

        if elapsed < MOVE_TIME:
            twist.twist.linear.x = FORWARD_SPEED
            self.cmd_pub.publish(twist)

        elif not self.finished:
            twist.twist.linear.x = 0.0
            self.cmd_pub.publish(twist)

            distance = math.sqrt(
                (self.current_x - self.start_x) ** 2 +
                (self.current_y - self.start_y) ** 2
            )

            self.get_logger().info(
                f"Finished. Distance traveled: {distance:.3f} meters"
            )

            self.finished = True


def main(args=None):
    rclpy.init(args=args)
    node = TimedMove()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()