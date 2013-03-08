import copy, math, itertools, os, sys, pickle

def hex_chr(HexStr):
    Int=int('0x'+HexStr,16)
    Chr=chr(Int)
    return Chr

def check_pickle(FN):
    if not FN.endswith('.pickle'):
        FN=FN+'.pickle'
    return FN

def flatten_list(l):
    return [item for sublist in l for item in sublist]

def load_pickle(FN):
    FN=check_pickle(FN)
    Pr=open(FN,'rb')
    Stuff=pickle.load(Pr)
    Pr.close()
    return Stuff

def write_strlist_asline(L,FN):
    if all([ isinstance(El,str) for El in L ]):
        FSw=open(FN,'wt')
        for El in L:
            FSw.write(El+'\n')
        FSw.close()
    else:
        print("There are non-str elements, aborting"); exit()


def dump_pickle_check(Stuff,FN):
    FN=check_pickle(FN)
    Pw=open(FN,'bw')        
    pickle.dump(Stuff,Pw)
    Pw.close()
    Stuff=load_pickle(FN)
#    print(Stuff)
    


def identify_type_char(Char):
    TCMap={'num': [(48,57,),(65296,65305,)],
           'roman': [('0x0041','0x005a',),('0x0061','0x0077',),('0xff21','0xff3a',),('0xff41','0xff5a',)],
        'sym': [(33,47,),(58,64,),(91,96,),(123,126,),(8192,8303,),(8591,8597,),(9632, 9983,),(12288,12351,),(65280,65519,)],
        'han': [(19968, 40959,),('f900','faff')],
        'kana': [(12352,12543,)],
        'hangul': [('0xAC00','0xD7AF',)], 
        'jamo': [('0x1100','0x11FF',),('0x3130','0x318f',)],
        'ws': [('0x0009','0x0009',),('0x000A','0x000D',),('0x0020','0x0020',),('0x3000','0x3000',)],
     }

    for (Type,Ranges) in TCMap.items():
        if in_ranges(ord(Char), Ranges):
            return Type
    return 'unknown'


def in_ranges(TgtNum,Ranges):
    Val=False
    for Range in Ranges:
        if type(Range[0]).__name__=='str':
            LB=int(Range[0],16); UB=int(Range[1],16)
        else:
            LB=Range[0]; UB=Range[1]
            
        if TgtNum >= LB and TgtNum <= UB:
            Val=True
            break
    return Val


def all_of_types_p(Str,Types,*,UnivTypes=['ws','num','sym']):
    Bool=True
    Types.extend(UnivTypes)
    for Char in Str:
        CharType=identify_type_char(Char)
        if CharType not in Types:
            Bool=False; break
    return Bool


#def all_roman(Str):
#    return all( identify_type_char(Char)=='roman' or \
#                identify_type_char(Char)=='ws' or \
#                identify_type_char(Char)=='num' or \
#                identify_type_char(Char)=='sym' for Char in Str)
             

def identify_type_wd(Wd):
    if all( identify_type_char(Char)=='num' for Char in Wd):
        Val='num'
    elif all( identify_type_char(Char)=='sym' for Char in Wd):
        Val='sym'
    elif all( identify_type_char(Char)=='others' for Char in Wd):
        Val='others'
    else:
        Val= 'mixed'      
    return Val

def identify_type_wd_loose(Wd):
    Val='others'
    if any( identify_type_char(Char)=='jp' for Char in Wd):
        Val='jp'
    if all( identify_type_char(Char)=='roman' for Char in Wd):
        Val='roman'
    return Val



def chunks(List,N):
    """yield successive n-sized chunks"""
    for i in range(0,len(List),N):
        yield List[i:i+N]

def set_debug():
    global Debug
    Debug=True

def get_debug():
    return Debug

def iter2strs(Iter,Delim):
    Str=''
    for El in Iter:
        Str=Str+str(El)+Delim
    return Str

