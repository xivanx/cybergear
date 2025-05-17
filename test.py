import os
import sys
# 添加pcan_cybergear库的路径
sys.path.append(os.path.join("cybergear"))

from pcan_cybergear import CANMotorController
import can
import logging
import time
# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to the CAN bus with 1 Mbit/s bitrate
bus = can.interface.Bus(bustype='slcan', channel='/dev/tty.usbmodem8334301', bitrate=1000000)
motor = CANMotorController(bus, motor_id=127, main_can_id=254)

jog_vel = 3.14  # rad/s
uint_value = motor._float_to_uint(jog_vel, motor.V_MIN, motor.V_MAX, 16)
jog_vel_bytes = motor.format_data(data=[uint_value], format="u16", type="encode")[:2][::-1]

data1 = [0x05, 0x70, 0x00, 0x00, 0x07, 0x01] + jog_vel_bytes
motor.clear_can_rx()
received_msg_data, received_msg_arbitration_id = motor.send_receive_can_message(
    cmd_mode=motor.CmdModes.SINGLE_PARAM_WRITE, data2=motor.MAIN_CAN_ID, data1=data1
)
motor.parse_received_msg(received_msg_data, received_msg_arbitration_id)
time.sleep(30)
motor.disable()