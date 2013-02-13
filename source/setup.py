#!/usr/bin/env python
from distutils.core import setup

setup(name='Expense-Manager',
      version='1.0',
      author='Souradeep De',
      platforms=['Linux'],
      author_email='souradeep.2011@gmail.com',
      url='http://github.com/desouradeep/Expense-Manager',
      license = 'http://www.gnu.org/copyleft/gpl.html',
      data_files=[('/usr/share/applications',['source/expensemanager.desktop']),
	('/usr/bin',['source/expensemanager']),
	('/usr/share/pixmaps',['source/icons/expensemanager.png']),
	('/usr/share/expensemanager',['source/bugfix.py','source/clean_database.py','source/edit.py','source/main.py','source/newEntry.py','source/stats.py','source/sort_file.py','source/update_list.py','source/viewer.py'])]
      
     )