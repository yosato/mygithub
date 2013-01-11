# coding: utf-8
from __future__ import division
try:
	
    import getopt, sys, os, re, random, math, codecs
except:
    sys.stderr.write( "ERROR: a module necessary could not be imported\n" )
    sys.exit(2)
  
def usage():
	
	print """ python dbdmake.py <inputDIR> <outputFILE>
	
		<inputDIR> 	Directory where .unp files present the full path. This path is used
		<outputFILE> 	.dbd FILE name including path
	
	This program will write the correspoinding dbd file for the unp files
	present in the inputDIR"""


try:
    args = sys.argv[1:]
    
except sys.ErrorDuringImport:
    usage()
    sys.exit(2)


if len(args) !=2 :
	usage()
	
	sys.exit("=======No input and output directory specified======")
else:
	if not os.path.exists(args[0]) :
		print "path unreachable :"+args[0]
		sys.exit()
	if not os.path.exists(os.path.dirname(args[1])):
		print "path unreachable :"+args[1]
		sys.exit()

inDIR=args[0]
outFILE=args[1]
filesInDIR = os.listdir(inDIR)

count = 0
for itfFILE in filesInDIR:
	
	#print itfFILE
	if itfFILE.endswith(".unp"):
		
		count =count+1		
		print "processing file : "+itfFILE
		
		label=""
		
		f=codecs.open(inDIR+"/"+itfFILE,"r","utf-8")
		l=f.readlines()
		
		for i in l:
			if "SEGMENT" in i:
				label = i.strip().rpartition(" \"")[2]
				label = label[0:len(label)-1]
				break
		f.close()
		
		if label :
			
			f=codecs.open(outFILE,"a","utf-8")
			#f=open(outFILE,"w")
			f.write(inDIR+itfFILE+" "+label+"\n")
			#print inDIR+itfFILE+" "+label
		
		else:
			print itfFILE+" contains empty label"
		

print str(count)+" dbd files created"
