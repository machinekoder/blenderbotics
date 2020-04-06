# -*- coding: utf-8 -*-
import json

import zmq

ZMQ_RECV_ADDRESS = 'tcp://127.0.0.1:12348'


def consumer():
    context = zmq.Context()
    # receive work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.bind(ZMQ_RECV_ADDRESS)

    while True:
        work = consumer_receiver.recv_json()
        print(json.dumps(work))


if __name__ == '__main__':
    consumer()
