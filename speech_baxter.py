#!/usr/bin/env python
# coding=utf-8

import argparse

import rospy

import baxter_interface
import baxter_external_devices

from baxter_interface import CHECK_VERSION
from speech.msg import voicemsg

speech_command = 10
def callback(msg):
    rospy.loginfo("Received speech command: %d.",msg.order)
    global speech_command
    speech_command = msg.order

def bin_to_str(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

def move():
    sub = rospy.Subscriber("voice_msg", voicemsg, callback, queue_size=1, buff_size=1, tcp_nodelay=True)

    right = baxter_interface.Limb('right')
    grip_right = baxter_interface.Gripper('right', CHECK_VERSION)
    rj = right.joint_names()

    def set_j(limb, joint_name, delta):
        current_position = limb.joint_angle(joint_name)
        joint_command = {joint_name: current_position + delta}
        limb.set_joint_positions(joint_command)

    bindings = {
        '1': (set_j, [right, rj[5], -0.1], "向前运动"),
        '2': (set_j, [right, rj[5], 0.1], "向后运动"),
        '3': (set_j, [right, rj[4], 0.1], "向右运动"),
        '4': (set_j, [right, rj[4], -0.1], "向左运动"),
        '5': (grip_right.open, [], "手爪打开"),
        '6': (grip_right.close, [], "手爪关合"),
        '7': (set_j, [right, rj[6], 0.1], "手腕翻转"),
        
     }
    done = False
    global speech_command
    while not done and not rospy.is_shutdown():
        # print('speech_command', speech_command)
        
        # print(type(speech_command), speech_command)
        if speech_command :
            speech_command = str(speech_command)
            #catch Esc or ctrl-c
            if speech_command in ['\x1b', '\x03']:
                done = True
                rospy.signal_shutdown("Example finished.")
            elif speech_command in bindings:
                cmd = bindings[speech_command]
                #expand binding to something like "set_j(right, 's0', 0.1)"
                cmd[0](*cmd[1])
                print("command: %s" % (cmd[2],))
            else:
                print("key bindings: ")
                print("  Esc: Quit")
                print("  ?: Help")
                for key, val in sorted(bindings.items(),
                                       key=lambda x: x[1][2]):
                    print("  %s: %s" % (key, val[2]))
        speech_command = None



def main():
    """RSDK Joint Position Example: Keyboard Control

    Use your dev machine's keyboard to control joint positions.

    Each key corresponds to increasing or decreasing the angle
    of a joint on one of Baxter's arms. Each arm is represented
    by one side of the keyboard and inner/outer key pairings
    on each row for each joint.
    """
    epilog = """
See help inside the example with the '?' key for key bindings.
    """
    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=arg_fmt,
                                     description=main.__doc__,
                                     epilog=epilog)
    parser.parse_args(rospy.myargv()[1:])

    print("Initializing node... ")
    rospy.init_node("rsdk_joint_position_keyboard")
    print("Getting robot state... ")
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    init_state = rs.state().enabled

    def clean_shutdown():
        print("\nExiting example...")
        if not init_state:
            print("Disabling robot...")
            rs.disable()
    rospy.on_shutdown(clean_shutdown)

    print("Enabling robot... ")
    rs.enable()
    
    move()
    print("Done.")


if __name__ == '__main__':
    main()
