import os
import sys
import gc
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'site-packages', 'searcher'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'site-packages'))
from torrserve import navigation

navigation.run()
gc.collect()
try: sys.modules.clear()
except: pass
