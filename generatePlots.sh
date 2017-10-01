run(){
  COLOR='\033[1;33m'
  DEFAULT='\033[0m'
  echo -e "${COLOR}-> ${1}${DEFAULT}";
  eval ${1};
}

for file in LogFiles/*
do
  run "python AuxScripts/logToPlots.py $file"
done