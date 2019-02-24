#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# file from https://github.com/Nircek/circuiter
# licensed under MIT license

# MIT License

# Copyright (c) 2018-2019 Nircek

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import math

class pos:
  def __init__(self, *a):
    if len(a) == 1:
      a = a[0]
    self.x = a[0]
    self.y = a[1]
    self.w = a[0]
    self.h = a[1]

class element:
  slots = 0
  s = pos(10, 10)
  def __str__(self):
    return 'element'
  def __init__(self, parent, p, name=None, ins=None, st='black'):
    self.addr = super().__repr__().split('0x')[1][:-1]
    self.UUID = -1
    self.updates = 0
    self.parent = parent
    self.e = pos(-1, -1)
    if name is None:
      self.name = self.__str__()
    else:
      self.name = name
    if ins is None:
      self.inputs = []
    else:
      self.inputs = ins
    for e in self.inputs:
      self.parent.get(e).outs += [self]
    self.power = False
    self.p = p
    self.st = st
    self.outs = []
  def getsize(self):
    return self.s
  def update(self, ins):
    self.power = self.calc(ins)
    self.updates += 1
    self.e = pos(self.xy())
  def onclick1(self):
    if self.st == 'black':
      self.st = 'orange'
    else:
      self.st = 'black'
  def onclick2(self):
      self.st = 'green'
  def motion(self, p):
      self.p.x = p.x - self.s.w // 2
      self.p.y = p.y - self.s.h // 2
      self.e = pos(self.xy())
  def onkey(self, ev):
    if  ev.x >= self.p.x and ev.x <= self.p.x+self.s.w \
    and ev.y >= self.p.y and ev.y <= self.p.y+self.s.h:
      print(self.UUID)
      if ev.keysym.upper() == 'D':
        self.inputs = []
      elif ev.keysym.upper() == 'I':
        self.parent.selected = self.UUID
      elif ev.keysym.upper() == 'O' and self.parent.selected is not None:
        self.inputs += [self.parent.selected]
        self.parent.get(self.parent.selected).outs += [self]
      elif ev.keysym == 'Delete':
        for e in self.outs:
          i=0
          while i < len(e.inputs):
            if e.inputs[i] == self.UUID:
              del e.inputs[i]
            else:
              i += 1
        self.parent.rm(self.UUID)
  def __repr__(self):
    return str(vars(self))
  def calc(self, ins):
    return self.power
  def render(self):
    self.parent.arc(self.p.x+self.s.w//2, self.p.y+self.s.h//2, min(self.s.w, self.s.h)//2, 0, 360, self.st)
  def xy(self):
    return (self.p.x+self.s.w//2, self.p.y+self.s.h//2)


class switch(element):
  slots = 0
  s = pos(40, 40)
  def __str__(self):
    return 'switch'
  def onclick2(self):
    self.power = not self.power
  def render(self):
    st = self.st
    if st == 'black' and self.power:
      st = 'red'
    self.parent.arc(self.p.x+self.s.w//2, self.p.y+self.s.h//2, min(self.s.w, self.s.h)//2, 0, 360, st)

class light(element):
  slots = 1
  s = pos(40, 40)
  def __str__(self):
    return 'light'
  def calc(self, ins):
    return False if len(ins) < self.slots else ins[0]
  def render(self):
    st = self.st
    if st == 'black' and self.power:
      st = 'red'
    self.parent.w.create_rectangle(self.p.x, self.p.y, self.p.x+self.s.w, self.p.y+self.s.h, outline=st)
    if len(self.inputs) >= self.slots:
      pc = self.parent.getPowerColor(self.inputs[0], self.UUID)
      e = self.parent.get(self.inputs[0]).e
      self.parent.w.create_line(e.x, e.y, self.p.x+self.s.w//2, self.p.y+self.s.h//2, fill=pc)

class ANDgate(element):
  s = pos(40, 40)
  slots = -1
  def __str__(self):
    return 'ANDgate'
  def calc(self, ins):
    for e in ins:
      if not e:
        return False
    return True
  def render(self):
    self.parent.w.create_line(self.p.x, self.p.y, self.p.x+20, self.p.y, fill=self.st)
    self.parent.w.create_line(self.p.x, self.p.y, self.p.x, self.p.y+40, fill=self.st)
    self.parent.w.create_line(self.p.x, self.p.y+40, self.p.x+20, self.p.y+40, fill=self.st)
    self.parent.arc(self.p.x+20, self.p.y+20, 20, 270, 180, self.st)
    for i in range(len(self.inputs)):
      j = 40*(i+1)/(len(self.inputs)+1)
      pc = self.parent.getPowerColor(self.inputs[i], self.UUID)
      self.parent.w.create_line(self.p.x, self.p.y+j, self.p.x-10, self.p.y+j, fill=pc)
      e = self.parent.get(self.inputs[i]).e
      self.parent.w.create_line(e.x, e.y, self.p.x-10, self.p.y+j, fill=pc)
  def xy(self):
    return (self.p.x+self.s.w, self.p.y+self.s.h//2)

class ORgate(element):
  slots = -1
  s = pos(40, 40)
  def __str__(self):
    return 'ORgate'
  def calc(self, ins):
    for e in ins:
      if e:
        return True
    return False
  def render(self):
    self.parent.arc(self.p.x-20,self.p.y+20,math.sqrt(2*20**2),315,90,self.st)
    self.parent.w.create_line(self.p.x, self.p.y, self.p.x+20, self.p.y, fill=self.st)
    self.parent.w.create_line(self.p.x, self.p.y+40, self.p.x+20, self.p.y+40, fill=self.st)
    self.parent.arc(self.p.x+20,self.p.y+20,20,270,180,self.st)
    for i in range(len(self.inputs)):
      j = 40*(i+1)/(len(self.inputs)+1)
      k = math.sqrt(20**2*2-(j-20)**2)-20
      pc = self.parent.getPowerColor(self.inputs[i], self.UUID)
      self.parent.w.create_line(self.p.x+k, self.p.y+j, self.p.x-10, self.p.y+j, fill=pc)
      e = self.parent.get(self.inputs[i]).e
      self.parent.w.create_line(e.x, e.y, self.p.x-10, self.p.y+j, fill=pc)
  def xy(self):
    return (self.p.x+self.s.w, self.p.y+self.s.h//2)

class NOTgate(element):
  slots = 1
  s = pos(40, 40)
  def __str__(self):
    return 'NOTgate'
  def calc(self, ins):
    return True if len(ins) < self.slots else not ins[0]
  def render(self):
    self.parent.w.create_line(self.p.x, self.p.y, self.p.x, self.p.y+40, fill=self.st)
    self.parent.w.create_line(self.p.x, self.p.y, self.p.x+32, self.p.y+20, fill=self.st)
    self.parent.w.create_line(self.p.x, self.p.y+40, self.p.x+32, self.p.y+20, fill=self.st)
    self.parent.arc(self.p.x+36, self.p.y+20, 4, 0, 360, self.st)
    if len(self.inputs) >= self.slots:
      pc = self.parent.getPowerColor(self.inputs[0], self.UUID)
      self.parent.w.create_line(self.p.x, self.p.y+20, self.p.x-10, self.p.y+20, fill=pc)
      e = self.parent.get(self.inputs[0]).e
      self.parent.w.create_line(e.x, e.y, self.p.x-9, self.p.y+20, fill=pc)
  def xy(self):
    return (self.p.x+self.s.w, self.p.y+self.s.h//2)
