import rclpy
from rclpy.node import Node
from std_msgs.msg import Header

class LatencyPublisher(Node):
    def __init__(self):
        super().__init__('latency_publisher')
        self.pub = self.create_publisher(Header, "pubsub_test", 10)
        self.sent = 0
        timer_period = 0.02
        self.timer = self.create_timer(timer_period, self.publish_callback)
        self.get_logger().info(f"Publishing 400 messages on pubsub_test")

    def publish_callback(self):
        if self.sent >= 400:
            self.timer.cancel()
            self.get_logger().info("Done publishing; Ctrl+C to stop node.")
            return
        h = Header()
        h.stamp = self.get_clock().now().to_msg()   # publish current time in header
        self.pub.publish(h)
        self.sent += 1

def main():
    rclpy.init()
    node = LatencyPublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

    