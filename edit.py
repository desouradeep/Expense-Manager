#!usr/bin/python
import bugfix
import gobject
import sys
with bugfix.suppress_output(sys.stderr):
    import gtk    
data=[]
class edit:
  def __init__(self,fname):
    self.checked=[]
    self.fname=fname
    self.update()
    #print data
    self.window=gtk.Window()
    self.window.set_default_size(400,400)
    self.window.set_position(gtk.WIN_POS_CENTER)
    self.window.connect("destroy",self.terminate)
    self.window.set_title(self.fname[5:9]+' '+self.fname[10:]+' RECORDS')
    
   
    button2=gtk.Button(stock=gtk.STOCK_DELETE)
    button2.connect('clicked', self.confirm_delete)
    
    hbox=gtk.HBox()
    hbox.pack_start(button2,False,False)
    
    store = self.create_model_side()    
    treeView = gtk.TreeView(store)
    treeView.set_rules_hint(True)
    
    self.create_columns_side(treeView)
    
    sw = gtk.ScrolledWindow()
    sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)     
    treeView.set_rules_hint(True)
    sw.add(treeView)
    
    vbox=gtk.VBox()
    vbox.pack_start(hbox,False)
    vbox.pack_start(sw)
    
    hbox2=gtk.HBox()
    button3=gtk.Button('APPLY',gtk.STOCK_OK)
    button3.connect('clicked',self.terminate)
    hbox2.pack_start(button3)
    
    vbox.pack_start(hbox2,False)
    self.window.add(vbox)
    
    
    
    self.window.show_all() 
    gtk.main()
    
  def update(self):
    
    for i in range(0,len(data)):
	    del data[-1]
    
        
    f=open(self.fname,'r')
    lines=f.readlines()
    f.close()
    for i in lines:
      
	a=['','',0,'']
	a[0]=i[0:7]
	a[1]=i[7:17].strip()
	a[2]=int(float(i[17:24].strip()))
	a[3]=i[24:].strip()
	data.append(a)
	#print a,
	
  def create_model_side(self):
	
        self.store = gtk.ListStore(gobject.TYPE_BOOLEAN,str, str, int, str)	
        for a in data:	    
            self.store.append([False, a[0],a[1], a[2], a[3]])
	
        return self.store
        
        
  def create_columns_side(self,treeView):    
	
	cell = gtk.CellRendererToggle()
	column = gtk.TreeViewColumn('', cell, active=0)
	#column.set_clickable(True)
	cell.connect ("toggled", self.toggled_item) 
	column.set_sort_column_id(0)    
	treeView.append_column(column)
	
	
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("DATE", rendererText, text=1)
        column.set_sort_column_id(1)    
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("TYPE", rendererText, text=2)
        column.set_sort_column_id(2)    
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("COST", rendererText, text=3)
        column.set_sort_column_id(3)
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("DESCRIPTION", rendererText, text=4)
        column.set_sort_column_id(4)
        treeView.append_column(column)    
#def change(self):
  def toggled_item(self,data, row):
	if self.store[row][0]:
	  self.store[row][0]=False  
	  del self.checked[(self.checked.index(int(row)))]

	else:
	  self.store[row][0]=True
	  if self.checked.count(int(row))==0:
	    self.checked.append(int(row))
        #print self.checked,'1'
        
  def delete(self,widget):
	self.checked.sort()
	#print self.checked,'2'
	f=open(self.fname,'r')
	records=f.readlines()
	f.close()
	for i in range(0,len(self.checked)):
	    #print self.checked,'3'
	    del self.store[self.checked[i]]
	    
	    
	    del records[self.checked[i]]
	    #print records
	    rec=''
	    for i in records:
	      rec=rec+i
	    #print rec
	    f=open(self.fname,'w')
	    f.write(rec)
	    f.close()
	    
	    for y in range(0,len(self.checked)):
	      self.checked[y]=self.checked[y]-1
	    
	self.checked=[]
	self.des(records)
	
  def des(self,a):
    self.window2.destroy()
    
      
  def confirm_delete(self,widget):
   if len(self.checked) > 0:
    self.window2=gtk.Window()
    label=gtk.Label('\n        Are you sure you want to delete these records?        \n')
    button_yes=gtk.Button('YES',stock=gtk.STOCK_YES)
    button_yes.connect('clicked',self.delete)
    button_no=gtk.Button('NO',stock=gtk.STOCK_NO)
    button_no.connect('clicked',self.des)
    
    hbox=gtk.HBox()
    hbox.pack_end(button_no,False)
    hbox.pack_end(button_yes,False)
    vbox=gtk.VBox()
    vbox.pack_start(label,False)
    vbox.pack_start(hbox,False)
    
    #self.window2.set_default_size(300,70)
    self.window2.set_position(gtk.WIN_POS_CENTER)
    #self.window2.connect("destroy",self.window2.destroy)
    self.window2.set_title('WARNING!!!')
    self.window2.add(vbox)
    self.window2.show_all()
    
  def terminate(self,w):
    try:
      self.des(w)
    except AttributeError:
      pass
    self.window.destroy()    
    gtk.main_quit()
    
#edit()    

    