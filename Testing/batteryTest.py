#!/bin/python3
import time
import socket
import struct
from quaternion import Quaternion
# import CubeAxes
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import time
from threading import Timer

UDP_IP = "127.0.0.1"
UDP_PORT = 6969
class CubeAxes(plt.Axes):
    """An Axes for displaying a 3D cube"""
    # fiducial face is perpendicular to z at z=+1
    one_face = np.array([[1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1], [1, 1, 1]])

    # construct six rotators for the face
    # x, y, z = np.eye(3)[0]
    rots = [Quaternion.from_v_theta(np.eye(3)[0], theta) for theta in (np.pi / 2, -np.pi / 2)]
    rots += [Quaternion.from_v_theta(np.eye(3)[1], theta) for theta in (np.pi / 2, -np.pi / 2)]
    rots += [Quaternion.from_v_theta(np.eye(3)[1], theta) for theta in (np.pi, 0)]
    
    # colors of the faces
    colors = ['blue', 'green', 'white', 'yellow', 'orange', 'red']
    
    def __init__(self, fig, rect=[0, 0, 1, 1], *args, **kwargs):
        # define the current rotation
        self.current_rot = Quaternion.from_v_theta((1, 1, 0), np.pi / 6)
        
    

class PacketTypes:
    PACKET_HEARTBEAT = 0
    ##define PACKET_ROTATION 1 // Deprecated
    ##define PACKET_GYRO 2 // Deprecated
    PACKET_HANDSHAKE = 3
    PACKET_ACCEL = 4
    ##define PACKET_MAG 5 // Deprecated
    PACKET_RAW_CALIBRATION_DATA = 6
    PACKET_CALIBRATION_FINISHED = 7
    PACKET_CONFIG = 8
    ##define PACKET_RAW_MAGNETOMETER 9 // Deprecated
    PACKET_PING_PONG = 10
    PACKET_SERIAL = 11
    PACKET_BATTERY_LEVEL = 12
    PACKET_TAP = 13
    PACKET_ERROR = 14
    PACKET_SENSOR_INFO = 15
    ##define PACKET_ROTATION_2 16 // Deprecated
    PACKET_ROTATION_DATA = 17
    PACKET_MAGNETOMETER_ACCURACY = 18
    PACKET_SIGNAL_STRENGTH = 19
    PACKET_TEMPERATURE = 20

    PACKET_INSPECTION = 105 // 0x69

    PACKET_RECEIVE_HEARTBEAT = 1
    PACKET_RECEIVE_VIBRATE = 2
    PACKET_RECEIVE_HANDSHAKE = 3
    PACKET_RECEIVE_COMMAND = 4

    PACKET_INSPECTION_PACKETTYPE_RAW_IMU_DATA = 1
    PACKET_INSPECTION_PACKETTYPE_FUSED_IMU_DATA = 2
    PACKET_INSPECTION_PACKETTYPE_CORRECTION_DATA = 3
    PACKET_INSPECTION_DATATYPE_INT = 1
    PACKET_INSPECTION_DATATYPE_FLOAT = 2

connected = False;
HandshakeMessage = b"\03Hey OVR =D 5"
HeartbeatMessage = b"\00\01"

def sendHeartbeat(sock, addr):
    sock.sendto(HeartbeatMessage, addr)

class HeartbeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args,**self.kwargs)
heartbeat = None
lastPacket = time.time()

