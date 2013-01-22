#!/usr/bin/env python
from distutils.core import setup

setup(name='Expense-Manager',
      version='1.0',
      author='Souradeep De',
      platforms=['Linux'],
      author_email='souradeep.2011@gmail.com',
      url='http://github.com/desouradeep/Expense-Manager',
      license = 'http://www.gnu.org/copyleft/gpl.html',
      data_files=[('/usr/share/applications',['expense-manager.desktop']),
	('/usr/bin',['expensemanager']),
	('/usr/share/pixmaps',['icons/expense-manager.png']),
	('/usr/share/expense-manager',['bugfix.py','clean_database.py','edit.py','main.py','newEntry.py','stats.py','sort_file.py','update_list.py','viewer.py'])]
      
     )