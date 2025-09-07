import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from std_msgs.msg import Header

class LatencySubscriber(Node):
    def __init__(self):
        super().__init__('latency_subscriber')
        self.sub = self.create_subscription(Header, "pubsub_test", self.on_msg, 10)
        self.latencies = []
        self.get_logger().info(f"Subscribing on 'pubsub_test' for 400 messages...")

    def on_msg(self, msg: Header):
        # Compute latency = now - header.stamp
        t_pub = Time.from_msg(msg.stamp)
        t_now = self.get_clock().now()
        dt = (t_now - t_pub).nanoseconds / 1e9  # seconds
        self.latencies.append(dt)

        if len(self.latencies) >= 400:
            self.plot_histogram()

    def plot_histogram(self):
        vals_ms = [v * 1e3 for v in self.latencies]
        right = (max(vals_ms) if vals_ms else 1.0)

        plt.figure()
        plt.hist(vals_ms, bins=40)
        plt.xlim(0, 5)
        plt.ylim(0, 180)

        plt.title("Topic Transfer Latency (ms)")
        plt.xlabel("Transfer latency (ms)")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig('topic_latency_hist.png')
        self.get_logger().info("400 messages recieved. topic_latency_hist.png saved.")
        rclpy.shutdown()  # stop the executor cleanly

def main():
    rclpy.init()
    node = LatencySubscriber()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        # rclpy.shutdown() happens in _plot_and_exit()

if __name__ == '__main__':
    main()