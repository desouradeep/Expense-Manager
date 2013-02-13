#!/usr/bin/env python
data=[]
import bugfix
import sys
import getpass

with bugfix.suppress_output(sys.stderr):
    import gtk

treeView = gtk.TreeView()    
data_location='/home/'+getpass.getuser()+'/.expensemanager/data/'
def main(self):
        
    
       
    store = create_model(self)    
    treeView.set_model(store)
    treeView.set_rules_hint(True)    
    create_columns(self,treeView)
    
    treeView.set_rules_hint(True)
    
def update(self,x):
    
    for i in range(0,len(data)):
            del data[-1]
    #print 'x: ',x
    fname=x[0:-3]
    ##print x
    #print fname
    #print fname
    
    s=x.find('_')
    s=x[s+1:]
    #print s
    try:
      f=open(fname,'r')
      lines=f.readlines()
      #print lines
      f.close()
      #print lines
      #print s,
      fname=fname[len(fname)-15+fname[-15:-1].find('data'):]
          
      for i in lines:
        if i.find(s)==0:
          a=['','','',0,'']
          a[0]=i[0:7]
          a[1]=fname[5:9]
          #print a[1]
          a[2]=i[7:17].strip()
          a[3]=int(float(i[17:24].strip()))
          a[4]=i[24:].strip()
          data.append(a)
          #print a
          #print a,
          #print i[7:],
    except IOError:
      pass
    #print data

def create_model(self):
        
        store = gtk.ListStore( str, str ,str, int, str)
        #print data
        #print data
        for a in data:
            #print a
            store.append([a[0], a[1], a[2], a[3], a[4]])
        
        return store
        
        
def create_columns(self,treeView):           
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("DATE", rendererText, text=0)
        column.set_sort_column_id(0)    
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("YEAR", rendererText, text=1)
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
        

        
#main(self)
#gtk.main()        