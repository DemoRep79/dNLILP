from  Lib.ILPRLEngine import *
import argparse
from Lib.DNF import DNF

maxN = 5

#define constants
C = []
for i in range(maxN+1):
    C.append( '%d'%i)
Constants = dict( {'C':C })



#definition of even predicate in terms of odd
class MyFuncEven(PredFunc):
    def __init__(self,name='',trainable=True,predColl=None,index=1):
        
        super().__init__(name,trainable)
        self.predColl = predColl

    def pred_func(self,xi,xcs,t):
        ind  =  self.predColl.preds_by_name['even'].inp_list.index('odd(A)')
        return 1.0-xi[:,ind]
         
    def get_func(self,session,names,threshold=.2,print_th=True):
        return ""  



#define predicates
predColl = PredCollection (Constants)
predColl.add_pred(dname='zero' ,arguments=['C'] )
predColl.add_pred(dname='succ' ,arguments=['C','C'] )
predColl.add_pred(dname='odd' ,arguments=['C'], variables=['C'] ,  pFunc = DNF('odd',terms=4,init=[-1,1,-1,1] ,sig=2)     )

#defining even predicate in terms of odd 
predColl.add_pred(dname='even' ,arguments=['C'], variables=['C'] ,  pFunc = MyFuncEven(predColl=predColl)    )
predColl.initialize_predicates()    

#add background
bg = Background( predColl )
bg.add_backgroud ('zero', ('0',) ) 
 
 
for i in range(maxN+1):
    if( i+1<=maxN):
        bg.add_backgroud ('succ', ('%d'%i,'%d'%(i+1)) ) 
    
    bg.add_example( 'even', ('%d'%i,) , float(i%2==0))
        


def bgs(it,is_training):
    return [bg,]
 

###########################################################################


parser = argparse.ArgumentParser()

parser.add_argument('--CHECK_CONVERGENCE',default=1,help='Check for convergence',type=int)
parser.add_argument('--SHOW_PRED_DETAILS',default=1,help='Print predicates definition details',type=int)

parser.add_argument('--BS',default=1,help='Batch Size',type=int)
parser.add_argument('--T',default=8 ,help='Number of forward chain',type=int)
parser.add_argument('--LR_SC', default={ (-1000,2):.005 ,  (2,1e5):.01} , help='Learning rate schedule',type=dict)

parser.add_argument('--BINARAIZE', default=1 , help='Enable binrizing at fast convergence',type=int)
parser.add_argument('--MAX_DISP_ITEMS', default=10 , help='Max number  of facts to display',type=int)
parser.add_argument('--DISP_BATCH_VALUES',default=[],help='Batch Size',type=list)
parser.add_argument('--W_DISP_TH', default=.2 , help='Display Threshold for weights',type=int)
parser.add_argument('--ITER', default=400000, help='Maximum number of iteration',type=int)
parser.add_argument('--ITER2', default=200, help='Epoch',type=int)
parser.add_argument('--PRINTPRED',default=1,help='Print predicates',type=int)
parser.add_argument('--PRINT_WEIGHTS',default=0,help='Print raw weights',type=int)
parser.add_argument('--MAXTERMS',default=6 ,help='Maximum number of terms in each clause',type=int)
parser.add_argument('--L1',default=0 ,help='Penalty for maxterm',type=float)
parser.add_argument('--L2',default=0 ,help='Penalty for distance from binary for weights',type=float)
parser.add_argument('--L3',default=0 ,help='Penalty for distance from binary for each term',type=float)
parser.add_argument('--L2LOSS',default=0,help='Use L2 instead of cross entropy',type=int)
parser.add_argument('--SYNC',default=0,help='Synchronized Update',type=int)
parser.add_argument('--ALLTIMESTAMP',default=0 ,help='Add loss for each timestamp',type=int)
parser.add_argument('--FILT_TH_MEAN', default=.5 , help='Fast convergence total loss threshold MEAN',type=float)
parser.add_argument('--FILT_TH_MAX', default=.5 , help='Fast convergence total loss threshold MAX',type=float)
parser.add_argument('--OPT_TH', default=.05 , help='Per value accuracy threshold',type=float)
parser.add_argument('--PLOGENT', default=.50 , help='Crossentropy coefficient',type=float)
parser.add_argument('--BETA1', default=.90 , help='ADAM Beta1',type=float)
parser.add_argument('--BETA2', default=.999 , help='ADAM Beta2',type=float)
parser.add_argument('--EPS', default=1e-6, help='ADAM Epsillon',type=float)
parser.add_argument('--GPU', default=1, help='Use GPU',type=int)
parser.add_argument('--LOGDIR', default='./logs/Logic', help='Log Dir',type=str)
parser.add_argument('--TB', default=0, help='Use Tensorboard',type=int)
parser.add_argument('--SEED',default=0,help='Random seed',type=int)
parser.add_argument('--ADDGRAPH', default=1, help='Add graph to Tensorboard',type=int)
parser.add_argument('--CLIP_NORM', default=0, help='Clip gradient',type=float)
args = parser.parse_args()

print('displaying config setting...')
for arg in vars(args):
        print( '{}-{}'.format ( arg, getattr(args, arg) ) )
    

model = ILPRLEngine( args=args ,predColl=predColl ,bgs=bgs )
model.train_model()    

