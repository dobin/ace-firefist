import os

def destroy_dir_recursive(dir):
  import shutil
  shutil.rmtree(dir)

def create_file(fullpath,content=""):
  f = open(fullpath,"w")
  f.write(content)
  f.close()    

def remove_file(fullpath):
  os.remove(fullpath)


def dir_exists(path):
  return os.path.isdir(path) 

def file_exists(fullpath):
  ex = os.path.isfile(fullpath)
  return ex 


def file_head(fullpath,size=5000):
  if not file_exists(fullpath):
    return ""
  f = open(fullpath,"r")
  res = f.read(size)
  f.close()
  return res

def create_dir(path):
  res = os.mkdir(path)
  return res 


#def create_dir(path,chmod=None):
#  res = os.mkdir(path)
#  if res != 0:
#    return res
#  if chmod is not None:
#    res = os.chmod(path, chmod)
#    # did not work out, all files were creatd as 755 no matter 
#  return res 

def get_stat(path):
  import string
  digs = string.digits + string.lowercase
  
  def int2base(i, base):
    if i < 0: sign = -1
    elif i==0: return '0'
    else: sign = 1
    i *= sign
    digits = []
    while i:
      digits.append(digs[i % base])
      i /= base
    if sign < 0:
      digits.append('-')
    digits.reverse()
    return "".join(digits)
  
  def int2base8(i):
    return int2base(i,8)

  import stat
  st = os.stat(path)[stat.ST_MODE]
  stat_int = stat.S_IMODE(st)
  stat_oct_s = "0" + int2base8(stat_int)
  return stat_oct_s
   


def mkdir_p(path):
  """
  Creates the directory (if it not exists),
  Also creates parent directories, if necessary-
  Does nothing if the directory already exists.
  """
  import os
  if dir_exists(path):
    return
  os.makedirs(path)



def get_random_temp_dir_name(basedir="/tmp"):
  """
  Creates a directory path with a unique random name as a subdirectory of
  the given directory.
  The directory name is derived from 
   - the current time
   - the process id and 
   - some random numbers
  """
  import time, os, random
  return "%s/%s-%s-%s" % (basedir,time.time(),os.getpid(),random.randrange(1000000,10000000)) 



        