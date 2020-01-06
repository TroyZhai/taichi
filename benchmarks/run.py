import os
import taichi as ti

class Case:
  def __init__(self, name, func):
    self.name = name
    self.func = func
    self.records = {}
    
  def __lt__(self, other):
    return self.name < other.name
  
  def __eq__(self, other):
    return self.name == other.name
  
  def pprint(self):
    print(' *', self.name)
    for arch in sorted(self.records.keys()):
      ms = self.records[arch] * 1000
      print(f'     * {str(arch):15} {ms:7.3f}ms/iter')
    
  def run(self, arch):
    ti.reset()
    ti.cfg.arch = arch
    t = self.func()
    self.records[arch] = t
    

class Suite:
  def __init__(self, filename):
    self.cases = []
    self.name = filename[:-3]
    loc = {}
    exec(f'import {self.name} as suite', {}, loc)
    suite = loc['suite']
    case_keys = list(sorted(filter(lambda x: x.startswith('benchmark_'), dir(suite))))
    self.cases = [Case(k, getattr(suite, k)) for k in case_keys]
    
  def print(self):
    print(f'suite {self.name}:')
    for b in self.cases:
      b.pprint()
      
  def run(self, arch):
    print(f'  suite {self.name}:')
    for case in sorted(self.cases):
      case.run(arch)
      

class TaichiBenchmark:
  def __init__(self):
    self.suites = []
    for f in sorted(os.listdir('.')):
      if f != 'run.py' and f.endswith('.py') and f[0] != '_':
        self.suites.append(Suite(f))
        
  def pprint(self):
    for s in self.suites:
      s.print()
      
  def run(self, arch):
    print("Running...")
    for s in self.suites:
      s.run(arch)


b = TaichiBenchmark()
b.pprint()
b.run(ti.x86_64)
b.run(ti.cuda)
b.pprint()