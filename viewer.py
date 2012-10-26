#!/usr/bin/env python
data=[]
import bugfix
import sys

with bugfix.suppress_output(sys.stderr):
    import gtk

window=gtk.Window()
def main(self):
	
    treeView = gtk.TreeView()    
    window.set_default_size(400,200)
    window.set_position(gtk.WIN_POS_CENTER)
    window.connect("destroy",terminate)
    window.set_title("Viewer")
        
    store = create_model_side(self)    
    treeView = gtk.TreeView(store)
    treeView.set_rules_hint(True)
    
    create_columns_side(self,treeView)
    
    sw = gtk.ScrolledWindow()
    sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)     
    treeView.set_rules_hint(True)
    sw.add(treeView)
    
    button=gtk.Button('OK')
    button.connect('clicked',terminate)
    vbox=gtk.VBox()
    vbox.pack_start(sw)
    vbox.pack_start(button,False)
    window.add(vbox)
    window.show_all()
    
    
def update(self,x):
    
    for i in range(0,len(data)):
	    del data[-1]
    
    fname=x[0:-3]
    
    
    s=x.find('_')
    s=x[s+1:]
    f=open(fname,'r')
    lines=f.readlines()
    f.close()
    for i in lines:
      if i.find(s)==0:
	a=['','',0,'']
	a[0]=i[0:7]
	a[1]=i[7:17].strip()
	a[2]=int(float(i[17:24].strip()))
	a[3]=i[24:].strip()
	data.append(a)
	#print a,
	#print i[7:],
    

def create_model_side(self):
	
        store = gtk.ListStore( str, str, int, str)
	
	
        for a in data:
	    
            store.append([a[0], a[1], a[2],a[3]])
	
        return store
        
        
def create_columns_side(self,treeView):    
	
	
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("DATE", rendererText, text=0)
        column.set_sort_column_id(0)    
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("TYPE", rendererText, text=1)
        column.set_sort_column_id(1)    
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("COST", rendererText, text=2)
        column.set_sort_column_id(2)
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("DESCRIPTION", rendererText, text=3)
        column.set_sort_column_id(3)
        treeView.append_column(column)
        
def terminate(self):
    window.destroy()
        
#main(self)
#gtk.main()        