
from time import perf_counter
from statistics import mean
import rclpy
from rclpy.node import Node

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from jone6508_service.srv import Jone6508Service
from std_msgs.msg import String

class ReverseClient(Node):
    def __init__(self):
        super().__init__('test_service_client')
        self.cli = self.create_client(Jone6508Service, 'run_reverse_service')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service...')
        self.req = Jone6508Service.Request()

    def send_request(self, msg_str: str):
        self.req.input = String(data=msg_str)

        time_start = perf_counter()
        future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, future)
        time_elapsed = perf_counter() - time_start

        res = future.result()
        if res is None:
            raise RuntimeError('Service call failed')
        
        transfer_latency = max(time_elapsed - float(res.service_runtime.data), 0.0)
        return time_elapsed, transfer_latency, res.output.data

def main():
    rclpy.init()
    node = ReverseClient()
    try:
        N = 400
        request = "testing"
        latencies = []

        for i in range(N):
            _, transfer_latency, _ = node.send_request(request)
            latencies.append(transfer_latency)
            if (i + 1) % 50 == 0:
                node.get_logger().info(f"Completed {i+1}/{N}")


    ### storing latencies in a CSV ###
        out = 'service_transfer_latencies.csv'
        with open(out, 'w') as f:
            f.write('\n'.join(f'{x:.9f}' for x in latencies))  # seconds, one per line
        print(f"Wrote {len(latencies)} values to {out}")
        
    finally:
        node.destroy_node()
        rclpy.shutdown()

    ### histogram ###
    vals_ms = [v * 1e3 for v in latencies]
    right = (max(vals_ms) if vals_ms else 1.0)
    plt.hist(vals_ms, bins=40)
    plt.xlim(0, 5)
    plt.ylim(0, 180)

    plt.title("Service Transfer Latency (ms)")
    plt.xlabel("Transfer latency (ms)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig('service_latency_hist.png')
    rclpy.shutdown()



if __name__ == '__main__':
    main()