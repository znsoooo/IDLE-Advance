import os, time

target = 'idlexx.zip'

if target in os.listdir():
    tt = time.strftime('.%Y%m%d_%H%M%S')
    base, ext = os.path.splitext(target)
    os.rename(target, base + tt + ext)

