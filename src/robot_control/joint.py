# -*- coding: utf-8 -*-
import attr


@attr.s
class Joint(object):
    position = attr.ib(default=0.0)
    velocity = attr.ib(default=0.0)
    acceleration = attr.ib(default=0.0)
    offset = attr.ib(default=0.0)
    axis = attr.ib(default=0)
    scale = attr.ib(default=1.0)

    @property
    def raw_position(self):
        return self.position - self.offset

    @raw_position.setter
    def raw_position(self, position):
        self.position = position - self.offset
