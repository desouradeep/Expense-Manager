#!/usr/bin/env python
data=[['ENTR',0],
      ['FOOD',0],
      ['MOBILE',0],
      ['OTHERS',0],
      ['TRANSPORT',0]]
      
import bugfix
import sys

with bugfix.suppress_output(sys.stderr):
    import gtk

treeView = gtk.TreeView()
def main(self,fname):
    
    
        
    #window.set_title(fname[10:]+' '+fname[5:9]+" STATS")
    update(fname)
    store = create_model(self)    
    treeView.set_model(store)
    treeView.set_rules_hint(True)
    
    create_columns(self,treeView)
    
def update(fname):
    
    for i in range(0,len(data)):
            data[i][1]=0

    try:
      if data[5][0]=='---TOTAL---':
        del data[-1]
    except IndexError:
      pass
      
    #print fname
    f=open(fname,'r')
    lines=f.readlines()
    f.close()
    
    
    for i in lines:
      for j in data:
        if j[0]==i[7:17].strip():          
          j[1]+=int(float(i[17:24].strip()))

    x=['---TOTAL---',0]
    for k in range(0,len(data)):
        #print k
        x[1]+=data[k][1]
    data.append(x)
    
    

def create_model(self):
        
        store = gtk.ListStore( str, int)
        
        
        for a in data:
            
            store.append([a[0], a[1]])
        
        return store
        
        
def create_columns(self,treeView):    
        
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("TYPE", rendererText, text=0)
        column.set_sort_column_id(0)    
        treeView.append_column(column)
        
        rendererText = gtk.CellRendererText()
        column = gtk.TreeViewColumn("COST", rendererText, text=1)
        column.set_sort_column_id(1)    
        treeView.append_column(column)
        
        
