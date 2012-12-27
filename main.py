#!/usr/bin/python
import update_list
import sys
import os
import newEntry
import bugfix
import viewer
import stats
import datetime
with bugfix.suppress_output(sys.stderr):
    import gtk    

class app:
    
    def __init__(self):
        self.window=gtk.Window()
        self.window.set_default_size(600,500)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("delete_event",self.terminate)
        self.window.set_title("Expense Manager")
	
	vbox = gtk.VBox(False)
	
	hbox = gtk.HBox()
	button1 = gtk.Button("EDIT")
	#button1.connect('clicked',self.edit)
	button2 = gtk.Button("UPDATE")
	button2.connect('clicked',self.gocl)
	button3 = gtk.Button("STATS")
	
	
	#liststore for months
	liststore = gtk.ListStore(str)
	self.months=["JAN",'FEB','MAR','APR','MAY','JUNE','JULY','AUG','SEPT','OCT','NOV','DEC']
        for i in self.months:
	  liststore.append([i])
        cell = gtk.CellRendererText()
        self.combobox = gtk.ComboBox(liststore)
	self.combobox.pack_start(cell, True)
	self.combobox.add_attribute(cell, "text", 0)
	self.combobox.connect('changed',self.changed_item)
	
	
	now=datetime.datetime.now()
	self.mm=now.month-1
	self.dd=now.day
	self.yy=now.year
	#self.yy='2012'
        self.combobox.set_active(self.mm)
        a= self.combobox.get_active_text()
        self.fname='data/'+str(self.yy)+'_'+a
	button3.connect('clicked',self.stats)
	
	
	now=datetime.datetime.now()
	self.mm=now.month-1
	self.dd=now.day
	self.yy=now.year
	
	#hbox.add(button1)
	hbox.pack_start(button2,False)
	hbox.pack_start(button3,False)
	hbox.pack_start(button1,False)
	#hbox.add(button4)
	self.select_years()
	hbox.pack_start(self.combobox,False)
	hbox.pack_start(self.combobox2,False)
	vbox.pack_start(hbox, False)
	
	sw = gtk.ScrolledWindow()
	sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)        
        
        
        store = self.create_model()

        self.treeView = gtk.TreeView(store)
        #tvc=gtk.TreeViewColumn()
        self.treeView.set_rules_hint(True)
        self.treeView.connect('row-activated',self.on_activated)
        sw.add(self.treeView)
	vbox.pack_start(sw,550)
        self.create_columns(self.treeView)
        
        self.window.add(vbox)
        
        
        
        self.window.show_all()
    
    
    def select_years(self):
	#this method selects the years to be stored in the years combobox	
	liststore2 = gtk.ListStore(str)
	f=open('data/years','a')
	f.close()
	f=open('data/years','r')
	yrs=f.readlines()
	f.close()
	print 1
	x=0
	y=0
	for i in yrs:
	    #print 'i = '+i[0:-1]
	    i=i[0:-1]
	    x=x+1
	    if int(i)==self.yy:
	      y=x
	      print y
	    liststore2.append([i])
	print yrs

        cell = gtk.CellRendererText()
        self.combobox2 = gtk.ComboBox(liststore2)
        
        self.combobox2.set_active(y-1) #activating the current year if records exist
        
	self.combobox2.pack_start(cell, True)
	self.combobox2.add_attribute(cell, "text", 0)
	#print type(self.yy)
	
	self.combobox2.connect('changed',self.changed_item_years)
	#self.combobox2.set_active(2012)
	a= self.combobox2.get_active_text()
	#print type(a)
	
    def changed_item_years(self,widget):
        #activated when combobox value holding years is changed
        #creates a folder named data to store database in case data/ doesnt exist.
        script_dir = os.path.dirname(os.path.abspath(__file__))
	dest_dir = os.path.join(script_dir, 'data')	
	try:
	    os.makedirs(dest_dir)
	except OSError:
	    pass 
      
	#creates a file(if not present) and opens it and reads its contents
	self.fname='data/'+str(widget.get_active_text())+'_'+self.combobox.get_active_text()
        #print self.fname
        f=open(self.fname,'a')
        f.close()
        f=open(self.fname,'r')
        x=f.readlines()
        f.close()
        #print 1
        update_list.main(self.fname)
        
        try:
	  self.treeView.set_model(self.create_model())
	  #model=self.treeView.get_model()
        except AttributeError:
	  pass
      
      
    def changed_item(self,widget):
        #activated when combobox value holding months is changed
        #self.yy='2012'
        a= widget.get_active_text()
        
        #creates a folder named data to store database in case data/ doesnt exist.
        script_dir = os.path.dirname(os.path.abspath(__file__))
	dest_dir = os.path.join(script_dir, 'data')	
	try:
	    os.makedirs(dest_dir)
	except OSError:
	    pass 	  
	
	#creates a file(if not present) and opens it and reads its contents
	
        try:
	  #print type(self.combobox2.get_active_text())
          self.fname='data/'+self.combobox2.get_active_text()+'_'+a
          #print self.fname
	  f=open(self.fname,'a')
	  f.close()
	  f=open(self.fname,'r')
	  x=f.readlines()
	  f.close()
        #print 1
	  update_list.main(self.fname)
        except AttributeError:
	  update_list.main('data/'+str(self.yy)+'_'+self.combobox.get_active_text())
	  pass
	
        try:
	  self.treeView.set_model(self.create_model())
	  #model=self.treeView.get_model()
        except AttributeError:
	  pass
	
        

        
        
        
      
    def create_model(self):
      #updates the liststore in treeView
        store = gtk.ListStore( str, int, int, int, int, int, int)
	for a in update_list.z:
            store.append([a[0], a[1], a[2], a[3], a[4], a[5], a[6]])
	   
        return store

    def create_columns(self,treeView):
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("DATE   ", rendererText, text=0)
        column.set_sort_column_id(0)    
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn('ENTR', rendererText, text=1)
        column.set_sort_column_id(1)
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("FOOD", rendererText, text=2)
        column.set_sort_column_id(2)
        treeView.append_column(column)

        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("OTHERS", rendererText, text=3)
        column.set_sort_column_id(3)
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("MOBILE", rendererText, text=4)
        column.set_sort_column_id(4)
        treeView.append_column(column)

	
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("TRANSPORT", rendererText, text=5)
        column.set_sort_column_id(5)
        treeView.append_column(column)
        
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("TOTAL", rendererText, text=6)
        column.set_sort_column_id(6)
        treeView.append_column(column)
        
    def gocl(self,btn):
	newEntry.newEntry(self.combobox2)
	self.changed_item(self.combobox)
	self.changed_item_years(self.combobox2)
      
    def on_activated(self,widget, row, col):
      #double click on the treeView
      model=widget.get_model()
      x='data/'+str(self.combobox2.get_active_text())+'_'+ model[row][0]
      #print x
      viewer.update(self,x)
      viewer.main(self)
    
    def stats(self,widget):
      stats.main(self,self.fname)
	  
    def terminate(self,a,r):
        sys.exit(0)
app()
gtk.main()