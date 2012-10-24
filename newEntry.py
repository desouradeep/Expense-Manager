#!/usr/bin/env python
import datetime
import b
import sys
import time
import sort_file
with b.suppress_output(sys.stderr):
    import gtk

    
class newEntry:
  def __init__(self):  
    self.ini()
    self.window=gtk.Window()
    #self.window.set_default_size(150,120)
    
    self.window.connect("destroy", self.terminate)
    self.window.set_position(gtk.WIN_POS_CENTER)
    self.window.set_title("Add New Entry")
    
    table=gtk.Table(3,2,True)
    
    
    label=gtk.Label('TYPE	   	    ')
    table.attach(label,0,1,0,1)
    label=gtk.Label('COST	 	    ')
    table.attach(label,0,1,1,2)
    label=gtk.Label('DESCRIPTION   ')
    table.attach(label,0,1,2,3)
    
    entry1=gtk.Entry()
    table.attach(entry1,1,2,1,2)
    entry2=gtk.Entry()
    table.attach(entry2,1,2,2,3)
        
    liststore = gtk.ListStore(str)
    cats=['ENTR        ','FOOD        ','OTHERS      ','MOBILE      ','TRANSPORT   ']
    for i in cats:
      liststore.append([i])
    cell = gtk.CellRendererText()
    combobox = gtk.ComboBox(liststore)
    combobox.pack_start(cell, True)
    combobox.add_attribute(cell, "text", 0)
    combobox.set_active(0)        
    combobox.connect('changed',self.item)    
    table.attach(combobox,1,2,0,1,True,True)
    
    
    table2=gtk.Table(1,3,True)
    button=gtk.Button('Done')
    button.connect("clicked", self.terminate)
    table2.attach(button,1,2,0,1)
    button=gtk.Button('Update')
    button.connect("clicked", self.verify,entry1,entry2)
    table2.attach(button,2,3,0,1)
    
    vbox=gtk.VBox()
    vbox.pack_start(table)
    vbox.pack_start(table2,False)
    
    self.hbox=gtk.HBox()
    self.cal=gtk.Calendar()
    self.cal.connect("day-selected", self.date)
    self.hbox.pack_start(vbox)
    self.hbox.pack_start(self.cal)
    
    self.window.add(self.hbox)
    self.window.show_all()
    gtk.main()
    
  def desw(self,a):    
    self.window.destroy()
    
  def des(self,a):
    
    self.w.destroy()
    
  
  def item(self,widget):
    self.cat=widget.get_active_text()
    #print self.cat
    
  def date(self,widget):
    date = self.cal.get_date()
    self.yy, self.mm, self.dd = date
    #print self.mm
    #print self.dd, "/", self.mm, "/", self.yy
    
  def verify(self, widget,entry1,entry2):
    self.e1=entry1.get_text()
    self.w=gtk.Window()
    e2=entry2.get_text()
    if self.num(self.e1) and float(self.e1)!=0:    
      months=['JAN','FEB','MAR','APR','MAY','JUNE','JULY','AUG','SEPT','OCT','NOV','DEC']
      self.e1=str(self.e1)
      l=len(self.e1)
      for i in range(l,10):
	  self.e1=self.e1+' '
      #print self.e1
      if self.dd<10:
	d='0'+str(self.dd)
      else:
	d=str(self.dd)
      ss=months[int(self.mm)]+' '+d+'\t'+(self.cat)+self.e1+str(e2)
      #print ss     
      fname='data/'+str(self.yy)+'_'+months[int(self.mm)]
      f=open(fname,'a')
      f.write(ss+'\n')
      f.close()
      #s='data/2012_OCT'
      sort_file.main(fname)
      time.sleep(0.5)
      
      
	
    else:
      
      self.w.set_position(gtk.WIN_POS_CENTER)
      self.w.set_default_size(200,100)
      label=gtk.Label('\t INVALID COST ENTRY\t ')
      self.w.set_title('ERROR!!!')
      vbox=gtk.VBox()
      vbox.pack_start(label)
      b=gtk.Button('OK')
      b.connect('clicked',self.des)
      vbox.pack_start(b,False)
      self.w.add(vbox)
      self.w.show_all()
      
  def num(self,x):
    
    try:
      y= float(x)
      return True
    except ValueError:
      return False
      
      
  def ini(self):
    now=datetime.datetime.now()
    self.yy=now.year
    self.mm=now.month-1
    self.dd=now.day
    self.cat='ENTR        '
    #self.cost_=0
    #self.desc_=''
    #print self.mm
    
  def terminate(self,a):
    #newEntry.self.window.destroy()
    try:
      self.w.destroy()
    except AttributeError:
      pass
    self.window.destroy()
    gtk.main_quit()
#newEntry()