def numStr_p(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def all_true(Iter):
    Cum=True
    Cntr=0
    for Bool in Iter:
        if not Iter[Cntr]:
            break
        Cntr=Cntr+1
    return Cum


def reverse_keyval(Dict):
   RevDict={}
   RevDictVals=[]
   for Key in list(Dict.keys()):
      RevDictVals.append((Dict[Key],Key))
   RevDict.update(RevDictVals)
   return RevDict


def gen_cartesian_prod(LofTups):
    CumProd=[]
    PrevProd=[()]
    for Tup in LofTups:
        for El in Tup:
            for PrevTup in PrevProd:
                PrevL=list(PrevTup)
                PrevL.append(El)
                NewTup=tuple(PrevL)
                CumProd.append(NewTup)

        PrevProd=CumProd
        CumProd=[]

    return PrevProd

gen_cartesian_prod([(1,2),(3,),(4,5,6)])

choice=None

def prob2logit(Prob):

      return math.log(Prob/(1-Prob))

def logit2prob(Logit):
    NegLogit=-Logit
    return 1/(1+math.exp(NegLogit))

def coeffs2probs_ord(IntCoeffs):
    Int=IntCoeffs[0]
    CoeffLs=copy.deepcopy(IntCoeffs[1:])
    Probs=[]

    (CL1,CL2)=CoeffLs
    CL1.append(0)
    CL2.append(0)
    
    for Coeff1 in CL1:
        for Coeff2 in CL2:
            Logit=Int+Coeff1+Coeff2
            Prob=logit2prob(Logit)
            Probs.append(Prob)

    return Probs


def rlinput(Prefill='aaa'):
#    defaultText = 'I am the default value'
    readline.set_startup_hook(lambda: readline.insert_text(Prefill))
    res = input('Edit this:')
    print(res)

#def rlinput(Prompt, Prefill=''):
 #  readline.set_startup_hook(lambda: readline.insert_text(Prefill))
  # try:
   #   return eval(input(Prompt))
  # finally:
   #    readline.set_startup_hook()

#give a list of dics and a pair of key/val, you fetch the ones that have that value 
def collect_rightdics(Dics,TgtKey,TgtVal):
    RightDics=[]
    for Dic in Dics:
        if Dic[TgtKey]==TgtVal:
            RightDics.append(Dic)
    
    return RightDics

def collect_nths(LofCols,N):
    TgtL=[]
    for Col in LofCols:
        TgtL.append(Col[N-1])
    return TgtL

def powersets(SupS):
    PSet=set()
    for i in range(len(SupS)+1):
        SetToAdd=set(itertools.combinations(SupS, i))
        PSet=PSet.union(SetToAdd)
    return PSet

def randpick_from_list(L):
    import random
    return L[random.randint(0,len(L)-1)]

def partition(OrgCol):
    Parts=[]
    for i in range(math.floor((len(OrgCol)/2)+1)):
        Combs=list(itertools.combinations(OrgCol, i))
        for Comb in Combs:
            Compl=compl(OrgCol,Comb)
            if len(Comb)>=len(Compl):
                Comb1=Comb
                Comb2=Compl
            else:
                Comb2=Comb
                Comb1=Compl
            Pair=[Comb1,Comb2]
            if Pair not in Parts:
                Parts.append(Pair)
    return Parts

def compl(WholeL,Tuple):
    ComplL=[]
    for El in WholeL:
        if El not in Tuple:
            ComplL.append(El)
    return tuple(ComplL)


# given a list of strings, output 'a, b, c, .... 'conj' n'
def select_prompt(OrgOpts,Conj,*,Numbered=False):
    SelPr=""
    Punc=', '
    Len=len(OrgOpts)
    Cntr=0
    Sent=False
    while not Sent:
        Cntr=Cntr+1

        if Len == 0:
            Sent=True

        else: 
          CurOpt=OrgOpts[Cntr-1]

          if Numbered:
              NumStr=str(Cntr)+'. '
          else:
              NumStr=''

          if type(CurOpt).__name__!='str':
              CurStr=str(CurOpt)
          else:
              CurStr=CurOpt

          if Len == 1:
              Sent=True
              SelPr=NumStr+CurStr
          else:
              if Cntr == Len:
                  Sent=True
                  SelPr=SelPr+' '+Conj+' '

              if Cntr>=Len-1:
                  Punc=''

              SelPr=SelPr+NumStr+CurStr+Punc

    return SelPr


def merge_lists(Ls):
    LToExtend=copy.deepcopy(Ls[0])
    for L in Ls[1:]:
        LToExtend.extend(L)
    return LToExtend

def peek_next_line(FS):
    OrgP=FS.tell()
    NxtL=FS.readline()
    Pos=FS.tell()
    FS.seek(OrgP, 0)
    return NxtL,Pos

# convert all sorts of yes-no's to True and False, if nothing is entered, return '', if not convertible, return None
def yesno2bool(Str):
    LowerStr=Str.strip().lower()
    if LowerStr=='yes' or LowerStr=='y':
        Final=True
    elif LowerStr=='no' or LowerStr=='n':
        Final=False
    elif LowerStr=='':
        Final=''
    else:
        Final=None

    return Final
        


def prompt_loop_fn(Prompt,*,Ext='',Path='.'):
    Sent=False
    while not Sent:
        FNStem=input(Prompt+' (extension "'+Ext+'", or say "exit" to exit): ')

        if FNStem=='exit':
            Sent=True
            FullPath=None
 
        else:
            FN=FNStem+'.'+Ext
            FullPathCand=Path+'/'+FN

            if not os.path.exists(FullPathCand):
                print("The specified dir/file doesn't exist. Try again")
                FullPath=None

            else:
                Sent=True
                FullPath=FullPathCand

    return (FullPath,FNStem,FN)


def prompt_loop_fs(Prompt,*,Path='',WR='r'):
    Path=prompt_loop_fn(Prompt)
    FS=open(Path,WR)
    return FS


def prompt_loop_bool(Prompt,*,Default=False,DefaultSuppress=False):
    Sent=False
    if Default:
        DefStr='yes'
    else:
        DefStr='no'
    AddStr=''
    if not DefaultSuppress:
        AddStr=AddStr+"[default ("+DefStr+")]"
        
    while not Sent:
        YesNoStr=input(Prompt+" Enter [Yy](es) or [Nn](o) "+AddStr+": ")
        YesNoBool=yesno2bool(YesNoStr)
        if (YesNoBool=='' and DefaultSuppress) or YesNoBool==None:
            print("You don't seem to have entered [Yy](es) or [Nn](o). Try again")
        else:
            Sent=True
            if YesNoBool=='':
               YesNoBool=Default

    return YesNoBool


def prompt_loop1(Prompt,Type):
    Input=input(Prompt+": ").strip()
    if Type=='int':
        Val=int(Input)
    return Val 

def create_numlist(NofNs,*,StartNum=1,Interval=1):
    Cntr=StartNum
    Nums=[]
    for i in range(NofNs):
        Nums.append(Cntr)
        Cntr=Cntr+Interval
    return Nums

def list_num_print(L):
    Cntr=0
    Str=''
    for E in L:
        Cntr=Cntr+1
        Str=Str+str(Cntr)+': '+str(E)+', '

    print(Str)

    return Str


def lower_strs(OrgL):
    L=copy.deepcopy(OrgL)
    NewEs=[]
    for E in L:
        if type(E).__name__=='str':
            NewE=E.lower()
        else:
            NewE=str(E)
        NewEs.append(NewE)
    return NewEs

def str2num(Str):
    if numStr_p(Str):
        NumStr=int(Str)
    else:
        NumStr=Str
    return NumStr



def stringify_list(OrgL):
#    L=copy.deepcopy(OrgL)
    NewL=[]
    for E in L:
        if type(E).__name__!='str':
            NewE=str(E)
        else:
            NewE=E
        NewL.append(NewE)
    return NewL
    
def prompt_loop_list(Prompt,OrgSelectOps,*,Default=None,ReturnSingleEl=False,Numbered=False,MsgSuppress=False,AtLeast=1,AtMost=100):
    Choices=[]
    # return single el implies there's only a single el
    if ReturnSingleEl:
        AtLeast=1
        AtMost=1

    # if there's no choice
    if len(OrgSelectOps) == 0:
        print('Nothing to choose from, returning an empty list')
        Choices=[]
    # if there's only one choice
    elif len(OrgSelectOps) == 1:
        OnlyChoice=OrgSelectOps[0]
        if prompt_loop_bool(Prompt+"\nOnly one option, "+OnlyChoice+", is it your choice?"):
            Choices=[OnlyChoice]
        else:
            Choices=[]
    # normal case: more than one option
    else:
        Choices=prompt_loop_list2(Prompt,OrgSelectOps,Default,Numbered,MsgSuppress,AtLeast,AtMost)

    if ReturnSingleEl:
        Choices=Choices[0]

    return Choices

def prompt_loop_list2(Prompt,SelOps,Default,Numbered,MsgSuppress,AtLeast,AtMost):
    #first the prompt message created
    if not MsgSuppress: 
        SelectPrompt=select_prompt(SelOps,'or',Numbered=Numbered)

        Msg=" Please choose from the following\n"
        if Default==None:
            AddMsg=''
        else:
            AddMsg=' (Default='+str(Default)+')'

        if AtLeast != 1 and AtMost != 1:
            AddMsg=AddMsg+"\nFor multiple options, separate them with comma(s)."
        if AtLeast == 0:
            AddMsg=AddMsg+" For no option, say 'none'"
    
        Msg=Msg+SelectPrompt+AddMsg

    else:
        Msg=' Your option'

    Choices=[] 
    NumChoice=len(SelOps)
    # needed to allow lower case input
    LStrSelOps=lower_strs(SelOps)
    Sent=False
    while not Sent:
        # wrong input keeps the loop running
        WrongInput=False
        # notice we lower-case the input
        Answers=input(Prompt+Msg+": " ).lower().strip().split(',')
        AnswerCnt=len(Answers)
        # if nothing is inputted you flag error or take the default
        if Answers==['']:
            if Default==None:
                print('You need to enter at least one option')
                WrongInput=True
            else:
                Choices=[Default]
        else:
            # if the answer is 'none' return empty list or flag error if disallowed
            if Answers==['none']:
                if AtLeast==0:
                    Choices=[]
                else:
                    print('You have to choose at least one option.')
                    WrongInput=True

            elif AnswerCnt < AtLeast or AnswerCnt > AtMost:
                print('You entered either too few or too many answers.')
                WrongInput=True

            # below's the normal list case
            else:
                # numbering allows the user to pick the corresponding num
                if Numbered:
                    for Answer in Answers:
                        if numStr_p(Answer):
                            AnswerNum=int(Answer)
                            # just to exclude out-of-range input error
                            if AnswerNum > 0 or AnswerNum <= AnswerCnt:
                                Choices.append(SelOps[AnswerNum-1])
                            else:
                                print('You entered the wrong number(s).')
                                WrongInput=True
                        # we'd also allow text input. remember we're handling lower case strings!
                        elif Answer in LStrSelOps:
                            Choices.append(same_ind_el(Answer,LStrSelOps,SelOps))
                        else:
                            print("There is no such option.")
                            WrongInput=True
            # if un-numbered
                else:
                    for Answer in Answers:
                        if Answer in LStrSelOps:
                            Choices.append(same_ind_el(Answer,LStrSelOps,SelOps))
                        else:
                            print("There is no such option.")
                            WrongInput=True

        if WrongInput:
            print("Wrong or no input. Try again")
        else:
            Sent=True

    return Choices

def same_ind_el(OrgE,OrgL,TgtL):
    return TgtL[OrgL.index(OrgE)]
