#!/usr/bin/python
# this is the example script to use xgboost to train 
import sys
import numpy as np
# add path of xgboost python module
sys.path.append('../../python/')
import xgboost as xgb

# path to where the data lies
dpath = 'data'

modelfile = 'higgs.model'
outfile = 'higgs.pred.csv'
# make top 15% as positive 
threshold_ratio = 0.15

# load in training data, directly use numpy
dtest = np.loadtxt( dpath+'/test.csv', delimiter=',', skiprows=1 )
data   = dtest[:,1:31]
idx = dtest[:,1]

xtest = xgb.DMatrix( data, missing = -999.0 )
bst = xgb.Booster()
bst.load_model( modelfile )

ypred = bst.predict( dtest )
res  = [ ( int(idx[i]), ypred[i] ) for i in xrange(len(ypred)) ] 

rorder = {}
for k, v in sorted( res, key = lambda x:-x[1] ):
    rorder[ k ] = len(rorder) + 1

# write out predictions
ntop = int( ratio * len(rorder ) )
fo = open(outfile, 'w')
nhit = 0
ntot = 0
fo.write('EventId,RankOrder,Class\n')
for k, v in res:        
    if rorder[k] <= ntop:
        lb = 's'
        nhit += 1
    else:
        lb = 'b'        
    fo.write('%s,%d,%s\n' % ( k, rorder[k], lb ) )
    ntot += 1
fo.close()

print 'finished writing into model file'



