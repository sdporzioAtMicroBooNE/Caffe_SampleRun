{ time caffe train -gpu 1 -solver ConfFiles/solver.prototxt ; } 2>&1 | tee -a LogFiles/log.log

