{ time caffe train -gpu 0 -solver ConfFiles/solver.prototxt ; } 2>&1 | tee -a LogFiles/log$( date +%s ).log

