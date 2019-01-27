# -*- coding: utf-8 -*-
import zmq
import bpy

# ZMQ_ADDRESS = 'ipc:///tmp/blender2robot'
# ZMQ_ADDRESS = 'ipc://{}'.format(os.path.expanduser('~/.blender2robot'))
ZMQ_SEND_ADDRESS = 'tcp://127.0.0.1:12348'
ZMQ_RECV_ADDRESS = 'tcp://127.0.0.1:12349'

zmq_interface = None


class ZmqInterface(object):
    def __init__(self, send_address=ZMQ_SEND_ADDRESS, recv_address=ZMQ_RECV_ADDRESS):
        self._context = zmq.Context()
        self._send_socket = self._context.socket(zmq.PUSH)
        self._recv_socket = self._context.socket(zmq.PULL)
        self._send_address = send_address
        self._recv_address = recv_address

    def start(self):
        self._send_socket.bind(self._send_address)
        self._recv_socket.bind(self._recv_address)

    def stop(self):
        self._send_socket.close()
        self._recv_socket.close()

    def send_data(self, data):
        print('sending data to {}'.format(self._send_address))
        try:
            self._send_socket.send_json(data, zmq.NOBLOCK)
        except zmq.ZMQError:
            print('sending failed')

    def _poll_receiver_socket(self):
        try:
            while self._recv_socket.poll(0) == zmq.POLLIN:
                data = self._recv_socket.recv_json()
                self._process_message(data)
        except zmq.ZMQError:
            print('socket closed')
            return None  # socket closed

        return 0.1

    def _process_message(self, data):
        print('received message {}:'.format(data))


def send_data(data):
    global zmq_interface
    zmq_interface.send_data(data)


def register():
    global zmq_interface
    zmq_interface = ZmqInterface()
    zmq_interface.start()
    bpy.app.timers.register(zmq_interface._poll_receiver_socket)


def unregister():
    global zmq_interface
    if zmq_interface:
        try:
            bpy.app.timers.unregister(zmq_interface._poll_receiver_socket)
        except ValueError:
            pass
        zmq_interface.stop()
        del zmq_interface
