
from util import *

class DataTrain:
  def __init__(self, train):
    #Train evolution information
    self.epoch = []
    self.mse_trn = []
    self.mse_val = []
    self.sp_val = []
    self.det_val = []
    self.fa_val = []
    self.mse_tst = []
    self.sp_tst = []
    self.det_tst = []
    self.fa_tst = []
    self.is_best_mse = []
    self.is_best_sp = []
    self.is_best_det = []
    self.is_best_fa = []
    self.num_fails_mse = []
    self.num_fails_sp = []
    self.num_fails_det = []
    self.num_fails_fa = []
    self.stop_mse = []
    self.stop_sp = []   
    self.stop_det = []   
    self.stop_fa = []   
    #Get train evolution information from TrainDatapyWrapper
    for i in range(len(train)):
      self.epoch.append(train[i].epoch)
      self.mse_trn.append(train[i].mseTrn)
      self.mse_val.append(train[i].mseVal)
      self.sp_val.append(train[i].spVal)
      self.det_val.append(train[i].detVal)
      self.fa_val.append(train[i].faVal)
      self.mse_tst.append(train[i].mseTst)
      self.sp_tst.append(train[i].spTst)
      self.det_tst.append(train[i].detTst)
      self.fa_tst.append(train[i].faTst)
      self.is_best_mse.append(train[i].isBestMse)
      self.is_best_sp.append(train[i].isBestSP)
      self.is_best_det.append(train[i].isBestDet)
      self.is_best_fa.append(train[i].isBestFa)
      self.num_fails_mse.append(train[i].numFailsMse)
      self.num_fails_sp.append(train[i].numFailsSP)
      self.num_fails_det.append(train[i].numFailsDet)
      self.num_fails_fa.append(train[i].numFailsFa)
      self.stop_mse.append(train[i].stopMse)
      self.stop_sp.append(train[i].stopSP)
      self.stop_det.append(train[i].stopDet)
      self.stop_fa.append(train[i].stopFa)

    self.epoch_best_sp  = self.lastIndex(self.is_best_sp,  True)
    self.epoch_best_det = self.lastIndex(self.is_best_det, True)
    self.epoch_best_fa  = self.lastIndex(self.is_best_fa,  True)
 
    

  def lastIndex(self, l, value ):
    l.reverse()
    return len(l)  -1 - l.index(value)


  def showInfo(self, i = 0):
    print 'epoch          =', self.epoch[i]
    print 'mse_trn        =', self.mse_trn[i]
    print 'mse_val        =', self.mse_val[i]
    print 'sp_val         =', self.sp_val[i]
    print 'mse_tst        =', self.mse_tst[i]
    print 'sp_tst         =', self.sp_tst[i]
    print 'is_best_mse    =', self.is_best_mse[i]
    print 'is_best_sp     =', self.is_best_sp[i]
    print 'num_fails_mse  =', self.num_fails_mse[i]
    print 'num_fails_sp   =', self.num_fails_sp[i]
    print 'stop_mse       =', self.stop_mse[i]
    print 'stop_sp        =', self.stop_sp[i]   
 

class Performance:
  def __init__(self, spVec, detVec, faVec, cutVec):
    self.spVec  = spVec;
    self.cutVec = cutVec;
    self.detVec = detVec;
    self.faVec  = faVec;
    idx = spVec.index(max(spVec));
    self.sp  = spVec[idx];
    self.det = detVec[idx];
    self.fa  = faVec[idx];
    self.cut = cutVec[idx];

  def showInfo(self):
    print 'sp  = ',self.sp
    print 'det = ',self.det
    print 'fa  = ',self.fa
    print 'cut = ',self.cut

