#!/usr/bin/python
import unittest2 as unittest

import file_helper
import archive


import os
opj = os.path.join

class TestFileHelper(unittest.TestCase):

  def testFileHelperFile(self):
    # create file:
    file_helper.create_file(opj(self.tempdir,"testfile"),"content123test")
    
    # test if it exists:
    self.assertEqual(file_helper.file_exists(opj(self.tempdir,"testfile")),True)

    # test its content:
    self.assertEqual(file_helper.file_head(opj(self.tempdir,"testfile")),"content123test")

    # test if it can be removed:
    file_helper.remove_file(opj(self.tempdir,"testfile"))
    self.assertEqual(file_helper.file_exists(opj(self.tempdir,"testfile")),False)
    
  def testFileHelperDir(self):
    # create dir:
    file_helper.create_dir(opj(self.tempdir,"testdir"))
    # test if it exists:
    self.assertEqual(file_helper.dir_exists(opj(self.tempdir,"testdir")),True)

    
  def testFileHelperDir(self):
    dir = opj(self.tempdir,"testdir")

    # create dir:
    file_helper.create_dir(dir)

    # test if it can be destroyed:
    file_helper.destroy_dir_recursive(dir)
    self.assertEqual(file_helper.dir_exists(dir),False)

  def testFileHelperDir(self):
    dir = opj(self.tempdir,"testdir")

    # create dir:
    file_helper.create_dir(dir)

    # get stat:
    stat1 =  file_helper.get_stat(dir)
    
    # stat1 could be "0755" or so
    self.assertEqual(len(stat1),4)
    self.assertEqual(stat1[0],"0")
      


  def testFileHelperDirError(self):
    # create dir at not existing location:
    try:
      exception = False
      file_helper.create_dir(opj(self.tempdir,"notexisting","testdir"))
    except:
      exception = True

    # should have raised exception (OSError)
    self.assertEqual(exception,True)

    # should not exists:
    self.assertEqual(file_helper.dir_exists(opj(self.tempdir,"testfile")),False)
    
  def setUp(self):
    #get a temp dir:
    self.tempdir = file_helper.get_random_temp_dir_name()
    file_helper.mkdir_p(self.tempdir)
  
  def tearDown(self):
    file_helper.destroy_dir_recursive(self.tempdir)
  
     
    

if __name__ == "__main__":
    unittest.main()