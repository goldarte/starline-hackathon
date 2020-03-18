#!/bin/bash
git subtree pull --prefix ../drivers_ws/src/rplidar_ros/       https://github.com/robopeak/rplidar_ros.git     master   --squash -m "auto-update subtree" && \
git subtree pull --prefix ../drivers_ws/src/ros_astra_camera/  https://github.com/orbbec/ros_astra_camera.git  master   --squash -m "auto-update subtree" && \
git subtree pull --prefix ../drivers_ws/src/kobuki/            https://github.com/yujinrobot/kobuki.git        kinetic  --squash -m "auto-update subtree" && \
git subtree pull --prefix ../drivers_ws/src/kobuki_msg/        https://github.com/yujinrobot/kobuki_msgs.git   kinetic  --squash -m "auto-update subtree" && \
git subtree pull --prefix ../drivers_ws/src/kobuki_core/       https://github.com/yujinrobot/kobuki_core.git   kinetic  --squash -m "auto-update subtree"
