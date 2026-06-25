import os
import sys

# make `import igpub` work whether tests are run from the repo root or this dir
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
