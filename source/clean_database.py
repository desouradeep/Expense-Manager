import os
import datetime
import getpass
def clean():
  data_location='/home/'+getpass.getuser()+'/.expensemanager/data/'
  f=open(data_location+'years','r')
  years=f.readlines()
  f.close()
  months=["JAN",'FEB','MAR','APR','MAY','JUNE','JULY','AUG','SEPT','OCT','NOV','DEC']
  for i in range(0,len(years)):
    year=years[i][0:-1]
    #print year
    
    for j in range(0,12):
      fname=data_location+year+'_'+months[j]
      #print fname
      try:
        #print 1
        f=open(fname,'r')
        rec=f.readlines()
        f.close()
        #print fname,len(rec)
        if len(rec)==0:
          script_dir = os.path.dirname(os.path.abspath(__file__))
          os.remove(fname)
  
      except :
        pass
      
  all_files=os.listdir(data_location)
  #print all_files
  for i in range(0,len(all_files)):
    count=0
    for j in range(0,len(years)):
      find=all_files[i].find(years[j][0:-1])
      #print all_files[i],years[j][0:-1],
      if find==-1:
        count=count+1
    if count==len(years) and all_files[i].find('years')==-1:
      #print all_files[i]
      script_dir = os.path.dirname(os.path.abspath(__file__))+data_location+all_files[i]
      os.remove(script_dir)
        
    now=datetime.datetime.now()
    mm=now.month-1
    yy=now.year
    f=open(data_location+str(yy)+'_'+str(months[mm]),'a')
    f.close()
#clean()
