#!/usr/bin/env python
import unittest
import pyIbex
from pyIbex import *
import sys
import math
import ctypes

class myCtc(pyIbex.Ctc):
	def __init__(self, x=0, y=0, R=2):
		pyIbex.Ctc.__init__(self, 2)
		self.f = Function('x', 'y', '(x-%f)^2+(y-%f)^2-%f'%(x,y,R**2))
		self.ctc = CtcFwdBwd(self.f, CmpOp.LEQ)

	def contract(self, box):
		tmp = IntervalVector(box)
		self.ctc.contract(tmp)
		box.assign(tmp)

class mySep(pyIbex.Sep):
	def __init__(self, x=0, y=0, R=2):
		pyIbex.Sep.__init__(self)
		self.f = Function('x', 'y', '(x-%f)^2+(y-%f)^2-%f'%(x,y,R**2))
		self.sep = SepFwdBwd(self.f, CmpOp.LEQ)

	def separate(self, xin, xout):
		tmp_in= IntervalVector(xin)
		tmp_out = IntervalVector(xout)
		self.sep.separate(tmp_in, tmp_out)
		xin.assign(tmp_in)
		xout.assign(tmp_out)
		
class SimplisticTest(unittest.TestCase):

	def test_myCtc(self):
		ctc1 = myCtc()
		ctc2 = myCtc(1,1)
		ctc = CtcUnion([ctc1, ctc2])
		x = IntervalVector(2, [-10,10])
		SIVIA(x, ctc, 1)

	def test_mySep(self):

		sep1 = mySep()
		sep2 = mySep(1,1)
		sep = SepUnion([sep1, sep2])
		x = IntervalVector(2, [-10,10])
		SIVIA(x, sep, 1)
		

if __name__ == '__main__':
	
	unittest.main()
