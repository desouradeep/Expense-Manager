#!/usr/bin/python
from matplotlib.figure import Figure
import auto
import sys
import os
import newEntry
import b
import a
import stats
import datetime
with b.suppress_output(sys.stderr):
    import gtk
    from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

class app:
    
    def __init__(self):
        
	self.window=gtk.Window()
        self.window.set_default_size(600,500)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("delete_event",self.terminate)
        self.window.set_title("Expense Manager")
	
	vbox = gtk.VBox(False)
	
	hbox = gtk.HBox()
	#button1 = gtk.Button("EDIT")
	button2 = gtk.Button("UPDATE")
	button2.connect('clicked',self.gocl)
	button3 = gtk.Button("STATS")
	
	#button4 = gtk.Button("LOG OUT")
	
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
	self.yy='2012'
        self.combobox.set_active(self.mm)
        a= self.combobox.get_active_text()
        self.fname='data/'+self.yy+'_'+a
	button3.connect('clicked',self.stats)
	
	
	now=datetime.datetime.now()
	self.mm=now.month-1
	self.dd=now.day
	self.yy=now.year
	
	#hbox.add(button1)
	hbox.pack_start(button2,False)
	hbox.pack_start(button3,False)
	#hbox.add(button4)
	hbox.pack_start(self.combobox,False)
	vbox.pack_start(hbox, False)
	
	sw = gtk.ScrolledWindow()
	sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)        
        
        
        store = self.create_model()

        self.treeView = gtk.TreeView(store)
        tvc=gtk.TreeViewColumn()
        tvc.set_resizable(True)
        self.treeView.set_rules_hint(True)
        self.treeView.connect('row-activated',self.on_activated)
        sw.add(self.treeView)
	vbox.pack_start(sw,550)
        self.create_columns(self.treeView)
        
        self.window.add(vbox)
        
        
        
        self.window.show_all()
    
    
	
    def changed_item(self,widget):
      
        self.yy='2012'
        a= widget.get_active_text()
        script_dir = os.path.dirname(os.path.abspath(__file__))
	dest_dir = os.path.join(script_dir, 'data')
	try:
	    os.makedirs(dest_dir)
	except OSError:
	    pass 
        self.fname='data/'+self.yy+'_'+a
        #print self.fname
        f=open(self.fname,'a')
        f.close()
        f=open(self.fname,'r')
        x=f.readlines()
        f.close()
        #print 1
        auto.main(self.fname)
        
        try:
	  self.treeView.set_model(self.create_model())
	  #model=self.treeView.get_model()
        except AttributeError:
	  print ''
	
        

        
        
        
      
    def create_model(self):
        store = gtk.ListStore( str, int, int, int, int, int, int)
	for a in auto.z:
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
	newEntry.newEntry()
	self.changed_item(self.combobox)
      
    def on_activated(self,widget, row, col):
      model=widget.get_model()
      x='data/2012_'+ model[row][0]
      #print x
      a.update(self,x)
      a.main(self)
    
    def stats(self,widget):
      stats.main(self,self.fname)
	  
    def terminate(self,a,r):
        sys.exit(0)
app()
gtk.main()