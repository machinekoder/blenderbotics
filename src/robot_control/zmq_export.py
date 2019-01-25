# coding=utf-8
import os
import zmq

# ZMQ_ADDRESS = 'ipc:///tmp/blender2robot'
ZMQ_ADDRESS = 'ipc://{}'.format(os.path.expanduser('~/.blender2robot'))
# ZMQ_ADDRESS = 'tcp://127.0.0.1:12346'


def send_data(data):
    ctx = zmq.Context()
    zmq_socket = ctx.socket(zmq.PUSH)
    print(ZMQ_ADDRESS)
    zmq_socket.bind(ZMQ_ADDRESS)
    zmq_socket.send_json(data)
