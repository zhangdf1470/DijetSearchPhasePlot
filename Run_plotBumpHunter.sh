for Seed in 2000
do
  #inPath="input/Gaus10perSeed${Seed}a/"
  inPath="input/Step1_SearchPhase/SWiFtConfig2/4Paras/OldBin/DibSpuriousSignal/mbb/"
  outPath="./plotting/SearchPhase/SWiFtConfig2/4Paras/OldBin/DibSpuriousSignal/mbb/"
  inPath="input/Step1_SearchPhase/SWiFtConfig2/4Paras/OldBin/"
  outPath="./plotting/SearchPhase/SWiFtConfig2/4Paras/OldBin/"
  for file in $(ls ${inPath})
  do
    if [[ $file != *".root" ]] || [[ $file != *"Wstar"* ]] || [[ $file != *"140fb"* ]]
    #if [[ $file != *".root" ]] 
    then 
      continue
    fi
    outPath_tmp=${outPath}${file%.root}/
    echo $outPath_tmp
    mkdir -p $outPath_tmp
    #python -b scriptResonance/BumpHunter/plotBumpHunter.py --inFileName ${inPath}/${file} --outPath $outPath_tmp --lumi 140
    #python -b scriptWStar/BumpHunter/plotBumpHunter.py --inFileName ${inPath}/${file} --outPath $outPath_tmp --lumi 140
    #python -b scriptResonance/SearchPhase/plotSearchPhase.py --inFileName ${inPath}${file} --outPath $outPath_tmp --lumi 139
    python -b scriptWStar/SearchPhase/plotSearchPhase.py --inFileName ${inPath}${file} --outPath $outPath_tmp --lumi 139
  done
done

#python -b scriptResonance/SearchPhase/plotSearchPhase.py --inFileName input/Step1_SearchPhase/SWiFtConfig2/3Paras/OldBin/SearchResultData_Wstar_Run2_140fb_SWiFtL22R22Bins.root --outPath ./plotting/SearchPhase/SWiFtConfig2/3Paras/OldBin/SearchResultData_Wstar_Run2_140fb_SWiFtL22R22Bins/ --lumi 140
#python -b scriptResonance/SearchPhase/plotSearchPhase.py --inFileName input/Step1_SearchPhase/SWiFtConfig2/3Paras/OldBin/SearchResultData_Wstar_Run2_140fb_SWiFtL20R20Bins.root --outPath ./plotting/SearchPhase/SWiFtConfig2/3Paras/OldBin/SearchResultData_Wstar_Run2_140fb_SWiFtL20R20Bins/ --lumi 140
