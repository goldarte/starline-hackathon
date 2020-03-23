#!/usr/bin/env python

# Title:        Turtlebot Navigation Stack
# File:         rviz_interface.py
# Date:         2017-02-13
# Author:       Preben Jensen Hoel and Paul-Edouard Sarlin
# Description:  Publishes the map and path as standard ROS messages to be
#               displayed in Rviz.

import rospy
from nav_msgs.msg import OccupancyGrid


class WallBuilder:
    def __init__(self):
        self.pub_map = rospy.Publisher("/robot_0/move_base/local_costmap/costmap2", OccupancyGrid, queue_size=1, latch=True)

        self.map = OccupancyGrid()
        self.map.header.frame_id = "map"
        self.map.info.resolution = 0.1
        self.map.info.width = int(12 / self.map.info.resolution)
        self.map.info.height = int(12 / self.map.info.resolution)
        self.map.info.origin.position.x = -3
        self.map.info.origin.position.y = -3
        self.map.info.origin.position.z = 0

    # Contruct and publish the map message (Occupancy Grid)
    def publishMap(self, walls):
        # Initialize 2D map with zeros
        map = []
        for i in range(self.map.info.height):
            row = []
            for j in range(self.map.info.width):
                row.append(0)
            map.append(row)

        # Iterate through the lines, set the pixels accordingly

        for [(x1, y1), (x2, y2)] in walls:

            # https://ru.wikipedia.org/wiki/%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D0%91%D1%80%D0%B5%D0%B7%D0%B5%D0%BD%D1%85%D1%8D%D0%BC%D0%B0

            for x in range(x1, x2):
                y = int((y2 - y1) * (x - x1) / (x2 - x1) + y1)
                map[x][y] = 100

            for y in range(y1, y2):
                x = int((y - y1) * (x2 - x1) / (y2 - y1) + x1)
                map[x][y] = 100

        self.map.data = []

        # Flatten map to self.map.data in a row-major order, publish
        for i in range(len(map)):
            for j in range(len(map[0])):
                self.map.data.append(map[j][i])
        self.pub_map.publish(self.map)


if __name__ == "__main__":
    rospy.init_node("test_publish_walls")
    w = WallBuilder()
    walls = [[(40, 20), (100, 110)]]
    # walls = [[(20, 0), (40, 40)], [(0, 20), (40, 50)], [(0, 20), (40, 20)], [(10, 20), (100, 110)]]
    print(w.map)

    try:
        r = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            w.publishMap(walls)
            r.sleep()
    except rospy.ROSInterruptException:
        pass
