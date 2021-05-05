"""
Start up the blossom webserver, CLI client, and web client.
"""

# make sure that prints will be supported
from __future__ import print_function
import sys
import yaml
import argparse
import os
import shutil
import signal
from config import RobotConfig
from src import robot, sequence
from sequencerobot import SequenceRobot
import re
from serial.serialutil import SerialException
from pypot.dynamixel.controller import DxlError
import random
import time
import threading
import uuid
import requests
# seed time for better randomness
random.seed(time.time())

master_robot = None
robots = []

'''
CLI Code
'''


def start_cli(robot):
    """
    Start CLI as a thread
    """
    print("cli started")
    t = threading.Thread(target=run_cli, args=[master_robot])
    t.daemon = True
    t.start()
    print("\ncli started 2")


def run_cli(robot):
    """
    Handle CLI inputs indefinitely
    """
    while(1):
        # handle the command and arguments
        handle_input(master_robot, 'm')
        print(master_robot.motors)
    print("\ncli not running")


def handle_quit():
    """
    Close the robot object and clean up any temporary files.
    Manually kill the flask server because there isn't an obvious way to do so gracefully.

    Raises:
        ???: Occurs when yarn failed to start but yarn_process was still set to true.
    """
    print("Exiting...")
    for bot in robots:
        # clean up tmp dirs and close robots
        tmp_dir = './src/sequences/%s/tmp' % bot.name
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        bot.robot.close()
    print("Bye!")
    # TODO: Figure out how to kill flask gracefully


last_cmd, last_args = 'rand', []


def handle_input(robot, cmd, args=[]):
    """
    handle CLI input

    Args:
        robot: the robot affected by the given command
        cmd: a robot command
        args: additional args for the command
    """
    # manipulate the global speed and amplitude vars
    # global speed
    # global amp
    # global post
    # print(cmd, args)
    # separator between sequence and idler
    global last_cmd, last_args
    idle_sep = '='

    ###?????###
    if cmd == 'm':
        # get motor and pos if not given
        if not args:
            args = ['', '', '']
            args[0] = input('Motor # (1, 2, 3): ')
            args[1] = input('Position: ')
            args[2] = input('Speed: ')
        for bot in robots:
            bot.speed = float(args[2])
        for bot in robots:
            if (args[0] == 'all'):
                bot.goto_position({'tower_1': float(args[1]), 'tower_2': float(args[1]), 'tower_3': float(args[1])}, 0, True)
            else:
                args[0] = 'tower_'+str(args[0])
                bot.goto_position({args[0]: float(args[1])}, 0, True)

    # adjust speed (0.5 to 2.0)
    elif cmd == 'e':
        for bot in robots:
            bot.speed = float(raw_input('Speed factor: '))
    # adjust amplitude (0.5 to 2.0)
    elif cmd == 'a':
        for bot in robots:
            bot.amp = float(raw_input('Amplitude factor: '))
    # adjust posture (-150 to 150)
    elif cmd == 'p':
        for bot in robots:
            bot.post = float(raw_input('Posture factor: '))

    # help
    elif cmd == 'h':
        exec('help(' + input('Help: ') + ')')

    # manual control
    elif cmd == 'man':
        while True:
            try:
                exec(input('Command: '))
            except KeyboardInterrupt:
                break

    #elif cmd == '':
        #handle_input(master_robot, last_cmd, last_args)
        #return
    # directly call a sequence (skip 's')
    #elif cmd in robot.seq_list.keys():
        #args = [cmd]
        #cmd = 's'
        #handle_input(master_robot, cmd, args)
    # directly call a random sequence by partial name match
    #elif [cmd in seq_name for seq_name in robot.seq_list.keys()]:
        # print(args[0])
        #if 'mix' not in cmd:
            #seq_list = [seq_name for seq_name in robot.seq_list.keys() if cmd in seq_name and 'mix' not in seq_name]
        #else:
        #    seq_list = [seq_name for seq_name in robot.seq_list.keys() if cmd in seq_name]

        #if len(seq_list) == 0:
        #    print("No sequences matching name: %s" % (cmd))
        #    return
        #handle_input(master_robot, 's', [random.choice(seq_list)])
        #cmd = cmd

    # elif cmd == 'c':
    #     robot.calibrate()

    else:
        print("Invalid input")
        return
    last_cmd, last_args = cmd, args


def record(robot):
    """
    Start new recording session on the robot
    """
    # stop recording if one is happening
    if not robot.rec_stop:
        robot.rec_stop = threading.Event()
    # start recording thread
    robot.rec_stop.set()
    robot.start_recording()


def stop_record(robot, seq_name=""):
    """
    Stop recording
    args:
        robot       the robot under which to save the sequence
        seq_name    the name of the sequence
    returns:
        the name of the saved sequence
    """
    # stop recording
    robot.rec_stop.set()

    # if provided, save sequence name
    if seq_name:
        seq = robot.rec_thread.save_rec(seq_name, robots=robots)
        store_gesture(seq_name, seq)
    # otherwise, give it ranodm remporary name
    else:
        seq_name = uuid.uuid4().hex
        robot.rec_thread.save_rec(seq_name, robots=robots, tmp=True)

    # return name of saved sequence
    return seq_name


def store_gesture(name, sequence, label=""):
    """
    Save a sequence to GCP datastore
    args:
        name: the name of the sequence
        sequence: the sequence dict
        label: a label for the sequence
    """
    url = "https://classification-service-dot-blossom-gestures.appspot.com/gesture"
    payload = {
        "name": name,
        "sequence": sequence,
        "label": label,
    }
    requests.post(url, json=payload)


'''
Main Code
'''


def main(args):
    """
    Start robots, start up server, handle CLI
    """
    # get robots to start
    global master_robot
    global robots

    # use first name as master
    configs = RobotConfig().get_configs(args.names)
    print(configs)
    master_robot = safe_init_robot(args.names[0], configs[args.names[0]])
    configs.pop(args.names[0])
    # start robots
    robots = [safe_init_robot(name, config)
              for name, config in configs.items()]
    robots.append(master_robot)

    master_robot.reset_position()

    # start CLI
    start_cli(master_robot)
    while True:
        time.sleep(1)



def safe_init_robot(name, config):
    """
    Safely start/init robots, due to sometimes failing to start motors
    args:
        name    name of the robot to start
        config  the motor configuration of the robot
    returns:
        the started SequenceRobot object
    """
    # SequenceRobot
    bot = None
    # limit of number of attempts
    attempts = 10

    # keep trying until number of attempts reached
    while bot is None:
        try:
            bot = SequenceRobot(name, config)
        except (DxlError, NotImplementedError, RuntimeError, SerialException) as e:
            if attempts <= 0:
                raise e
            print(e, "retrying...")
            attempts -= 1
    return bot


def parse_args(args):
    """
    Parse arguments from starting in terminal
    args:
        args    the arguments from terminal
    returns:
        parsed arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--names', '-n', type=str, nargs='+',
                        help='Name of the robot.', default=["woody"])
    parser.add_argument('--port', '-p', type=int,
                        help='Port to start server on.', default=8000)
    # parser.add_argument('--host', '-i', type=str, help='IP address of webserver',
    #                     default=srvr.get_ip_address())
    parser.add_argument('--browser-disable', '-b',
                        help='prevent a browser window from opening with the blossom UI',
                        action='store_true')
    parser.add_argument('--list-robots', '-l',
                        help='list all robot names', action='store_true')
    return parser.parse_args(args)


"""
Generic main handler
"""
if __name__ == "__main__":
    main(parse_args(sys.argv[1:]))