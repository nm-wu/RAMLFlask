import os
import sys
import shutil
from StringIO import StringIO
import time

os.system('mprof clean')
for i in range(100):

  time.sleep(1)
  # Setup
  if os.path.exists('./delegates'):
    shutil.rmtree('./delegates')
    
  if os.path.exists('./routes'):
    shutil.rmtree('./routes')
      
  if os.path.exists('./generated'):
    shutil.rmtree('./generated')
      
  oldstdout = sys.stdout
  out = StringIO()
  sys.stdout = out
    
    
  # Memory test
  os.system('mprof run --interval 0.005 python2 mem_tested.py')
    
    
  # Cleanup
  sys.stdout = oldstdout
  if os.path.exists('./delegates'):
    shutil.rmtree('./delegates')
      
  if os.path.exists('./routes'):
    shutil.rmtree('./routes')
        
  if os.path.exists('./generated'):
    shutil.rmtree('./generated')
        
        
  # Graph
  # os.system('mprof plot')