def parseMessage(sock, data, addr, ax):
    global connected
    global heartbeat
    global lastPacket
    # print ("data[3]: %s" % data[3])
    # print(addr)
    match data[3]:
        case PacketTypes.PACKET_HEARTBEAT:
            print("PACKET_HEARTBEAT")
            # sock.sendto(HeartbeatMessage, addr)
        case PacketTypes.PACKET_HANDSHAKE:
            print("PACKET_HANDSHAKE")
            # sock.sendto(HeartbeatMessage, addr)

            sock.sendto(HandshakeMessage, addr)
        case PacketTypes.PACKET_ACCEL:
            # print("PACKET_ACCEL")
            # print(f"{data[4:]}")
            vector = struct.unpack_from('!Qfffb', data, 4)
            # print(vector[0])
            accel = vector[1:4]
            sensorNo = vector[4]
            # print(f"{sensorNo}: {accel}")
            #vector = struct.unpack_from('!f', data, 9)
            # print(vector[1])
            #vector = struct.unpack_from('!f', data, 13)
            # print(vector[2])



        case PacketTypes.PACKET_RAW_CALIBRATION_DATA:
            print("PACKET_RAW_CALIBRATION_DATA")
        case PacketTypes.PACKET_CALIBRATION_FINISHED:
            print("PACKET_CALIBRATION_FINISHED")
        case PacketTypes.PACKET_CONFIG:
            print("PACKET_CONFIG")
        case PacketTypes.PACKET_PING_PONG:
            print("PACKET_PING_PONG")
        case PacketTypes.PACKET_SERIAL:
            print("PACKET_SERIAL")
        case PacketTypes.PACKET_BATTERY_LEVEL:
            # sock.sendto(HeartbeatMessage, addr)
            # print("PACKET_BATTERY_LEVEL")
            # print(f"{data[4:]}")
            vector = struct.unpack_from('!Qff', data, 4)
            # print(vector[0])
            print(f"Battery Level: {vector[1]}V {vector[2]}%")

        case PacketTypes.PACKET_TAP:
            print("PACKET_TAP")
        case PacketTypes.PACKET_ERROR:
            print("PACKET_ERROR")
        case PacketTypes.PACKET_SENSOR_INFO :
            print("PACKET_SENSOR_INFO")
            if not connected:
                heartbeat = HeartbeatTimer(.250, sendHeartbeat, [sock, addr])
                heartbeat.start()
                connected = True
            
        case PacketTypes.PACKET_ROTATION_DATA:
            # thisPacket = time.time()
            # delay = thisPacket - lastPacket
            # lastPacket = thisPacket
            # print(f"sensor packet delay: {delay}")
            # print("PACKET_ROTATION_DATA")
            # print(f"{data[4:]}")
            vector = struct.unpack_from('!Qbbffffb', data, 4)
            # print(vector)
            rotation = vector[3:7]
            sensorNo = vector[1]
            # print(f"{sensorNo}: {rotation}")
            #vector = struct.unpack_from('!f', data, 9)
            # print(vector[1])
            #vector = struct.unpack_from('!f', data, 13)
            # print(vector[2])

            # print(Quaternion(rotation))
            # ax.update_rotation(Quaternion(rotation))





        case PacketTypes.PACKET_MAGNETOMETER_ACCURACY:
            print("PACKET_MAGNETOMETER_ACCURACY")
        case PacketTypes.PACKET_SIGNAL_STRENGTH:
            print("PACKET_SIGNAL_STRENGTH")
        case PacketTypes.PACKET_TEMPERATURE:
            print("PACKET_TEMPERATURE")

        case PacketTypes.PACKET_INSPECTION:
            print("PACKET_INSPECTION")

        case PacketTypes.PACKET_RECEIVE_HEARTBEAT:
            print("PACKET_RECEIVE_HEARTBEAT")
        case PacketTypes.PACKET_RECEIVE_VIBRATE:
            print("PACKET_RECEIVE_VIBRATE")
        case PacketTypes.PACKET_RECEIVE_HANDSHAKE:
            print("PACKET_RECEIVE_HANDSHAKE")
        case PacketTypes.PACKET_RECEIVE_COMMAND:
            print("PACKET_RECEIVE_COMMAND")

        case PacketTypes.PACKET_INSPECTION_PACKETTYPE_RAW_IMU_DATA:
            print("PACKET_INSPECTION_PACKETTYPE_RAW_IMU_DATA")
        case PacketTypes.PACKET_INSPECTION_PACKETTYPE_FUSED_IMU_DATA:
            print("PACKET_INSPECTION_PACKETTYPE_FUSED_IMU_DATA")
        case PacketTypes.PACKET_INSPECTION_PACKETTYPE_CORRECTION_DATA:
            print("PACKET_INSPECTION_PACKETTYPE_CORRECTION_DATA")
        case PacketTypes.PACKET_INSPECTION_DATATYPE_INT:
            print("PACKET_INSPECTION_DATATYPE_INT")
        case PacketTypes.PACKET_INSPECTION_DATATYPE_FLOAT:
            print("PACKET_INSPECTION_DATATYPE_FLOAT")
        case _:
            print("unknown message type")

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
#sock.bind((UDP_IP, UDP_PORT))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# Enable broadcasting mode
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

sock.settimeout(0.2)
print("UDP server up and listening")


startTime = time.gmtime()
# to run GUI event loop
# plt.ion()
 
# fig = plt.figure(figsize=(4, 4))
# ax = CubeAxes(fig)
# fig.add_axes(ax)
# ax.draw_cube()
# plt.show()
# fig.canvas.draw()

try:

    sock.sendto(HandshakeMessage, ('<broadcast>', UDP_PORT))
    while True:
        try:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            parseMessage(sock, data, addr, ax)
            # fig.canvas.flush_events()
            # fig.canvas.draw()
        except TimeoutError:
            print("connection timed out...")
            connected = False;
            if heartbeat is not None:
                heartbeat.cancel()
                heartbeat = None

            # break;
            sock.sendto(HandshakeMessage, ('<broadcast>', UDP_PORT))
        except KeyboardInterrupt:
            sock.close()
            if heartbeat is not None:
                heartbeat.cancel()
                heartbeat = None

        #print("received message <%s> : %s" % addr, data)

except KeyboardInterrupt:
    print('ctrl-c pressed. Exiting...')
    sock.close()
    if heartbeat is not None:
        heartbeat.cancel()
        heartbeat = None

else:
    print('Some other error. Also exiting...')

#print(f'runtime: {time.gmtime() - startTime}s')
sock.close()
if heartbeat is not None:
    heartbeat.cancel()
    heartbeat = None

