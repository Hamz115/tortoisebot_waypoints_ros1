#!/usr/bin/env python3

import rospy
import unittest
import actionlib
from tortoisebot_waypoints.msg import WaypointAction, WaypointGoal
from geometry_msgs.msg import Point
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
import math


class TestWaypointActionServer(unittest.TestCase):
    def setUp(self):
        rospy.init_node('test_waypoint_action_server')
        self.client = actionlib.SimpleActionClient(
            'tortoisebot_as', WaypointAction)
        self.client.wait_for_server()
        self.odom_subscriber = rospy.Subscriber(
            '/odom', Odometry, self.odom_callback)
        self.current_position = None
        self.current_yaw = None

        # Get target position from ROS parameters
        self.target_x = rospy.get_param('~target_x', 0.5)
        self.target_y = rospy.get_param('~target_y', 0.5)
        self.tolerance = rospy.get_param('~tolerance', 0.1)

    def odom_callback(self, msg):
        self.current_position = msg.pose.pose.position
        orientation = msg.pose.pose.orientation
        _, _, self.current_yaw = euler_from_quaternion(
            [orientation.x, orientation.y, orientation.z, orientation.w])

    def test_position(self):
        goal = WaypointGoal()
        goal.position = Point(self.target_x, self.target_y, 0.0)
        self.client.send_goal(goal)
        # Wait up to 60 seconds for the result
        self.client.wait_for_result(rospy.Duration(60))

        # Give some time for the final odometry message to arrive
        rospy.sleep(2)

        self.assertIsNotNone(self.current_position)
        self.assertAlmostEqual(self.current_position.x,
                               self.target_x, delta=self.tolerance)
        self.assertAlmostEqual(self.current_position.y,
                               self.target_y, delta=self.tolerance)

    def test_rotation(self):
        goal = WaypointGoal()
        goal.position = Point(self.target_x, self.target_y, 0.0)
        self.client.send_goal(goal)
        # Wait up to 60 seconds for the result
        self.client.wait_for_result(rospy.Duration(60))

        # Give some time for the final odometry message to arrive
        rospy.sleep(2)

        self.assertIsNotNone(self.current_yaw)
        expected_yaw = math.atan2(self.target_y, self.target_x)
        self.assertAlmostEqual(
            self.current_yaw, expected_yaw, delta=self.tolerance)


if __name__ == '__main__':
    import rostest
    rostest.rosrun('tortoisebot_waypoints',
                   'test_waypoint_action_server', TestWaypointActionServer)
