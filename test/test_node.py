from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import unittest
import numpy as np
from onnxtf.backend import run_node
from onnx import helper

class TestStringMethods(unittest.TestCase):
  """ Tests for ops
  """

  def _get_rnd(self, shape):
    return np.random.uniform(-1, 1, np.prod(shape)) \
                      .reshape(shape) \
                      .astype(np.float32)

  def test_relu(self):
    node_def = helper.make_node("Relu", ["X"], ["Y"])
    x = np.random.uniform(-1, 1, 1000)
    output = run_node(node_def, [x])
    np.testing.assert_almost_equal(output["Y"], np.maximum(x, 0))

  def test_pad(self):
    node_def = helper.make_node("Pad", ["X"], ["Y"],
                                mode="constant",
                                paddings=[1, 1, 1, 1],
                                value=2.0)
    x = self._get_rnd([100, 100])
    output = run_node(node_def, [x])
    np.testing.assert_almost_equal(output["Y"],
                                   np.lib.pad(x, ((1, 1), (1, 1)),
                                              'constant',
                                              constant_values=(2, 2)))

  def test_pow(self):
    node_def = helper.make_node("Pow", ["X", "Y"], ["Z"])
    x = np.random.uniform(0.5, 1, 1000)
    y = np.random.uniform(0.5, 1, 1000)
    output = run_node(node_def, [x, y])
    np.testing.assert_almost_equal(output["Z"],
                                   np.power(x, y))

  def test_run_all(self):
    dummy_inputs = [self._get_rnd([100]) for _ in range(10)]
    run_node(helper.make_node("Relu", ["X"], ["Y"]), dummy_inputs[0:1])
    run_node(helper.make_node("PRelu", ["X", "Slope"], ["Y"]), \
                                dummy_inputs[0:2])
    run_node(helper.make_node("Pad", ["X"], ["Y"],
                              mode="constant",
                              paddings=[1, 1],
                              value=1.0),
             dummy_inputs[0:1])

if __name__ == '__main__':
  unittest.main()