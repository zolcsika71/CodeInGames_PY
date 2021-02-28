# Normal library imports
# NOTE:  imports declared in imported functions need to be
#       manually added here for now...
import sys
import math
import time
# etc...


# IMPORT
from lib.functions.Util_ import *
from lib.functions.Second_ import *
from lib.functions.First_ import *
# END_IMPORT

def run():
    init_t = time.time()
    first_func()
    debug_time(f"Time:", init_t, time.time())


run()
