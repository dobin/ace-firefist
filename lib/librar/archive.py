import os
import subprocess
import types
import errno


def shellcall(cmd,silent=False):
  # do a system call with shell = true
  # taken from 
  # http://stackoverflow.com/questions/699325/suppress-output-in-python-calls-to-executables
  import os
  import subprocess

  # silent will suppress stdoud and stderr, good for testing!  
  if silent:
    fnull = open(os.devnull, 'w')
    # we need shell = true to keep the cwd 
    result = subprocess.call(cmd, shell = True, stdout = fnull, stderr = fnull)
    fnull.close()
    return result
  else:
    result = subprocess.call(cmd, shell = True)
    return result


def findfile(choice):
    # Check if one of the filenames in the tuple 'choice' exists and return that filename.
    # 'choice' can either be of type String, containing a single filename
    # or also a tuple of strigs.
    # On some systems the rar b in file is in a different location.
    if isinstance(choice, str):
      #if type(choice) is types.StringType:
      if os.path.isfile(choice):
        return choice
      else:
        raise Exception("File not found: %s" % choice)

    if isinstance(choice, tuple):
      #if type(choice) is types.TupleType:
      for f in choice:
        if os.path.isfile(f):
          return f
      raise Exception("Files not found: %s" % (choice,))


def mkdir_p(path):
    # 'mkdir -p' in python.
    # create a directory and all parent directories silently.
    # from http://stackoverflow.com/a/600612/362951
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise

class Logger(object):
  """logs to syslog using the unix logger function"""

  def __init__(self,tag):
    self.tag = tag

  def log(self,message):
    #command = "logger -t %s -- %s" % (self.tag,message)
    print("%s" % (message))


class Archive(object):

  def __init__(self,archive_fullpath,base_path,rarbin = ("/usr/bin/rar","/usr/local/bin/rar", "/opt/homebrew/bin/rar")):
    self.archive_fullpath = archive_fullpath
    self.base_path = base_path
    self.rarbin = findfile(rarbin)
    self.pwd = None
    # compression level: 0: store, 1: fastest, 2: fast, 3: normal, 4: good, 5: best
    self.compression_level = 3
    # Percentage of recovery record
    self.recovery_record = None
    # Volume size if necessary <size>[k|b|f|m|M|g|G] More info in rar.txt
    self.volume_size = None
    self.exclude_base_dir = False

    self.include_files = []
    self.include_dirs = []
    self.exclude_patterns = []
    self.sys_logger = None

  def use_syslog(self,tag="LIB-RAR"):
    self.sys_logger=Logger(tag)
    
  
  def exclude(self,pattern):
    self.exclude_patterns.append(pattern)
  
  def add_file(self,fullpath):
    self.include_files.append(fullpath)
    
  def add_dir(self,fullpath):
    self.include_dirs.append(fullpath)
    
  def set_password(self, pwd):
    self.pwd = pwd
  
  def set_compression_level(self, compression_level):
    self.compression_level = compression_level

  def set_exclude_base_dir(self, exclude_base_dir):
    self.exclude_base_dir = exclude_base_dir
  
  def set_recovery_record(self, rr_percent):
    self.recovery_record = rr_percent
  
  def set_volume_size(self, volume_size):
    self.volume_size = volume_size
  
  def extract(self,target_path,silent=True):
    import os
    os.chdir(target_path)
    # e = extract to current dir, x = extract using full path
    # -r = recurse subdirectories
    # (-r could be introduced, because single added files otherwise are extrated 
    #  to the wrong place. But this should bex fixed on archiving, nit unarchiving!)
    cmd = self.rarbin + " x " + self.archive_fullpath
    return shellcall(cmd,silent=silent)
    
  def run(self,silent=True):
    # -ep1 remove base directory from paths (store only relative directory)

    import os
    os.chdir(self.base_path)

    # rar add 
    cmd = self.rarbin + " a" 
    
    # exclude certain locations
    for p in self.exclude_patterns: 
      cmd = cmd +  " -x" + p

    # the archive path and name
    cmd = cmd + " " + self.archive_fullpath 

    # directories to include
    for p in self.include_dirs: 
      cmd = cmd +  " " + p

    # files to include
    for p in self.include_files: 
      cmd = cmd +  " " + p
    
    # include password if necessary
    if self.pwd:
      pwd = " -p" + str(self.pwd)
      # do not show password in syslog:
      logpwd = " -p*****"
    else:
      pwd = ""
      logpwd = ""
    
    # compression level
    cmd = cmd + " -m" + str(self.compression_level)
  
    # split to volumes based on volume size
    if self.volume_size:
      cmd = cmd + " -v" + str(self.volume_size)
    
    # add recovery record if necessary
    if self.recovery_record:
      cmd = cmd + " -rr" + str(self.recovery_record)

    if self.exclude_base_dir:
      cmd = cmd + " -ep1"

    res = shellcall("%s%s" % (cmd,pwd),silent=silent)

    if self.sys_logger is not None:
      # hide the password with asterisks in syslog:
      self.sys_logger.log("%s%s; result: %s" % (cmd,logpwd,res))

    return res
