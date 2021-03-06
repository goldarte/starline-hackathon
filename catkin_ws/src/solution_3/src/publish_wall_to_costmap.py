#!/usr/bin/env python

# Title:        WallBuilder
# File:         publish_wall_to_costmap.py
# Date:         2020-03-22
# Author:       Artem Smirnov @urpylka
# Description:  It publish lines from input array to the map

import rospy
from nav_msgs.msg import OccupancyGrid

def cleanGrid(_map):
    if _map is None:
        return

    data = []
    for i in range(_map.info.height * _map.info.width):
        data.append(0)
    _map.data = data

class WallBuilder:

    def __init__(self, pub_topic):
        self.pub_map = rospy.Publisher(pub_topic, OccupancyGrid, queue_size=1, latch=True)

        self.map = OccupancyGrid()
        self.map.header.frame_id = "map"
        self.map.info.resolution = 0.0502257
        self.map.info.width = 220
        self.map.info.height = 220
        self.map.info.origin.position.x = 0.0
        self.map.info.origin.position.y = 0.0
        self.map.info.origin.position.z = 0
        cleanGrid(self.map)

        self.pub_map.publish(self.map)


    def publishMap(self, walls):
        """
        Contruct and publish the map message (Occupancy Grid)
        """
        # Initialize 2D map with zeros
        g = []
        for i in range(self.map.info.height):
            row = []
            for j in range(self.map.info.width):
                row.append(0)
            g.append(row)

        # Iterate through the lines, set the pixels accordingly

        for [(x1, y1), (x2, y2)] in walls:

            x1 = int(x1 / self.map.info.resolution)
            x2 = int(x2 / self.map.info.resolution)
            y1 = int(y1 / self.map.info.resolution)
            y2 = int(y2 / self.map.info.resolution)

            sr = "x1: " + str(x1) + ", y1: " + str(y1) + ", x2: " + str(x2) + ", y2: " + str(y2)
            # rospy.loginfo(sr)

            # https://ru.wikipedia.org/wiki/%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_%D0%91%D1%80%D0%B5%D0%B7%D0%B5%D0%BD%D1%85%D1%8D%D0%BC%D0%B0

            for x in range(x1, x2):
                y = int((y2 - y1) * (x - x1) / (x2 - x1) + y1)
                g[x][y] = 100

            for y in range(y1, y2):
                x = int((y - y1) * (x2 - x1) / (y2 - y1) + x1)
                g[x][y] = 100

        self.map.data = []

        # Flatten map to self.map.data in a row-major order, publish
        for i in range(len(g)):
            for j in range(len(g[0])):
                self.map.data.append(g[j][i])

        self.pub_map.publish(self.map)


if __name__ == "__main__":
    rospy.init_node("test_publish_walls")
    w = WallBuilder("/maps/walls")
    walls = [[(40, 40), (40, 80)]]
    # walls = [[(20, 0), (40, 40)], [(0, 20), (40, 50)], [(0, 20), (40, 20)], [(10, 20), (100, 110)]]
    # print(w.map)

    try:
        r = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            w.publishMap(walls)
            r.sleep()
    except rospy.ROSInterruptException:
        pass
