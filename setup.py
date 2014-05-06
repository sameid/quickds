from distutils.core import setup
import py2exe, sys, os

setup(console=['quickds.py'],
      data_files=['cacert.pem'])
