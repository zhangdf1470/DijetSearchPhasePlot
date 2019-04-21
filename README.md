python -b scriptResonance/SearchPhase/plotSearchPhase.py --inFileName input/SearchResultData_Resonance.root --outPath ./plotting/SearchPhase/plots_Resonance/ --lumi 139
# Draw Comparison of Nominal and Alternate Fitting
python -b scriptResonance/SearchPhase/plotSearchPhase.py --inFileName input/SearchResultData_Resonance.root --outPath ./plotting/SearchPhase/plots_Resonance/ --doAlternate --lumi 139
# Signal overlaid on Background
python -b scriptResonance/SearchPhase/plotSearchPhase.py --inFileName input/SearchResultData_Resonance.root --outPath ./plotting/SearchPhase/plots_Resonance/ --overlaidSignal --signalFileName input/dijetMC_qstar_fullBins.root --lumi 139
# Signal overlaid on Background and compare the data with MC
python -b scriptResonance/SearchPhase/plotSearchPhase.py --inFileName input/SearchResultData_Resonance.root --outPath ./plotting/SearchPhase/plots_Resonance/ --overlaidSignal --signalFileName input/dijetMC_qstar_fullBins.root --mcFileName input/pseudoMC.root --drawMCComparison --lumi 139

python -b scriptResonance/SearchPhase/plotSearchPhase.py --inFileName input/Step1_SearchPhase/SWiFtConfig2/4Paras/OldBin/SearchResultData_Resonance_Run2_140fb.root --outPath ./Test/ --lumi 139 --mcFileName input/pseudoMC.root --drawMCComparison --overlaidSignal --signalFileName input/dijetMC_qstar_fullBins.root

#Draw BumpHunter Out
python scriptResonance/BumpHunter/plotBumpHunter.py --inFileName input/BumpHunter_Resonance.root --outPath plotting/BumpHunter/plots_Resonance/ --lumi 37
# Signal overlaid on Background
python scriptResonance/BumpHunter/plotBumpHunter.py --inFileName input/BumpHunter_Resonance.root --outPath plotting/BumpHunter/Test/ --lumi 139 --overlaidSignal --signalFileName input/dijetMC_qstar_fullBins.root
# WithMCRatio
python scriptResonance/BumpHunter/plotBumpHunter.py --inFileName input/BumpHunter_Resonance.root --outPath plotting/BumpHunter/Test/ --lumi 139 --overlaidSignal --signalFileName input/dijetMC_qstar_fullBins.root --mcFileName input/pseudoMC.root --drawMCComparison
