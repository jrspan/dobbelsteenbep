import os
import sys
cdir = os.path.dirname(__file__)
fdir = os.path.join(cdir, "iocProgramFiles")
if fdir not in sys.path:
    sys.path.append(fdir)
    print(f"[ioc_STARTER] Added directory: {fdir}")
else:
    print(f"[ioc_STARTER] Directory already exists. ({fdir})")
    
import iocV7

iocV7.start_up()