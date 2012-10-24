#!/usr/bin/env python
z=[]
def main(fname):
	#fname='data/2012_OCT'
	f=open(fname)
	lines=f.readlines()
	f.close()
	
	#for i in lines:
	#      print i
	ch=0
	if fname.find('_')==9:
	  ch=1
	mm=fname[9+ch:]
	#print mm
	  
	#print mm
	ndays=[31,29,31,30,31,30,31,31,30,31,30,31]
	months=["JAN",'FEB','MAR','APR','MAY','JUNE','JULY','AUG','SEPT','OCT','NOV','DEC']
	nd=0
	
	for i in range(0,12):
	  if months[i]==mm:
	    nd=ndays[i]
	#print nd
	#z=[]
	for j in z:
	    for i in range(1,7):
	      j[i]=0
	for i in range(0,len(z)):
	    del z[-1]
	for i in range(0,nd):
	  z.append(['',0,0,0,0,0,0])
	#print len(z)
	for i in range(1,nd+1):
	  if i<10:
	    z[i-1][0]=mm+' 0'+ str(i)
	  else:
	    z[i-1][0]=mm+' '+ str(i)
	   
	  for k in lines:
	    d=k[0:6+ch]
	    c=k[7:16]
	    p=float(k[19:29])
	    for j in z[i-1]:
	      s1=z[i-1][0]
	      s2=d
	      if s1.strip()==s2.strip():
		#print s1,s2,s1.strip()==s2.strip()
		if c.strip()=='ENTR':
		  z[i-1][1]+=p	
		if c.strip()=='FOOD':
		  z[i-1][2]+=p
		if c.strip()=='OTHERS':
		  z[i-1][3]+=p
		if c.strip()=='MOBILE':
		  z[i-1][4]+=p
		if c.strip()=='TRANSPORT':
		  z[i-1][5]+=p
		z[i-1][6]=0
		for x in range(1,6):
		  z[i-1][6]+=z[i-1][x]
		break
	#for i in z:
	   # print i
	
	 
#main()