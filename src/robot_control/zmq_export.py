# -*- coding: utf-8 -*-
import zmq

# ZMQ_ADDRESS = 'ipc:///tmp/blender2robot'
# ZMQ_ADDRESS = 'ipc://{}'.format(os.path.expanduser('~/.blender2robot'))
ZMQ_ADDRESS = 'tcp://127.0.0.1:123458'


def send_data(data, address=ZMQ_ADDRESS):
    ctx = zmq.Context()
    zmq_socket = ctx.socket(zmq.PUSH)
    print('sending data to {}'.format(address))
    zmq_socket.bind(address)
    zmq_socket.send_json(data)
