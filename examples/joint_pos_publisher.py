# -*- coding: utf-8 -*-
import zmq

if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.connect('tcp://127.0.0.1:12349')
    socket.send_json({'data': 'hello world'})
