#!/bin/sh
sudo python source/setup.py install
cd /usr/share/applications
sudo chmod 755 expensemanager.desktop
cd /usr/bin
sudo chmod 755 expensemanager
cd /usr/share/pixmaps
sudo chmod 755 expensemanager.png
cd /usr/share/expensemanager/
sudo chmod 755 bugfix.py
sudo chmod 755 clean_database.py
sudo chmod 755 edit.py
sudo chmod 755 main.py
sudo chmod 755 newEntry.py
sudo chmod 755 sort_file.py
sudo chmod 755 stats.py
sudo chmod 755 update_list.py
sudo chmod 755 viewer.py

