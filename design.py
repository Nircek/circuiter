import code
from tkinter import *
import math

class pos:
  def __init__(self, *a):
    if len(a) == 1:
      a = a[0]
    if hasattr(a, 'x') and hasattr(a, 'y'):
      a = (a.x, a.y)
    self.x = a[0]
    self.y = a[1]
    self.w = a[0]
    self.h = a[1]
  def arr(self):
    return (self.x, self.y)

def dist(a,b):
  return math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)

def az(a,b):
  # SRC: https://gist.github.com/Nircek/76453baf3f734215a4e56c5479e3d964
  """It calculates azimuth from a( [dd, dd] ) to b( [dd, dd] )"""
  dx = b[0] - a[0]
  dy = b[1] - a[1]
  a = math.degrees(math.atan2(dy, dx))
  if a < 0:
    a += 360
  return a
    
class element:
  slots = 0
  s = pos(1, 1)
  def __str__(self):
    return 'element'
  def __init__(self, parent, p, name=None, ins=None, st='black'):
    self.addr = super().__repr__().split('0x')[1][:-1]
    self.UUID = -1
    self.updates = 0
    self.parent = parent
    if name is None:
      self.name = self.__str__()
    else:
      self.name = name
    self.p = p
    self.st = st
  def getsize(self):
    return self.s
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
  def onkey(self, ev):
    if  ev.x >= self.p.x and ev.x <= self.p.x+self.s.w \
    and ev.y >= self.p.y and ev.y <= self.p.y+self.s.h:
      print(self.UUID)
      if ev.keycode == 46:
        self.parent.rm(self.UUID)
  def __repr__(self):
    return str(vars(self))
  def render(self):
    self.parent.w.create_oval(self.p.x, self.p.y, self.p.x, self.p.y, width=0, fill=self.st)
    #self.parent.w.create_line(self.p.x, self.p.y, self.p.x+20, self.p.y, fill=self.st)
    #self.parent.arc(self.p.x+20, self.p.y+20, 20, 270, 180, self.st)

class line(element):
  def __str__(self):
    return 'line'
  def __init__(self, parent, p, name=None, ins=None, st='black'):
    super().__init__(parent, p, name, ins, st)
    self.parent.h = {'r1': self.r1, 'm': self.m}
    self.e = self.p
  def r1(self, ev):
    self.parent.h = None
  def m(self, ev):
    self.e = pos(ev.x, ev.y)
  def render(self):
    self.parent.w.create_line(self.p.x,self.p.y,self.e.x,self.e.y, fill=self.st)


class arc(element):
  def __str__(self):
    return 'arc'
  def __init__(self, parent, p, name=None, ins=None, st='black'):
    super().__init__(parent, p, name, ins, st)
    self.arc = [0, 360]
    self.r = 0
    self.parent.r1 = self.r1
    self.parent.m = self.m
    self.parent.h = True
  def m(self, ev):
    self.r = dist(self.p, ev)
  def r1(self, ev):
    self.parent.m = self.m_1
    self.parent.r1 = self.r1_1
    self.arc[1] = 180 - 45
    self.m_1(ev)
  def m_1(self, ev):
    self.arc[0] = 360 - az(self.p.arr(), pos(ev).arr())
    self.arc[0] = math.ceil(self.arc[0]/5)*5
  def r1_1(self, ev):
    self.parent.m = self.m_2
    self.parent.r1 = self.r1_2
    self.m_2(ev)
  def m_2(self, ev):
    self.arc[1] = 360 - az(self.p.arr(), pos(ev).arr()) - self.arc[0]
    if self.arc[1] <= 0:
      self.arc[1] += 360
    self.arc[1] = round(self.arc[1]/5)*5
    print(self.arc[1])
  def r1_2(self, ev):
    self.parent.h = False
    self.parent.m = None
    self.parent.r1 = None
  def render(self):
    self.parent.arc(self.p.x, self.p.y, self.r, self.arc[0], self.arc[1], self.st)
  
class UUIDs:
  def arc(self,x,y,r,s,e, outline='black'):
    if e >= 360:
      self.w.create_arc(x-r,y-r,x+r,y+r,start=0,extent=180,style=ARC,outline=outline)
      self.w.create_arc(x-r,y-r,x+r,y+r,start=180,extent=180,style=ARC,outline=outline)
    else:
      self.w.create_arc(x-r,y-r,x+r,y+r,start=s,extent=e,style=ARC, outline=outline)
  def __init__(self, WIDTH=1280, HEIGHT=720):
    self.UUIDS = []
    self.UUIDi = -1
    self.tk = Tk()
    self.w = Canvas(self.tk, width=WIDTH, height=HEIGHT)
    self.w.bind('<Button 1>',         self.hc1)
    self.w.bind('<ButtonRelease-1>',  self.hr1)
    self.w.bind('<B1-Motion>',        self.hm1)
    self.w.bind('<Button 3>',         self.hc2)
    self.w.bind('<ButtonRelease-3>',  self.hr2)
    self.w.bind('<B3-Motion>',        self.hm2)
    self.w.bind('<Motion>',           self.hm)
    self.w.bind('<KeyPress>',         self.onkey)
    self.w.pack()
    self.w.focus_set()
    self.in_motion = None
    self.click_moved = False
    self.rounding = True
    self.h = None
    self.hs = {'c1':self.onclick1, 'm1':self.motion1, 'r1':self.onrel1,
    'c2':self.onclick2, 'm2':self.motion2, 'r2':self.onrel2, 'm': self.motion}
    self.c1 = None
    self.m1 = None
    self.r1 = None
    self.c2 = None
    self.m2 = None
    self.r2 = None
    self.m = None
  def hc1(self, ev):
    self.hh('c1', ev)
  def hr1(self, ev):
    self.hh('r1', ev)
  def hm1(self, ev):
    self.hh('m1', ev)
  def hc2(self, ev):
    self.hh('c2', ev)
  def hr2(self, ev):
    self.hh('r2', ev)
  def hm2(self, ev):
    self.hh('m2', ev)
  def hm(self, ev):
    self.hh('m', ev)
  def hh(self, h, ev):
    if self.rounding:
      ev.x = round(ev.x, -1)
      ev.y = round(ev.y, -1)
    if self.h is not None:
      if h in self.h:
        print('k')
        self.h[h](ev)
    else:
      self.hs[h](ev)
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
  def render(self):
    self.w.delete('all')
    for e in self.UUIDS:
      e.render()
    self.tk.update()
  def motion(self, ev):
    pass
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
  def onrel2(self,ev):
    if not self.click_moved:
      for e in self.UUIDS:
        if  ev.x >= e.p.x and ev.x <= e.p.x+e.s.w \
        and ev.y >= e.p.y and ev.y <= e.p.y+e.s.h:
          e.onclick2()
  def motion2(self, ev):
    self.click_moved = True
  def onkey(self, ev):
    if self.rounding:
      ev.x = round(ev.x, -1)
      ev.y = round(ev.y, -1)
    print(ev)
    if ev.keycode > 111 and ev.keycode < 111+13:
      gates = [None, element, line, arc]
      b = gates[ev.keycode-111]
      self.new(b, pos(ev.x-b.s.w//2, ev.y-b.s.h//2))
    if ev.keycode == 220:
      code.InteractiveConsole(vars()).interact()
    if ev.state == 0x40001:
      self.UUIDS = []
      self.UUIDi = 0
    for e in self.UUIDS:
      e.onkey(ev)

UUIDS = UUIDs()
s = 70
in1 = UUIDS.new(element,pos(s,s))
while 1:
  UUIDS.render()
code.InteractiveConsole(vars()).interact()
