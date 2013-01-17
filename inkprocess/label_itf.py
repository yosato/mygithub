# coding: utf-8
try:
    import getopt, sys, os, re, random, math, codecs
except:
    sys.stderr.write( "ERROR: a module necessary could not be imported\n" )
    sys.exit(2)

def usage():
    print """label-itf.py
    
    python label-itf.py -l <label_file>  <itfFile> <outFile>

    parametres:
    
	<label_file>	Label file
	<itfFile>	originalItf file with complete path
	<outFile>	outputFilename with complete path
				
				itfFile should have #UniPenLabel utf8 line in each of the ActiveBox before proceeding
	example : 
           
    """

def main(labelFile,itfFile,outputFN):

    labelLine=labelFile.readlines()
    itfLine=itfFile.readlines()

    count=0
    for idx in range( len(itfLine) ):
	
	print 	itfLine[idx].strip().lower()
	#first line edit
	if "#unipenlabel" in itfLine[idx].lower() :
		
		if count <= len(labelLine):
			itfLine[idx] = itfLine[idx].strip()+" "+labelLine[count]
			print itfLine[idx].strip()
			count = count + 1
		else:
			print " amount of unipenlabel and actual labels not equal"


#    f = codecs.open(outputFN,"w", "utf-8")
    f = open(outputFN,'w')

    print str(len(labelLine)) + " " + str(count)
    if len(labelLine) == count:
	
	for l in range(len(itfLine)) :
            f.write(itfLine[l].strip())
	#	print >> f,itfLine[l].strip()
	f.close()
    else :
	print "length of label file and itf file not equal"
        sys.exit(2)



if __name__=='__main__':	

    try:
        opts, args = getopt.getopt( sys.argv[1:], 'l:h', ["label-file=","help"] )
    except getopt.GetoptError:
        usage()
        sys.exit(2)
   

    print len(opts)

    if len(opts) != 1:
	usage()
	exit(2)

    for o, v in opts:
	
	if o in ('-h', '--help'):
            usage();
            sys.exit(2)
			

	elif o in ('-l','--label-file'):
		
            try:
			with open(v) as f: pass
			labelFile=codecs.open(v,'r',"utf-8")
			#labelLine=labelFile.readlines()
			
            except IOError as e:
			s = " label file could not be opened"+v
			exit(s)
	else:
            usage()
            exit(2)
			


    if len( args ) != 2:
	usage()
	sys.exit( "Requires one lexicon filename " )
    else:	
	try:
		with open(args[0]) as f: pass
		
	except IOError as e:
		s = args[0]+ " Input and output files could not be opened"
		exit(s)
	



    itfFile=codecs.open(args[0],'r',"utf-8")
    #itfLine=itfFile.readlines()

    main(labelLine, itfLine, args[1])


	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

