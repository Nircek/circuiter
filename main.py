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

import code
import tkinter as tk
from time import time
import elements as el

class UUIDs:
  def getPowerColor(self, s, d):
    if self.get(s).power:
      return 'red'
    return 'black'
  def arc(self,x,y,r,s,e, outline='black'):
    if e >= 360:
      self.w.create_arc(x-r,y-r,x+r,y+r,start=0,extent=180,style='arc',outline=outline)
      self.w.create_arc(x-r,y-r,x+r,y+r,start=180,extent=180,style='arc',outline=outline)
    else:
      self.w.create_arc(x-r,y-r,x+r,y+r,start=s,extent=e,style='arc', outline=outline)
  def __init__(self, WIDTH=1280, HEIGHT=720):
    self.UUIDS = []
    self.UUIDi = -1
    self.tk = tk.Tk()
    self.w = tk.Canvas(self.tk, width=WIDTH, height=HEIGHT)
    self.w.bind('<Button 1>',self.onclick1)
    self.w.bind('<ButtonRelease-1>', self.onrel1)
    self.w.bind('<B1-Motion>', self.motion1)
    self.w.bind('<Button 3>',self.onclick2)
    self.w.bind('<ButtonRelease-3>', self.onrel2)
    self.w.bind('<B3-Motion>', self.motion2)
    self.w.bind('<KeyPress>',self.onkey)
    self.w.pack()
    self.w.focus_set()
    self.in_motion = None
    self.click_moved = False
    self.selected = None
    self.rmc = el.pos(-1,-1)
  def get(self, x):
    for e in self.UUIDS:
      if e.UUID == x:
        return e
    return None
  def rm(self, x):
    i = 0
    while i < len(self.UUIDS):
      if self.UUIDS[i].UUID == x:
        del self.UUIDS[i]
      else:
        i += 1
  def new(self, c, p, ins=None):
    e = c(self, p, ins=ins)
    self.UUIDi += 1
    while self.get(self.UUIDi) is not None:
      self.UUIDi += 1
    e.UUID = int(self.UUIDi)
    self.UUIDS += [e]
    return self.UUIDi
  def add(self, x=None): # deprecated because x must have parent
    if x is None:
      x = element()
    x.parent = self
    self.UUIDi += 1
    while self.get(self.UUIDi) is not None:
      self.UUIDi += 1
    x.UUID = int(self.UUIDi)
    self.UUIDS += [x]
    return self.UUIDi
  def update(self, inf=False, x=None):
    if x is None:
      tt = False
      for i in range(len(self.UUIDS)):
        tt = False
        for e in self.UUIDS:
          t = self.get(e.UUID).power
          self.update(x=e.UUID)
          if self.get(e.UUID).power != t:
            tt = True
        if not (tt and inf):
          break
      if tt and inf:
        print('inf')
    else:
      s = self.get(x)
      i = []
      for j in s.inputs:
        i += [self.get(j).power]
      s.update(i)
  def render(self):
    self.w.delete('all')
    for e in self.UUIDS:
      e.render()
    if self.selected is not None and self.rmc.x != -1:
      t = self.get(self.selected)
      self.w.create_line(t.e.x, t.e.y, self.rmc.x, self.rmc.y)
    self.tk.update()
  def onclick1(self, ev):
    self.click_moved = False
    self.in_motion = None
    for e in self.UUIDS:
      if  ev.x >= e.p.x and ev.x <= e.p.x+e.s.w \
      and ev.y >= e.p.y and ev.y <= e.p.y+e.s.h:
        self.in_motion = e.UUID
  def onrel1(self,ev):
    if not self.click_moved:
      for e in self.UUIDS:
        if  ev.x >= e.p.x and ev.x <= e.p.x+e.s.w \
        and ev.y >= e.p.y and ev.y <= e.p.y+e.s.h:
          e.onclick1()
  def motion1(self, ev):
    self.click_moved = True
    if self.in_motion is not None:
      self.get(self.in_motion).motion(ev)
  def onclick2(self, ev):
    self.click_moved = False
    self.selected = None
    for e in self.UUIDS:
      if  ev.x >= e.p.x and ev.x <= e.p.x+e.s.w \
      and ev.y >= e.p.y and ev.y <= e.p.y+e.s.h:
        self.selected = e.UUID
  def onrel2(self,ev):
    if not self.click_moved:
      for e in self.UUIDS:
        if  ev.x >= e.p.x and ev.x <= e.p.x+e.s.w \
        and ev.y >= e.p.y and ev.y <= e.p.y+e.s.h:
          e.onclick2()
    elif self.selected is not None:
      for e in self.UUIDS:
        if  ev.x >= e.p.x and ev.x <= e.p.x+e.s.w \
        and ev.y >= e.p.y and ev.y <= e.p.y+e.s.h:
          e.inputs += [self.selected]
          self.get(self.selected).outs += [e]
    self.rmc = el.pos(-1,-1)
  def motion2(self, ev):
    self.click_moved = True
    self.rmc.x = ev.x
    self.rmc.y = ev.y
  def onkey(self, ev):
    print(ev)
    if len(ev.keysym)>1 and ev.keysym[:1] == 'F':
      nr = int(ev.keysym[1:])-1
      gates = [el.switch, el.light, el.NOTgate, el.ORgate, el.ANDgate]
      b = gates[nr]
      self.new(b, el.pos(ev.x-b.s.w//2, ev.y-b.s.h//2))
    if ev.keysym == 'backslash':
      code.InteractiveConsole(vars()).interact()
    if (ev.state&1)!=0 and ev.keysym == 'Delete':
      self.UUIDS = []
      self.UUIDi = 0
    for e in self.UUIDS:
      e.onkey(ev)

UUIDS = UUIDs()
s = 70
in1  = UUIDS.new(el.switch,  el.pos(s,s))
in2  = UUIDS.new(el.switch,  el.pos(s,2*s))
not1 = UUIDS.new(el.NOTgate, el.pos(2*s,s),      [in1])
not2 = UUIDS.new(el.NOTgate, el.pos(2*s,2*s),    [in2])
orc1 = UUIDS.new(el.ORgate,  el.pos(3*s,1.5*s),  [not1, not2])
or1  = UUIDS.new(el.ORgate,  el.pos(4*s,s),      [not1, orc1])
or2  = UUIDS.new(el.ORgate,  el.pos(4*s,2*s),    [orc1, not2])
no1  = UUIDS.new(el.NOTgate, el.pos(5*s,s),      [or1])
no2  = UUIDS.new(el.NOTgate, el.pos(5*s,2*s),    [or2])
orc2 = UUIDS.new(el.ORgate,  el.pos(6*s,1.5*s),  [no1, no2])
out  = UUIDS.new(el.light,   el.pos(7*s, 1.5*s), [orc2])
try:
  while 1:
    UUIDS.update()
    t = time()
    while t+0.2 > time():
      UUIDS.render()
except tk.TclError:
  # window exit
  pass
# code.InteractiveConsole(vars()).interact()
