import json

import zmq
from robot_control import ZMQ_ADDRESS


def consumer():
    context = zmq.Context()
    # recieve work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect(ZMQ_ADDRESS)

    while True:
        work = consumer_receiver.recv_json()
        print(work)
        print(json.dumps(work))


if __name__ == '__main__':
    consumer()
