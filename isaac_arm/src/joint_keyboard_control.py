#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import sys
import termios
import tty
import select

class JointKeyboardControl(Node):
    def __init__(self):
        super().__init__('joint_keyboard_control')
        self.publisher_ = self.create_publisher(JointState, '/joint_command', 10)
        self.joint_names = [
            'right_j0',
            'head_pan',
            'right_j1',
            'right_j2',
            'right_j3',
            'right_j4',
            'right_j5',
            'right_j6'
        ]
        self.joint_positions = [0.0 for _ in range(8)]
        self.selected_joint = 0
        self.step_size = 0.01
        self.old_settings = termios.tcgetattr(sys.stdin)
        self.print_instructions()

    def print_instructions(self):
        print("\n=== 鍵盤控制（8 軸版） ===")
        print("1-8: 選擇關節")
        print("a/d: 調整關節位置（a=減小, d=增大）")
        print("q: 退出程式")
        print("當前關節:", self.joint_names[self.selected_joint])
        print("當前位置:", self.joint_positions[self.selected_joint])

    def get_key(self):
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.read(1)
        return None

    def run(self):
        try:
            tty.setcbreak(sys.stdin.fileno())

            while rclpy.ok():
                key = self.get_key()
                if key is not None:
                    if key in [str(i) for i in range(1, 9)]:
                        self.selected_joint = int(key) - 1
                        print("\n當前關節:", self.joint_names[self.selected_joint])
                        print("當前位置:", self.joint_positions[self.selected_joint])
                    elif key == 'a':
                        self.joint_positions[self.selected_joint] -= self.step_size
                        self.publish_joint_command()
                        print("位置 -:", self.joint_positions[self.selected_joint])

                    elif key == 'd':
                        self.joint_positions[self.selected_joint] += self.step_size
                        self.publish_joint_command()
                        print("位置 +:", self.joint_positions[self.selected_joint])
                    elif key == 'q':
                        print("\n退出程式...")
                        break
                rclpy.spin_once(self, timeout_sec=0.01)

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def publish_joint_command(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = self.joint_positions
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    joint_keyboard_control = JointKeyboardControl()

    try:
        joint_keyboard_control.run()
    except KeyboardInterrupt:
        pass
    finally:
        joint_keyboard_control.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
