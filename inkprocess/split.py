# coding: utf-8

# changes made by YS: make the input list based. The user inputs either Dir or the list of files. One needs to give a list even for a single file, i.e. [<FileName.].

Usage= """ python split.py <inputDir/FILEs> <outputDIR>
	
		<inputDir/FILEs> 	Directory where .itf files present or list of files
		<outputDIR> 	Directory where .unp files should be saved
	
	This program will output files with the same name but with different
	indexes for instance if there is an input file named Sentence.itf then
	the output would be Sentence-0.unp ; Sentence-1.unp ; Sentence-2.unp...
	and depends on how many ActiveBox are present"""


from __future__ import division

try:
	
    import getopt, sys, os, re, random, math, codecs
except:
    sys.stderr.write( "ERROR: a module necessary could not be imported\n" )
    sys.exit(2)
  

def makeUNP(filesInDIR, inDIR,outDIR):
	#print filesInDIR
	if itfFILE.endswith(".itf"):
		
		print "processing file : "+itfFILE
		
		labelLIST=list()
		AddActiveBoxLIST=list()
		boxInitX=list()
		boxInitY=list()
		boxMaxX=list()
		boxMaxY=list()
		AddStrokeLIST=list()
		outputLIST=list()
		
		AABCount=0
		ULCount=0
		readXY_pointer=0
		xyExpr= re.compile("[0-9]+\.?[0-9]+\s[0-9]+\.?[0-9]+")
		
	
		f = codecs.open(inDIR+"/"+itfFILE,'r',"utf-8")
		l = f.readlines()
		f.close()
		
		for lineNum in range( len(l) ):
			
			## labels should have encoding utf8 or utf-8 for it to work 
			if "unipenlabel" in l[lineNum].lower():
				tmp=re.split("utf8|utf-8", l[lineNum].strip().lower())
				
				if len(tmp) == 2 :
					tmp=tmp[1].strip()
				else:
					print itfFILE+" do not contain \"utf8\" encoding info in the UnipenLabel info\nplease fix this continuing with other files"
					break
					
				
				if tmp :
					labelLIST.append(tmp)
				else:
					labelLIST.append(" ")
					print "empty label"
				ULCount=ULCount+1  #keep track of how many labels are present
				#print re.split("utf8|utf-8", l[lineNum].strip())[1].strip()
			
			if "AddActiveBox" in l[lineNum]:
				AABCount=AABCount+1  #keep track of how many active boxes are present
				outputLIST.append(list())
				tmp=l[lineNum].strip().split()
				if len(tmp) ==5 :
					boxInitX.append( float(tmp[1]) )
					boxInitY.append( float(tmp[2]) )
					boxMaxX.append( float(tmp[1])+float(tmp[3]) )
					boxMaxY.append( float(tmp[2])+float(tmp[4]) )
				else:
					print "Active Box format does not contain exactly 4 fields seperated with space. "
				
				#print l[lineNum].partition(" ")[2].strip()
			
			if "AddStroke" in l[lineNum]:
				#print l[lineNum].strip()
				#next line has to be coordinates
				NXTlineNum =lineNum+1
				
				strokeXYLIST=list()
				strokeX=list()
				strokeY=list()
				
				strokeXYLIST.append( ".PEN_DOWN" )
				while xyExpr.search(l[NXTlineNum].strip()):
					
					tmp = l[NXTlineNum].strip().split()
					
					strokeXYLIST.append( l[NXTlineNum].strip() )
					strokeX.append(float( tmp[0]) )
					strokeY.append(float( tmp[1]) )
					
					if NXTlineNum+1 < len(l): #EOF check
						NXTlineNum +=1				
					else:
						break
				strokeXYLIST.append( ".PEN_UP" )
				
				lineNum = NXTlineNum-1 #fix index
				
				#if stroke coordinates not empty then it indicates there is strokes
				#find which active box is belongs to and save it in some place.
				if strokeX:
					
					maxX=max(strokeX)
					minX=min(strokeX)
					maxY=max(strokeY)
					minY=min(strokeY)
					
					#print "============"
					for idxLabel in range(AABCount):
						
						if maxX<=boxMaxX[idxLabel] and minX>= boxInitX[idxLabel] and maxY<=boxMaxY[idxLabel] and minY>= boxInitY[idxLabel] :# corresponding label found
							outputLIST[idxLabel].append(strokeXYLIST)
							#outputLIST[idxLabel].append("AddStroke")
							#outputLIST[idxLabel].append(strokeX)
							#outputLIST[idxLabel].append(strokeY)
							
					
					#print str(maxX)+" "+str(minX)+" "+str(maxY)+" "+str(minY)
					#print "============"
					
				else:
					print("no strokes recorded")
		
		#Print the outputlist
		
		if AABCount == ULCount :
			
			print "Formating good - label = activebox"
			
			for idxOut in range(len(outputLIST)) :				
				f = codecs.open(outDIR+"/"+itfFILE+"-"+str(idxOut)+".unp","w", "utf-8")
				#print outDIR+"/"+itfFILE+"-"+str(idxOut)+" "+labelLIST[idxOut]
				print>>f,".CCORD X Y\n.ENCODING UTF8\n.SEGMENT ? ? ? \""+labelLIST[idxOut]+"\"\n.PAGE_SIZE 660 350"
				for fLEVEL in outputLIST[idxOut]:
					for sLEVEL in fLEVEL:
						if isinstance(sLEVEL,list):
							for innerLEVEL in sLEVEL:
								print>> f,innerLEVEL
						else:
							print>> f,sLEVEL
					
				f.close()
		else:
			print "Number of labels and activebox are not the same...\n .unp file not created for this itf file !!!\nPlease fix the problem before launching again !!!\n For now moving on.."

def usage():
	
	print Usage



# Script starts here
if __name__=='__main__':

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
        if not os.path.exists(args[1]):
            print "path unreachable :"+args[1]
            sys.exit()
	
    inFiles=args[0]
    outDIR=args[1]

    if type(inFiles)=='list':
        if os.path.isfile(inDIR) :
            if "/" in inDIR:
		tmp=inDIR.rpartition("/")
		itfFILE=tmp[2]
		
            print itfFILE
            makeUNP(itfFILE, tmp[0],outDIR)
	
    elif os.path.isdir(inDIR) :
	filesInDIR = os.listdir(inDIR)
	print "directory"
	for itfFILE in filesInDIR:
		makeUNP(itfFILE, inDIR,outDIR)


