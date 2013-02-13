#!/usr/bin/python
import update_list
import sys
import os
import clean_database
import getpass
import newEntry
import bugfix
import viewer
import stats
import datetime
import edit
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas

with bugfix.suppress_output(sys.stderr):
    import gtk    

class app:
    data_location=''
    def __init__(self):
        
        app.data_location='/home/'+getpass.getuser()+'/.expensemanager/data/'
        dest_dir = os.path.join(app.data_location[0:-5],'data/')
        #print dest_dir
        try:
          f=open(app.data_location+'years','r')
          f.readlines()
          f.close()
        except :
          #script_dir = os.path.dirname(os.path.abspath(__file__))
          #dest_dir = os.path.join(app.data_location)        
          #print type(dest_dir), dest_dir
          #print 1
          try:
	      #print 2
              os.makedirs(dest_dir)
          except OSError:
              pass 
        
        
        self.window=gtk.Window()
        self.window.set_default_size(1220,658)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("delete_event",self.terminate)
        self.window.set_title("Expense Manager")
        
        
        vbox = gtk.VBox(False)
        
        hbox = gtk.HBox()
        settings=(gtk.Button()).get_settings()
        settings.set_property("gtk-button-images",True)
        button1 = gtk.Button(stock=gtk.STOCK_EDIT)


        button1.connect('clicked',self.edit)
        
        button2 = gtk.Button(stock=gtk.STOCK_ADD)
        button2.connect('clicked',self.gocl)
        
        
        
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
        #dest_dir = os.path.join(/home/+get,getpass.getuser() 'data')        
        self.fname=app.data_location+str(self.yy)+'_'+a

        
        
        
        
        try:
          f=open(app.data_location+'years','r')
          f.close()
        except :
          f=open(app.data_location+'years','w')
          f.write(str(self.yy)+'\n')
          f.close()
          
        
        #hbox.add(button1)
        hbox.pack_start(button2,False)
        hbox.pack_start(button1,False)
        #hbox.add(button4)
        self.select_years()
        hbox.pack_end(self.combobox2,False)
        hbox.pack_end(self.combobox,False)
        button5=gtk.Button(stock=gtk.STOCK_ABOUT)
        button5.connect('clicked',self.about)
        #hbox.pack_end(buttmon5,False)
        vbox.pack_start(hbox, False)        #hbox contains the add/stats/edit etc buttons/comboboxes
        hbox2=gtk.HBox()
        hbox2.pack_end(button5,False)         #button5 is the about button
        label_user=gtk.Label('    Welcome,    '+getpass.getuser().title()+'.')
        hbox2.pack_start(label_user,False)
        vbox.pack_end(hbox2,False)        #hbox2 holds only the about button
        
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)        
        
        
        store = self.create_model()

        self.treeView = gtk.TreeView(store)
        #tvc=gtk.TreeViewColumn()
        self.treeView.set_rules_hint(True)
        self.treeView.connect('cursor-changed',self.on_activated)
        sw.add(self.treeView)        
        
        
        pane=gtk.HPaned()
        pane.pack1(sw)#,resize=True, shrink=True)
        
        #self.sw_graphs=gtk.ScrolledWindow()
        #self.sw_graphs.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        #self.sw_graphs.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)     
        
        
        self.f = plt.figure(dpi=75,facecolor='w')
        #self.f.patch.set_alpha(0.95)
        self.f.subplots_adjust(left = 0.08,bottom=0.1,top = 0.9,right=0.95,wspace=0.25,hspace=0.25)
        self.canvas = FigureCanvas(self.f)
        
        self.line1=[]
        self.line1b=[]
        self.line2=[]
        
        self.graphs(1)
        self.graphs(2)
        
        
        #self.sw_graphs.add_with_viewport(self.canvas)
        
        frame=gtk.Frame()
        frame.add(self.canvas)
        
        pane_rightPane=gtk.VPaned()
        pane_stats_viewer=gtk.HPaned()

        
        
        
        viewer_sw = gtk.ScrolledWindow()
        viewer_sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        viewer_sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)     
        viewer_sw.add(viewer.treeView)
        
        x=app.data_location+str(self.yy)+'_'+ str(self.months[self.mm])+' '+str(self.dd)
        #print x
        viewer.update(self,x)
        viewer.main(self)
        
        stats_sw = gtk.ScrolledWindow()
        
        stats_sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        stats_sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)   
        stats.main(self,self.fname)
        stats_sw.add(stats.treeView)
        
        
        pane_stats_viewer.add1(stats_sw)
        pane_stats_viewer.set_position(182)
        pane_stats_viewer.add2(viewer_sw)
        
        pane_rightPane.add1(frame)
        pane_rightPane.set_position(390)
        pane_rightPane.add2(pane_stats_viewer)
        
        
        pane.pack2(pane_rightPane,resize=True, shrink=False)
        pane.set_position(590)
        #pane.compute_position(1120, True, False)
        #pane.queue_resize()
        vbox.pack_start(pane)        
        
        
        
        self.create_columns(self.treeView)
        
        self.window.add(vbox)
        
        self.window.show_all()
    
    
    def graphs(self,option):        
        # when option==1, the first graph, self.a is redrawn
        # when option==2, the second graph, self.c is redrawn
      #self.f.text(0.5,0.92,'',fontsize=14)
      #self.f.text(0.5,0.92,self.combobox.get_active_text()+' '+self.combobox2.get_active_text(),fontsize=14,horizontalalignment='center')
      
      #print self.get_suptitle()
      matplotlib.rc('xtick', labelsize=11) 
      matplotlib.rc('ytick', labelsize=11) 
      try:
        if option==1:
          self.a = self.f.add_subplot(221)
          self.a.patch.set_color('black')
          self.a.patch.set_alpha(0.05)
          #print self.a.get_yticks()
          self.a.yaxis.grid('True')
          #print self.combobox.get_active_text()
          self.a.set_xlabel(self.combobox.get_active_text()+' '+self.combobox2.get_active_text(),fontsize=12)
          #print self.a.get_xlabel()
          self.a.set_ylabel('Daily Expense',fontsize=12)
          model=self.treeView.get_model()
          total_list=[0]
          counter=0 
          for i in model:
            for j in i:
              counter+=1
              if counter%7==0:
                total_list.append(j)
              #print j, type(j),
            #print '\n' 
          #print range(len(total_list))
          #print total_list
          if max(total_list)==0:
            M=1
          else:
            M=max(total_list)+0.1*max(total_list)
          self.a.set_ylim(0,M)
          self.a.set_xlim(1,len(total_list)-1)
          days=[]
          for i in range(len(total_list)):
            if i%2!=0:
              days.append(i)
          self.a.set_xticks(days)
          self.a.set_xticklabels(days,fontsize=9)
          
          #print total_list, len(total_list)        
          #total_list.append(100)
          while len(self.line1)!=0:
            l=self.line1.pop(0)
            l.remove()
          total_list.append(0)
          #self.a.set_antialiased(False)
          #print total_list
          self.line1=self.a.fill(total_list,'blue',alpha=0.6)
          self.canvas.draw()
          
        
          #print line
          
          
          self.b=self.f.add_subplot(222)
          self.b.patch.set_color('black')
          self.b.patch.set_alpha(0.05)
          self.b.yaxis.grid('True')
          self.b.set_xlabel('Categories',fontsize=12)
          self.b.set_ylabel('Category Expense',fontsize=12)
          total_list=[0]
          counter=0
          #print 1
          stats.update(self.fname)
          counter=0
          cat=[]
          for i in stats.create_model(self):
            for j in i:
              counter+=1
              if counter%2==0:
                total_list.append(j)
              else:
                cat.append(j)
          
          del total_list[-1]
          del cat[-1]
          #print cat
          #print total_list
          #print 'sfdf'
          if max(total_list)==0:
            M=1
          else:
            M=max(total_list)+0.1*max(total_list)
          self.b.set_ylim(0,M)
          self.b.set_xlim(0.5,5.5)
          self.b.set_xticks([1,2,3,4,5])
          self.b.set_xticklabels(cat,fontsize=9)
          
          #print total_list, len(total_list)        
          #total_list.append(100)
          
          
          while len(self.line1b)!=0:
            l2=self.line1b.pop(0)
            l2.remove()
            
          #self.line1b=[]
          #print 3
          total_list.append(0)
          #self.a.set_antialiased(False)
          #print total_list
          self.line1b=self.b.fill(total_list,'yellow',alpha=0.6)
          self.canvas.draw()
          
          
          
        
        else:
          
          self.c = self.f.add_subplot(212)        
          self.c.patch.set_color('black')
          self.c.patch.set_alpha(0.05)
          self.c.yaxis.grid('True')
          self.c.set_xlabel(self.combobox2.get_active_text(),fontsize=12)
          self.c.set_ylabel('Monthly Expense',fontsize=12)
          
          self.c.set_xlim(0,13)
          self.c.set_xticks(range(1,13))
          #self.c.set_xticks(range(5))
          #for i in max(monthly_totals_list):
            
          #print self.c.get_yticks()
          
          self.c.set_xticklabels(self.months,fontsize=11)
          year=self.combobox2.get_active_text()
          monthly_totals_list=[0]
          
          for i in range(12):
            cost=0
            s=year+'_'+str(self.months[i])
            #print s
            try:
              f=open(app.data_location+s,'r')
              s=f.readlines()
              f.close()
              
              #print 0
              for i in s:
                #print i[19:22]
                #print i
                cost+=float(i[19:27].strip())
                #print cost,
              
            except IOError:
              #print 2
              pass
            #print cost
            monthly_totals_list.append(cost)
          #print 
          
          if max(monthly_totals_list)==0:
            M=1
          else:
            M=max(monthly_totals_list)+0.1*max(monthly_totals_list)
          self.c.set_ylim(0,M)
          
          while len(self.line2)!=0:
            l=self.line2.pop(0)
            l.remove()
          
          self.line2=self.c.fill(monthly_totals_list,'green',alpha=0.6)
          self.canvas.draw()
          
          ##print line
        
        
      except AttributeError:
        pass
      
        
    
    def about(self,widget):
        dialog = gtk.AboutDialog()
        license='''Expense-Manager is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Expense-Manager is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Expense-Manager; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA'''
        dialog.set_license(license)
        dialog.set_wrap_license(False)
        dialog.set_name('Expense-Manager')
        dialog.set_copyright('(c) 2013 Souradeep De')
        dialog.set_website('http://github.com/desouradeep/Expense-Manager')
        #dialog.set_website_label('http://desouradeep.wordpress.com')
        dialog.set_authors(['Souradeep De \n email: <souradeep.2011@gmail.com> \n blog: http://desouradeep.wordpress.com'])
        dialog.set_program_name('Expense-Manager')
        dialog.set_version('1.0')
        dialog.run()
        dialog.destroy()
    
    def edit(self,widget):
        self.treeView.set_model(self.create_model())
        model=self.treeView.get_model()
        edit.edit(self.fname)
        #print 1
        
        update_list.main(self.fname)
          
        self.treeView.set_model(self.create_model())
        model=self.treeView.get_model()
        '''print 1
        for i in model:
            for j in i:
              print j,
            print
        print 2
        '''
        self.graphs(1)
        self.graphs(2)
        stats.update(self.fname)
        stats.treeView.set_model(stats.create_model(self))
        try:
          viewer.update(self,'')
          viewer.treeView.set_model(viewer.create_model(self))
        except AttributeError:
          pass
        
    def select_years(self):
        #this method selects the years to be stored in the years combobox        
        liststore2 = gtk.ListStore(str)
        f=open(app.data_location+'years','a')
        f.close()
        f=open(app.data_location+'years','r')
        yrs=f.readlines()
        f.close()
        #print 1
        x=0
        y=0
        for i in yrs:
            #print 'i = '+i[0:-1]
            i=i[0:-1]
            x=x+1
            if int(i)==self.yy:
              y=x
              #print y
            liststore2.append([i])
        #print yrs

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
        #creates a folder named data to store database in case /home/souradeep/data/ doesnt exist.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dest_dir = os.path.join(script_dir, 'data')        
        #print type(dest_dir), dest_dir
        try:
            os.makedirs(dest_dir)
        except OSError:
            pass 
      
        #creates a file(if not present) and opens it and reads its contents
        self.fname=app.data_location+str(widget.get_active_text())+'_'+self.combobox.get_active_text()
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
        self.graphs(1)
        self.graphs(2)
        stats.update(self.fname)
        stats.treeView.set_model(stats.create_model(self))
        try:
          viewer.update(self,'')
          viewer.treeView.set_model(viewer.create_model(self))
        except AttributeError:
          pass
        
        
      
    def changed_item(self,widget):
        #activated when combobox value holding months is changed
        #self.yy='2012'
        a= widget.get_active_text()
        
        #creates a folder named data to store database in case /home/souradeep/data/ doesnt exist.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dest_dir = os.path.join(script_dir, 'data')        
        try:
            os.makedirs(dest_dir)
        except OSError:
            pass           
        
        #creates a file(if not present) and opens it and reads its contents
        #self.select_years()
        
        try:
          #print type(self.combobox2.get_active_text())
          self.fname=app.data_location+self.combobox2.get_active_text()+'_'+a
          #print self.fname
          
          f=open(self.fname,'a')
          f.close()
          f=open(self.fname,'r')
          x=f.readlines()
          f.close()
        #print 1
          update_list.main(self.fname)
        except AttributeError:
          f=open(app.data_location+str(self.yy)+'_'+str(self.months[self.mm]),'a')
          f.close()
          update_list.main(app.data_location+str(self.yy)+'_'+self.combobox.get_active_text())
          pass
        
        try:
          self.treeView.set_model(self.create_model())
          #model=self.treeView.get_model()
        except AttributeError:
          pass
        
        #del self.line
        self.graphs(1)
        self.graphs(2)
        
        try:
          stats.update(self.fname)
          stats.treeView.set_model(stats.create_model(self))
        
        
          viewer.update(self,self.fname)
          viewer.treeView.set_model(viewer.create_model(self))
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
      
    def on_activated(self,widget):
      #single click on the treeView
      
      model=widget.get_model()
      #b= self.treeView.get_selection()
      b=self.treeView.get_cursor()
      row=0
      for i in b[0]:
        row= int(i)
        
     
        
      x=app.data_location+str(self.combobox2.get_active_text())+'_'+ model[row][0]
      #print x
      viewer.update(self,x)
      viewer.treeView.set_model(viewer.create_model(self))
      #print 1
    

   
         
    def terminate(self,a,r):
        clean_database.clean()
        sys.exit(0)
app()
gtk.main()
