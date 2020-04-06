# -*- coding: utf-8 -*-
import pytest

from robot_control.joint import Joint


@pytest.fixture
def foo():
    return True


def test_raw_position_read_and_written_correctly():
    joint = Joint(offset=44.65)

    joint.raw_position = 10.0

    assert pytest.approx(joint.position, 54.65)
    assert pytest.approx(joint.raw_position, 10.0)
