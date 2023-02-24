#!/usr/bin/python
import os
import unittest2 as unittest

import file_helper, archive 

opj = os.path.join

class TestArchive(unittest.TestCase):
    
  def setUp(self):
    self.keep = False # set this to true to keep a resulting temp dir after testing
    #get a temp dir:
    self.tempdir = file_helper.get_random_temp_dir_name()
    #create the temp dir:
    file_helper.create_dir(self.tempdir)

    
  
  def tearDown(self):
    if self.keep:
      print "RESULT WAS KEPT: ================================="
      print
      print "cd", self.tempdir
      print
      print
      return
    file_helper.destroy_dir_recursive(self.tempdir)
     

  def testMakeArchive(self):
    # Part A creates a single file, archives it, then deletes it
    # Part B extracts the file again from the archive and checks the content
    
    base = self.tempdir
    
    frel = "testfile"
    fabs = opj(base,"testfile")
    rar = opj(base,"testarchive1.rar")
    
    # Part A:
    file_helper.create_file(fabs,"content123test")
    
    a = archive.Archive(rar,base)
    a.add_file(frel)

    self.assertEqual(a.run(),0)
     
    self.assertEqual(file_helper.file_exists(rar),True)

    file_helper.remove_file(fabs)
    self.assertEqual(file_helper.file_exists(fabs),False)

    # Part B:
    b = archive.Archive(rar,base)
    syscode = b.extract(target_path=base)
    self.assertEqual(syscode,0)

    self.assertEqual(file_helper.file_head(fabs),"content123test")

  def testMakeArchive2Files(self):
    # Part A creates a single file, archives it, then deletes it
    # Part B extracts the file again from the archive and checks the content
    
    base = self.tempdir
    
    frel = "testfile"
    fabs = opj(base,frel)

    frel2 = "testfile2"
    fabs2 = opj(base,frel2)

    rar = opj(base,"testarchive1.rar")
    
    # Part A:
    file_helper.create_file(fabs,"content123test")
    file_helper.create_file(fabs2,"content123test2")
    
    a = archive.Archive(rar,base)
    a.add_file(frel)
    a.add_file(frel2)

    self.assertEqual(a.run(),0)
     
    self.assertEqual(file_helper.file_exists(rar),True)

    file_helper.remove_file(fabs)
    self.assertEqual(file_helper.file_exists(fabs),False)
    file_helper.remove_file(fabs2)
    self.assertEqual(file_helper.file_exists(fabs2),False)

    # Part B:
    b = archive.Archive(rar,base)
    syscode = b.extract(target_path=base)
    self.assertEqual(syscode,0)

    self.assertEqual(file_helper.file_head(fabs),"content123test")
    self.assertEqual(file_helper.file_head(fabs2),"content123test2")





  def testMakeArchiveFileInSubdir(self):
    # test archiving a file in a subdir and extracting relative

    base = self.tempdir
    rar = opj(base,"testarchive1.rar")

    # Part A:
    a = archive.Archive(rar,base)

    
    drel = opj("A","1","a") # relative path to directory
    dabs = opj(base,drel) # absolute
    frel = opj("A","1","a","testfile-1")
    fabs = opj(base,frel)

    file_helper.mkdir_p(dabs)
    file_helper.create_file(fabs,"content-1")
    self.assertEqual(file_helper.file_exists(fabs),True)

    a.add_file(frel) # must add relative paths

    # run and check if rar archive exists:
    
    self.assertEqual(a.run(),0)
    self.assertEqual(file_helper.file_exists(rar),True)

    # remove original file and check:
    file_helper.remove_file(fabs)
    self.assertEqual(file_helper.file_exists(fabs),False)
                                                                        
    # Part B:                                                     
    b = archive.Archive(rar,base)          
    syscode = b.extract(target_path=base)
    self.assertEqual(syscode,0)

    self.assertEqual(file_helper.file_exists(fabs),True)
    
    # TODO: check content:
    self.assertEqual(file_helper.file_head(fabs),"content-1")
    
  def testMakeArchiveFailSubdirs(self):
    # create an archive at not existing directory
    base=self.tempdir
    aname = opj(self.tempdir,"dir/doesnt/exist","testarchive1.rar")
    a = archive.Archive(aname,base)
    file_helper.create_file(opj(self.tempdir,"testfile")) # empty file is ok
    a.add_file(opj("testfile"))
    syscode = a.run()
    # should fail, because the target dir does not exist:
    self.assertNotEqual(syscode,0)

  def testMakeArchiveFail1(self):
    # create an archive of not existing file, this is the only file for the archive!
    base=self.tempdir
    a = archive.Archive(opj(base,"testarchive1.rar"),base)
    a.add_file("this-file-does-not-exist")
    syscode = a.run() 
    self.assertNotEqual(syscode,0)



  def testMakeArchiveSubdir1(self):
    # test archiving a subdir with a file and extracting relative
    
    base=self.tempdir
    rar=opj(base,"testarchive1.rar")
    a = archive.Archive(rar,base)

    drel_top = "A"
    drel=opj(drel_top,"1","a")
    dabs=opj(base,drel)

    frel=opj(drel,"testfile-1")
    fabs=opj(base,frel)


    file_helper.mkdir_p(dabs)
    file_helper.create_file(fabs,"content-1")

    a.add_dir(drel_top)

    self.assertEqual(a.run(),0) 
    self.assertEqual(file_helper.file_exists(rar),True)

    file_helper.remove_file(fabs)
    self.assertEqual(file_helper.file_exists(fabs),False)
                                                                        
    # test content of archive by extracting:                                                     
    b = archive.Archive(rar,base)    
    syscode = b.extract(target_path=self.tempdir)
    self.assertEqual(syscode,0)

    self.assertEqual(file_helper.file_head(fabs),"content-1")
    


  def testMakeArchive2Trees(self):
    # test archiving files in a tree and extracting relative
    # method to communcate tree: add 2 base dirs
    
    # Part A creates a single file, archives it, then deletes it
    # Part B extracts the file again from the archive and checks the content
    
    base = self.tempdir 
    
    rar = opj(base,"testarchive1.rar")



    drel_top = "A"
    drel=opj(drel_top,"1","a")
    dabs = opj(base,drel)
    frel=opj(drel_top,"1","a","testfile-1")
    fabs=opj(base,frel)
    
    drel_topB = "B"

    drel2=opj(drel_topB,"1","a")
    dabs2 = opj(base,drel2)
    frel2=opj(drel_topB,"1","a","testfile-")
    fabs2=opj(base,frel2)
    
    drel3=opj(drel_topB,"2","a")
    dabs3 = opj(base,drel3)
    frel3=opj(drel_topB,"2","a","testfile-")
    fabs3=opj(base,frel3)

    # Part A:
    
    a = archive.Archive(rar,base)

    file_helper.mkdir_p(dabs)
    file_helper.create_file(fabs,"content-1")

    a.add_dir(drel_top)

    file_helper.mkdir_p(dabs2)
    file_helper.create_file(fabs2,"content-2")

    file_helper.mkdir_p(dabs3)
    file_helper.create_file(fabs3,"content-3")

    a.add_dir(drel_topB)

    self.assertEqual(a.run(),0) 
    self.assertEqual(file_helper.file_exists(rar),True)

    file_helper.remove_file(fabs)
    file_helper.remove_file(fabs2)
    file_helper.remove_file(fabs3)

    self.assertEqual(file_helper.file_exists(fabs),False)
    self.assertEqual(file_helper.file_exists(fabs2),False)
    self.assertEqual(file_helper.file_exists(fabs3),False)
                                                                        
    # Part B:                                                     
    b = archive.Archive(rar,base)          
    syscode = b.extract(target_path=base)
    self.assertEqual(syscode,0)

    self.assertEqual(file_helper.file_head(fabs),"content-1")
    self.assertEqual(file_helper.file_head(fabs2),"content-2")
    self.assertEqual(file_helper.file_head(fabs3),"content-3")



  def testMakeArchiveTreeAndFile(self):
    # test archiving files in a tree and extracting relative
    # method to communcate tree: add 1 file and 1 base dir of a tree
    
    # Part A creates a single file, archives it, then deletes it
    # Part B extracts the file again from the archive and checks the content
    
    base = self.tempdir 
    
    rar = opj(base,"testarchive1.rar")



    drel_top = "A"
    drel=opj(drel_top,"1","a")
    dabs = opj(base,drel)
    frel=opj(drel_top,"1","a","testfile-1")
    fabs=opj(base,frel)
    
    drel_topB = "B"

    drel2=opj(drel_topB,"1","a")
    dabs2 = opj(base,drel2)
    frel2=opj(drel_topB,"1","a","testfile-")
    fabs2=opj(base,frel2)
    
    drel3=opj(drel_topB,"2","a")
    dabs3 = opj(base,drel3)
    frel3=opj(drel_topB,"2","a","testfile-")
    fabs3=opj(base,frel3)

    # Part A:
    
    a = archive.Archive(rar,base)

    file_helper.mkdir_p(dabs)
    file_helper.create_file(fabs,"content-1")

    a.add_file(frel)

    file_helper.mkdir_p(dabs2)
    file_helper.create_file(fabs2,"content-2")

    file_helper.mkdir_p(dabs3)
    file_helper.create_file(fabs3,"content-3")

    a.add_dir(drel_topB)

    self.assertEqual(a.run(),0) 
    self.assertEqual(file_helper.file_exists(rar),True)

    file_helper.remove_file(fabs)
    file_helper.remove_file(fabs2)
    file_helper.remove_file(fabs3)

    self.assertEqual(file_helper.file_exists(fabs),False)
    self.assertEqual(file_helper.file_exists(fabs2),False)
    self.assertEqual(file_helper.file_exists(fabs3),False)
                                                                        
    # Part B:                                                     
    b = archive.Archive(rar,base)          
    syscode = b.extract(target_path=base)
    self.assertEqual(syscode,0)

    self.assertEqual(file_helper.file_head(fabs),"content-1")
    self.assertEqual(file_helper.file_head(fabs2),"content-2")
    self.assertEqual(file_helper.file_head(fabs3),"content-3")

  def testExclude(self):
    # test archiving a subdir with a file and extracting relative
    
    base=self.tempdir
    rar=opj(base,"testarchive1.rar")
    a = archive.Archive(rar,base)

    drel_top = "A"
    drel=opj(drel_top,"1","a")
    dabs=opj(base,drel)
    file_helper.mkdir_p(dabs)

    frel=opj(drel,"testfile-1")
    fabs=opj(base,frel)
    file_helper.create_file(fabs,"content-2")

    frel2=opj(drel,"testfile-2")
    fabs2=opj(base,frel2)
    file_helper.create_file(fabs2,"content-2")

    a.add_dir(drel_top)
    a.exclude(frel) # exclude the first file!

    self.assertEqual(a.run(),0) 
    self.assertEqual(file_helper.file_exists(rar),True)

    file_helper.remove_file(fabs)
    self.assertEqual(file_helper.file_exists(fabs),False)

    file_helper.remove_file(fabs2)
    self.assertEqual(file_helper.file_exists(fabs2),False)
                                                                        
    # test content of archive by extracting:                                                     
    b = archive.Archive(rar,base)    
    syscode = b.extract(target_path=self.tempdir)
    self.assertEqual(syscode,0)

    # the first file was excluded, may not exist:
    self.assertEqual(file_helper.file_exists(fabs),False)
    # the second file must be there:
    self.assertEqual(file_helper.file_head(fabs2),"content-2")
    





if __name__ == "__main__":
    unittest.main()