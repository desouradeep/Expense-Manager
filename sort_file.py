#!/usr/bin/python
import sys
def main(s):
  #print s,type(s)
  f=open(s,'r')
  lines=[]
  lines=f.readlines()
  lines.sort()
  f.close()
  #print s,type(s)
  f=open(s,'w')
  for i in lines:
    f.write(i)
