# just the python rendering of 'uniq', order preserving de-duplication

def uniq(List):
    Uniqs=[]
    Prev=''
    for El in List:
        if El!=Prev:
           Uniqs.append(El)
        Prev=El

    return Uniqs

import sys

if __name__=='__main__':
    if len(sys.argv[1])==2:
        print('Give an argument, the filename!'); exit()
    else:
        FN=sys.argv[1]
    List=open(FN).read().split('\n')
    Uniqs=[ El for (Cntr,El) in enumerate(List) if El!=List[Cntr-2] ]
    for Line in Uniqs:
        sys.stdout.write(Line+'\n')
        
