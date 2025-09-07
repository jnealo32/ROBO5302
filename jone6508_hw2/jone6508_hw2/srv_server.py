import rclpy
from rclpy.node import Node
from time import perf_counter

from jone6508_service.srv import Jone6508Service
#from std_msgs.msg import String, Float64

class ReverseService(Node):
    def __init__(self):
        super().__init__('test_service_server')
        self.srv = self.create_service(Jone6508Service, 'run_reverse_service', self.perform_service)
        self.get_logger().info("Service 'run_reverse_service' ready.")

    def perform_service(self, request, response):
        time_start = perf_counter()

        request_data = request.input.data
        
        response_data = request_data[::-1]

        time_elapsed = perf_counter() - time_start

        response.output.data = response_data
        response.service_runtime.data = time_elapsed
        return response

def main():
    rclpy.init()
    node = ReverseService()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()
