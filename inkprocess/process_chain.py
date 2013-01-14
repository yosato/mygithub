#!/usr/env python2

import imp

import label_itf, split, dbdMake

imp.reload(label_itf)
imp.reload(split)
imp.reload(dbdMake)

labelFN='testdirs/labels/hiragana_label.txt'
itfInputFN='testdirs/itfs/gojuon_jp2.itf'
itfOutputFN='testdirs/itfs/labeled.itf'

unpDir='testdirs/unps'
dbdDir='testdirs/dbds'

if __name__=='__main__':
    
    label_itf.main(labelFN,itfInputFN,itfOutputFN)
#    split.main(itfOutputFN,unpDir)
#    dbd-make.main(unpDir,dbdDir)
