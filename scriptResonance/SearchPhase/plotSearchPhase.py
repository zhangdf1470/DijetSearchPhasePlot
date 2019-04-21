#!/usr/bin/env python

import ROOT
from art.morisot import Morisot
from array import array
import sys,os
import argparse

def main():

    # User controlled arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--inFileName",       type=str,  default="", help="The path to the input file from SearchPhase")
    parser.add_argument("--outPath",       type=str,  default="./plotting/SearchPhase/plots/", help="The path prefix (directory) where you want the output plots")
    parser.add_argument("--lumi",       type=float,  default=1, help="Luminosity in fb-1")
    parser.add_argument("--doAlternate",     action='store_true', help="Compare Nominal and Alternate Fit")
    parser.add_argument("--overlaidSignal", action='store_true', help="Overlaid Signal on Background")
    parser.add_argument("--signalFileName", type=str, default="", help="Signal histogram overlaid on background")
    parser.add_argument("--drawMCComparison", action='store_true', help="Draw the comparison between data and MC")
    parser.add_argument("--mcFileName", type=str, default="", help="MC File Name")

    args = parser.parse_args()
    inFileName       = args.inFileName
    outPath       = args.outPath
    luminosity = 1000*args.lumi
    doAlternate = args.doAlternate
    overlaidSignal = args.overlaidSignal
    signalFileName = args.signalFileName
    drawMCComparison = args.drawMCComparison
    mcFileName = args.mcFileName
    
    print "==================================="
    print "Executing Run_SearchPhase.py with :"
    print "inFileName       : ",inFileName      
    print "outPath       : ",outPath
    print "Lumi       : ", args.lumi
    print "doAlternate: ", doAlternate
    print "overlaidSignal: ", overlaidSignal
    if overlaidSignal: 
      print " signalFileName: ", signalFileName
    print "drawMCComparison: ", drawMCComparison
    print "mcFileName: ", mcFileName
    print "==================================="

    # Get input (the rootfile name should match that specified in the SearchPhase.config file)
    searchInputFile = ROOT.TFile(inFileName, "READ")

    # make plots folder i.e. make folder extension
    if not os.path.exists(outPath):
        os.makedirs(outPath)

    # Define necessary quantities.
    Ecm = 13

    # Get input
    doStatSearch = False
    #doAlternate = True # You can use this if you included the alternate fit function in the search phase

    # Initialize painter
    myPainter = Morisot()
    myPainter.setColourPalette("Teals")
    #myPainter.setEPS(True)
    myPainter.setLabelType(2) # Sets label type i.e. Internal, Work in progress etc.
                              # See below for label explanation

    # 0 Just ATLAS    
    # 1 "Preliminary"
    # 2 "Internal"
    # 3 "Simulation Preliminary"
    # 4 "Simulation Internal"
    # 5 "Simulation"
    # 6 "Work in Progress"

    # Retrieve search phase inputs
    basicData = searchInputFile.Get("basicData")
    basicBkg = searchInputFile.Get("basicBkgFrom4ParamFit")
    #normalizedData = searchInputFile.Get("normalizedData")
    #normalizedBkgFrom4ParamFit = searchInputFile.Get("normalizedBkgFrom4ParamFit")
    residualHist = searchInputFile.Get("residualHist")
    relativeDiffHist = searchInputFile.Get("relativeDiffHist")
    sigOfDiffHist = searchInputFile.Get("sigOfDiffHist")
    logLikelihoodPseudoStatHist = searchInputFile.Get("logLikelihoodStatHistNullCase")
    chi2PseudoStatHist = searchInputFile.Get("chi2StatHistNullCase")
    bumpHunterStatHist = searchInputFile.Get("bumpHunterStatHistNullCase")
    #theFitFunction = searchInputFile.Get('theFitFunction')
    bumpHunterTomographyPlot = searchInputFile.Get('bumpHunterTomographyFromPseudoexperiments')
    bumpHunterStatOfFitToData = searchInputFile.Get('bumpHunterStatOfFitToData')

    # nominal background +- statistical uncertainty(uncertainty from fitting parameters)
    nomPlus1 = searchInputFile.Get("nominalBkgFromFit_plus1Sigma")
    nomMinus1 = searchInputFile.Get("nominalBkgFromFit_minus1Sigma")

    #nominal background +- uncertainties from fitting function choice
    if doAlternate :
      alternateBkg = searchInputFile.Get("alternateFitOnRealData")
      nomWithNewFuncErrSymm = searchInputFile.Get("nomOnDataWithSymmetricRMSScaleFuncChoiceErr")
      valueNewFuncErrDirected = searchInputFile.Get("nomOnDataWithDirectedRMSScaleFuncChoiceErr")

    logLOfFitToDataVec = searchInputFile.Get('logLOfFitToData')
    chi2OfFitToDataVec = searchInputFile.Get('chi2OfFitToData')
    statOfFitToData = searchInputFile.Get('bumpHunterPLowHigh')
    logLOfFitToData = logLOfFitToDataVec[0]
    logLPVal = logLOfFitToDataVec[1]
    chi2OfFitToData = chi2OfFitToDataVec[0]
    chi2PVal = chi2OfFitToDataVec[1]
    bumpHunterStatFitToData = statOfFitToData[0]
    bumpHunterPVal = bumpHunterStatOfFitToData[1]
    bumpLowEdge = statOfFitToData[1]
    bumpHighEdge = statOfFitToData[2]

    #NDF = searchInputFile.Get('NDF')[0]
    #fitparams = searchInputFile.Get('fittedParameters')

    print "logL of fit to data is",logLOfFitToData
    print "logL pvalue is",logLPVal
    print "chi2 of fit to data is",chi2OfFitToData
    #print "NDF is",NDF
    #print "chi2/NDF is",chi2OfFitToData/NDF
    print "chi2 pvalue is",chi2PVal
    print "bump hunter stat of fit to data is",bumpHunterStatFitToData
    print "bumpLowEdge, bumpHighEdge are",bumpLowEdge,bumpHighEdge
    print "BumpHunter pvalue is",bumpHunterPVal
    print "which is Z value of",GetZVal(bumpHunterPVal,True)
    #print "Fitted parameters were:",fitparams

    # Find range
    firstBin = 1000
    lastBin = basicData.GetNbinsX()
    print lastBin
    while (basicData.GetBinContent(lastBin)==0 and lastBin > 0) :
      lastBin = lastBin - 1

    # Calculate from fit range
    fitRange = searchInputFile.Get("FitRange")
    firstBin = basicData.FindBin(fitRange[0])
    lastBin = basicData.FindBin(fitRange[1])
    print "New firstbin, lastbin",firstBin,lastBin

    # Convert plots into desired final form
    standardbins = basicData.GetXaxis().GetXbins()
    newbins = []#ROOT.TArrayD(standardbins.GetSize())
    for np in range(standardbins.GetSize()) :
      newbins.append(standardbins[np]/1000)

    # Make new versions of old plots
    newbasicdata = ROOT.TH1D("basicData_TeV","basicData_TeV",len(newbins)-1,array('d',newbins))
    newbasicBkg = ROOT.TH1D("basicBkg_TeV","basicBkg_TeV",len(newbins)-1,array('d',newbins))
    newresidualHist = ROOT.TH1D("residualHist_TeV","residualHist_TeV",len(newbins)-1,array('d',newbins))
    newrelativeDiffHist = ROOT.TH1D("relativeDiffHist_TeV","relativeDiffHist_TeV",len(newbins)-1,array('d',newbins))
    newsigOfDiffHist = ROOT.TH1D("sigOfDiffHist_TeV","sigOfDiffHist_TeV",len(newbins)-1,array('d',newbins))

    newNomPlus1= ROOT.TH1D("nomPlus1_TeV","nomPlus1_TeV",len(newbins)-1,array('d',newbins))
    newNomMinus1= ROOT.TH1D("nomMinus1_TeV","nomMinus1_TeV",len(newbins)-1,array('d',newbins))

    newAlternateBkg = ROOT.TH1D("alternateBkg_TeV","alternateBkg_TeV",len(newbins)-1,array('d',newbins))
    newnomWithNewFuncErrSymm = ROOT.TH1D("nomWithNewFuncErrSymm_TeV","nomWithNewFuncErrSymm_TeV",len(newbins)-1,array('d',newbins))
    newValueNewFuncErrDirected= ROOT.TH1D("nomWithNewFuncErrDirected_TeV","nomWithNewFuncErrDirected_TeV",len(newbins)-1,array('d',newbins))

    for histnew,histold in [[newbasicdata,basicData],[newbasicBkg,basicBkg],\
                            [newNomPlus1,nomPlus1],[newNomMinus1,nomMinus1], \
                            [newresidualHist,residualHist],[newrelativeDiffHist,relativeDiffHist],\
                            [newsigOfDiffHist,sigOfDiffHist]] :
      for bin in range(histnew.GetNbinsX()+2) :
        histnew.SetBinContent(bin,histold.GetBinContent(bin))
        histnew.SetBinError(bin,histold.GetBinError(bin))
 
    if doAlternate:
      icount=0
      for histnew,histold in [[newAlternateBkg,alternateBkg], [newnomWithNewFuncErrSymm,nomWithNewFuncErrSymm],\
                              [newValueNewFuncErrDirected,valueNewFuncErrDirected]] :
     
        print "Count : ",icount
        print histnew.GetName()
        print histold.GetName()
        icount+=1
      
        for bin in range(histnew.GetNbinsX()+2) :
          histnew.SetBinContent(bin,histold.GetBinContent(bin))
          histnew.SetBinError(bin,histold.GetBinError(bin))

    # Significances for Todd
    ToddSignificancesHist = ROOT.TH1D("ToddSignificancesHist","ToddSignificancesHist",100,-5,5)
    for bin in range(0,newresidualHist.GetNbinsX()+1):
      if bin < firstBin: continue
      if bin > lastBin: continue
      residualValue = newresidualHist.GetBinContent(bin)
      ToddSignificancesHist.Fill(residualValue)

    # Search phase plots
    myPainter.drawDataAndFitOverSignificanceHist(newbasicdata,newbasicBkg,newresidualHist, 'm_{jj} [TeV]','Events','Significance','{0}/figure1'.format(outPath), luminosity,13,fitRange[0],fitRange[1], firstBin,lastBin,True,bumpLowEdge/1000.0,bumpHighEdge/1000.0,[],True,False,[],True,bumpHunterPVal)
    myPainter.drawDataAndFitOverSignificanceHist(newbasicdata,newbasicBkg,newresidualHist, 'm_{jj} [TeV]','Events','Significance','{0}/figure1_nologx'.format(outPath), luminosity,13,fitRange[0],fitRange[1], firstBin,lastBin,True,bumpLowEdge/1000.0,bumpHighEdge/1000.0,[],False,False,[],True,bumpHunterPVal)
    myPainter.drawDataAndFitOverSignificanceHist(newbasicdata,newbasicBkg,newresidualHist, 'm_{jj} [TeV]','Events','Significance','{0}/figure1_nobump'.format(outPath), luminosity,13,fitRange[0],fitRange[1],firstBin,lastBin+2,False,bumpLowEdge,bumpHighEdge,[],True,False,[],True,bumpHunterPVal)
    myPainter.drawDataAndFitOverSignificanceHist(newbasicdata,newbasicBkg,newresidualHist, 'm_{jj} [TeV]','Events','Significance','{0}/figure1_nobump_nologx'.format(outPath), luminosity,13,fitRange[0],fitRange[1],firstBin,lastBin,False,bumpLowEdge,bumpHighEdge,[],False,False,[],True,bumpHunterPVal)
    myPainter.drawPseudoExperimentsWithObservedStat(logLikelihoodPseudoStatHist,float(logLOfFitToData),logLPVal,0,luminosity,13, 'logL statistic','Pseudo-exeperiments',"{0}/logLStatPlot".format(outPath))
    myPainter.drawPseudoExperimentsWithObservedStat(chi2PseudoStatHist,float(chi2OfFitToData),chi2PVal,0,luminosity,13, "#chi^{2}",'Pseudo-exeperiments',"{0}/chi2StatPlot".format(outPath))
    myPainter.drawPseudoExperimentsWithObservedStat(bumpHunterStatHist,float(bumpHunterStatFitToData),bumpHunterPVal,0,luminosity,13, 'BumpHunter','Pseudo-exeperiments',"{0}/bumpHunterStatPlot".format(outPath))
    myPainter.drawBumpHunterTomographyPlot(bumpHunterTomographyPlot,"{0}/bumpHunterTomographyPlot".format(outPath))

    # Various significance plots
    myPainter.drawBasicHistogram(ToddSignificancesHist,-1,-1,"Residuals","Entries","{0}/ToddSignificancesHist".format(outPath))
    myPainter.drawSignificanceHistAlone(newrelativeDiffHist,"m_{jj} [TeV]","(D - B)/B","{0}/significanceonlyplot".format(outPath))
    myPainter.drawSignificanceHistAlone(newsigOfDiffHist,"m_{jj} [TeV]","(D - B)/#sqrt{Derr^{2}+Berr^{2}}","{0}/sigofdiffonlyplot".format(outPath))

    # Now to make the one comparing uncertainties
    placeHolderNom = newbasicBkg.Clone()
    placeHolderNom.SetName("placeHolderNom")
    nomPlusSymmFuncErr = newbasicBkg.Clone()
    nomPlusSymmFuncErr.SetName("nomPlusNewFuncErr")
    nomMinusSymmFuncErr = newbasicBkg.Clone()
    nomMinusSymmFuncErr.SetName("nomMinusNewFuncErr")
    for bin in range(nomPlusSymmFuncErr.GetNbinsX()+2) :
      nomPlusSymmFuncErr.SetBinContent(bin,newnomWithNewFuncErrSymm.GetBinContent(bin) + newnomWithNewFuncErrSymm.GetBinError(bin))
      nomMinusSymmFuncErr.SetBinContent(bin,newnomWithNewFuncErrSymm.GetBinContent(bin) - newnomWithNewFuncErrSymm.GetBinError(bin))

    if doAlternate:
      myPainter.drawDataWithFitAsHistogram(newbasicdata,newbasicBkg,luminosity,13,"m_{jj} [TeV]","Events",["Data","Fit","Fit uncertainty","Function choice"],"{0}/compareFitQualityAndAlternateFit".format(outPath),True,[[newNomPlus1,newNomMinus1],[placeHolderNom,newAlternateBkg]],firstBin,lastBin,True,True,True,False,False)
      myPainter.drawDataWithFitAsHistogram(newbasicdata,newbasicBkg,luminosity,13,"m_{jj} [TeV]","Events",["Data","Fit","Function choice","Alternate function"],"{0}/compareFitChoiceAndAlternateFit".format(outPath),True,[[nomPlusSymmFuncErr,nomMinusSymmFuncErr],[placeHolderNom,newAlternateBkg]],firstBin,lastBin,True,True,True,False,False)
      myPainter.drawDataWithFitAsHistogram(newbasicdata,newbasicBkg,luminosity,13,"m_{jj} [TeV]","Events",["Data","Fit","Fit uncertainty","Function choice"],"{0}/compareFitQualtiyAndFitChoice".format(outPath),True,[[newNomPlus1,newNomMinus1],[nomPlusSymmFuncErr,nomMinusSymmFuncErr]],firstBin,lastBin,True,True,True,False,False)
      myPainter.drawDataWithFitAsHistogram(newbasicdata,newbasicBkg,luminosity,13,"m_{jj} [TeV]","Events",["Data","Fit","Statistical fit uncertainty","Function choice"],"{0}/compareFitQualityAndFitChoice_Asymm".format(outPath),True,[[newNomPlus1,newNomMinus1],[placeHolderNom,newValueNewFuncErrDirected]],firstBin,lastBin,True,True,True,False,False)

      # Overlay nominal and alternate fit functions
      myPainter.drawDataWithFitAsHistogram(newbasicdata,newbasicBkg,luminosity,13,"m_{jj} [TeV]","Events",["Data","Fit","Alternate function"],"{0}/compareFitChoices".format(outPath),True,[[placeHolderNom,newAlternateBkg]],firstBin,lastBin,True,True,True,False,False)

      # Make a ratio histogram for bottom plot.
      altFitRatio = ROOT.TH1D("altFitRatio","altFitRatio",len(newbins)-1,array('d',newbins))
      for bin in range(0,altFitRatio.GetNbinsX()+1) :
        if newbasicBkg.GetBinContent(bin) == 0 :
          altFitRatio.SetBinContent(bin,0)
        else :
          altFitRatio.SetBinContent(bin,(valueNewFuncErrDirected.GetBinContent(bin)-newbasicBkg.GetBinContent(bin))/newbasicBkg.GetBinContent(bin))

      # Make a ratio histogram for paper plot.
      PlusNomRatio = ROOT.TH1D("PlusNomRatio","PlusNomRatio",len(newbins)-1,array('d',newbins))
      for bin in range(0,PlusNomRatio.GetNbinsX()+1) :
        if newbasicBkg.GetBinContent(bin) == 0 :
          PlusNomRatio.SetBinContent(bin,0)
        else :
          PlusNomRatio.SetBinContent(bin,(newNomPlus1.GetBinContent(bin)-newbasicBkg.GetBinContent(bin))/newbasicBkg.GetBinContent(bin))
      MinusNomRatio = ROOT.TH1D("MinusNomRatio","MinusNomRatio",len(newbins)-1,array('d',newbins))
      for bin in range(0,MinusNomRatio.GetNbinsX()+1) :
        if newbasicBkg.GetBinContent(bin) == 0 :
          MinusNomRatio.SetBinContent(bin,0)
        else :
          MinusNomRatio.SetBinContent(bin,(newNomMinus1.GetBinContent(bin)-newbasicBkg.GetBinContent(bin))/newbasicBkg.GetBinContent(bin))

      myPainter.drawDataWithFitAsHistogramAndResidual(newbasicdata,newbasicBkg,luminosity,13,"m_{jj} [TeV]","Events",["Data","Fit","Statistical uncertainty on fit","Function choice"],"{0}/compareFitQualityAndFitChoice_Asymm_WithRatio".format(outPath),True,[[newNomPlus1,newNomMinus1],[placeHolderNom,newValueNewFuncErrDirected]],[altFitRatio,MinusNomRatio,PlusNomRatio],firstBin,lastBin,True,True,True,False,False,True,False,True,bumpHunterPVal,True,fitRange[0],fitRange[1])
     
      myPainter.drawDataWithFitAsHistogramAndResidualPaper(newbasicdata,newbasicBkg,luminosity,13,"m_{jj} [TeV]","Events",["Data","Fit","Statistical uncertainty on fit","Function choice"],"{0}/compareFitQualityAndFitChoice_Asymm_WithRatioPaper".format(outPath),True,[[newNomPlus1,newNomMinus1],[placeHolderNom,newValueNewFuncErrDirected]],[altFitRatio,MinusNomRatio,PlusNomRatio],firstBin,lastBin,True,True,True,False,False)
     
      myPainter.drawMultipleFitsAndResiduals(newbasicdata,[newbasicBkg,newValueNewFuncErrDirected],[altFitRatio],["Nominal fit","Function choice"],"m_{jj} [TeV]","Events",["(alt-nom)/nom"],"{0}/directedFuncChoiceVersusNominal_withRatio".format(outPath),luminosity,13,firstBin,lastBin)

    ####### Draw Signal Template overlaid on Background###########
    if overlaidSignal:
      signalFile = ROOT.TFile.Open(signalFileName, "read")
      if not signalFile:
        print signalFileName, " doesn't exist!!!!"
        return
      # setup signal information
      #signalTitles = {"QStar": "#it{q}*"}
      #signalTypes = ["QStar"]
      #signalsMasses = {"QStar":[4000, 5000]}
      #signalScalingFactors = {"QStar": 0.1}
      #signalAxes = {"QStar": {"X" : "M_{#it{q}*} [GeV]", "Y": "#sigma #times #it{A} #times BR [pb]"} }
      signalTitles = {"DMZprime": "DM #it{Z}'"}
      signalTypes = ["DMZprime"]
      signalsMasses = {"DMZprime":[4000, 5000]}
      signalScalingFactors = {"DMZprime": 1000}
      signalAxes = {"DMZprime": {"X" : "M_{#it{q}*} [GeV]", "Y": "#sigma #times #it{A} #times BR [pb]"} }

      for signalType in signalTypes:
        print "in signal",signalType
        signalMasses = signalsMasses[signalType]
        signalMassesTeV = signalsMasses[signalType][:]
        for index in range(len(signalMasses)) :
          signalMassesTeV[index] = signalMasses[index]/1000.0
        print signalMassesTeV

        signalPlotsTeV = []
        legendlistTeV = []
        for mass in signalMasses :
          #sigplot = signalFile.Get("h_mjj_{0}".format(mass))
          sigplot = signalFile.Get("{0}_{1}".format(signalType, mass))
          sigplot.SetDirectory(0)
          sigplottev = newbasicdata.Clone()
          sigplottev.SetName("sigplot_{0}_{1}_TeV".format(signalType,mass))
          for bins in range(sigplot.GetNbinsX()+2) :
            for bin in range(sigplottev.GetNbinsX()+2) :
              if sigplot.GetBinLowEdge(bins)/1000.==sigplottev.GetBinLowEdge(bin) :
                sigplottev.SetBinContent(bin,sigplot.GetBinContent(bins))
                sigplottev.SetBinError(bin,sigplot.GetBinError(bins))
          sigplotforfitplusbkg = sigplottev.Clone()
          sigplotforfitplusbkg.SetDirectory(0)
          sigplotforfitplusbkg.SetName(sigplottev.GetName()+"_forfitplusbkg_TeV")
          sigplotforfitplusbkg.Scale(signalScalingFactors[signalType])
          signalPlotsTeV.append(sigplotforfitplusbkg)
          thistitle = signalTitles[signalType] + ", {0}= {1} TeV".format(signalAxes[signalType]["X"].split("[GeV]")[0].replace("M","m"),mass/1000.0)
          legendlistTeV.append(thistitle)

          extLastBin = lastBin
          for bin in range(sigplotforfitplusbkg.GetNbinsX()) :
            if bin > extLastBin and sigplotforfitplusbkg.GetBinContent(bin) > 0.01 :
              extLastBin = bin
            if sigplotforfitplusbkg.GetBinLowEdge(bin) > 1.3*mass/1000.0 :
              continue
            if extLastBin < lastBin :
              extLastBin = lastBin

      UserScaleText = signalTitles[signalType]
      if signalScalingFactors[signalType] == 1 :
        UserScaleText = signalTitles[signalType]
      else :
        UserScaleText = UserScaleText+",  #sigma #times "+str(signalScalingFactors[signalType])
      outputName = outPath+"FancyFigure1_"+signalType
      myPainter.drawDataAndFitWithSignalsOverSignificances(newbasicdata,newbasicBkg, None,\
                   newresidualHist,signalPlotsTeV, None, signalMassesTeV,legendlistTeV,\
                   "m_{jj} [TeV]","Events","","Significance ", outputName,luminosity,\
                   Ecm, firstBin,extLastBin,\
                   True, bumpLowEdge/1000,bumpHighEdge/1000,\
                   True,False,True,UserScaleText,True,bumpHunterPVal, True, \
                   fitRange[0], fitRange[1])
      outputName = outPath+"FancyFigure1_"+signalType+"_nologx"
      myPainter.drawDataAndFitWithSignalsOverSignificances(newbasicdata,newbasicBkg, None,\
                   newresidualHist,signalPlotsTeV, None, signalMassesTeV,legendlistTeV,\
                   "m_{jj} [TeV]","Events","","Significance ", outputName,luminosity,\
                   Ecm, firstBin,extLastBin,\
                   True, bumpLowEdge/1000,bumpHighEdge/1000,\
                   False,False,True,UserScaleText,True,bumpHunterPVal, True, \
                   fitRange[0], fitRange[1])
      outputName = outPath+"FancyFigure1_"+signalType+"_noBump"
      myPainter.drawDataAndFitWithSignalsOverSignificances(newbasicdata,newbasicBkg, None,\
                   newresidualHist,signalPlotsTeV, None, signalMassesTeV,legendlistTeV,\
                   "m_{jj} [TeV]","Events","","Significance ", outputName,luminosity,\
                   Ecm, firstBin,extLastBin,\
                   False, bumpLowEdge/1000,bumpHighEdge/1000,\
                   True,False,True,UserScaleText,True,bumpHunterPVal, True, \
                   fitRange[0], fitRange[1])
      outputName = outPath+"FancyFigure1_"+signalType+"_noBump_nologx"
      myPainter.drawDataAndFitWithSignalsOverSignificances(newbasicdata,newbasicBkg, None,\
                   newresidualHist,signalPlotsTeV, None, signalMassesTeV,legendlistTeV,\
                   "m_{jj} [TeV]","Events","","Significance ", outputName,luminosity,\
                   Ecm, firstBin,extLastBin,\
                   False, bumpLowEdge/1000,bumpHighEdge/1000,\
                   False,False,True,UserScaleText,True,bumpHunterPVal, True, \
                   fitRange[0], fitRange[1])

      ###############################
      # Draw the comparison between data and MC in the bottom panel
      if drawMCComparison:
        mcFile = ROOT.TFile(mcFileName, "read") ;
        if not mcFile:
          print "Can not open: ", mcFileName
          return 
        mchist_nominal = mcFile.Get("djet_mjj_nominal")
        mchist_jesup = mcFile.Get("djet_mjj_JES_up")
        mchist_jesdown = mcFile.Get("djet_mjj_JES_down")
        newmchist_nominal=ROOT.TH1D("djet_mjj_nominal_TeV","djet_mjj_nominal_TeV",len(newbins)-1,array('d',newbins))
        newmchist_jesup=ROOT.TH1D("djet_mjj_jesup_TeV","djet_mjj_jesup_TeV",len(newbins)-1,array('d',newbins))
        newmchist_jesdown=ROOT.TH1D("djet_mjj_jesdown_TeV","djet_mjj_jesdown_TeV",len(newbins)-1,array('d',newbins))
        for iBin1 in range(1, newmchist_nominal.GetNbinsX()+1):
          for iBin2 in range(1, mchist_nominal.GetNbinsX()+1):
            if newmchist_nominal.GetBinLowEdge(iBin1)*1000==mchist_nominal.GetBinLowEdge(iBin2):
              newmchist_nominal.SetBinContent(iBin1, mchist_nominal.GetBinContent(iBin2))
              newmchist_nominal.SetBinError(iBin1, mchist_nominal.GetBinError(iBin2))
              continue
        for iBin1 in range(1, newmchist_jesup.GetNbinsX()+1):
          for iBin2 in range(1, mchist_jesup.GetNbinsX()+1):
            if newmchist_jesup.GetBinLowEdge(iBin1)*1000==mchist_jesup.GetBinLowEdge(iBin2):
              newmchist_jesup.SetBinContent(iBin1, mchist_jesup.GetBinContent(iBin2))
              newmchist_jesup.SetBinError(iBin1, mchist_jesup.GetBinError(iBin2))
              continue
        for iBin1 in range(1, newmchist_jesdown.GetNbinsX()+1):
          for iBin2 in range(1, mchist_jesdown.GetNbinsX()+1):
            if newmchist_jesdown.GetBinLowEdge(iBin1)*1000==mchist_jesdown.GetBinLowEdge(iBin2):
              newmchist_jesdown.SetBinContent(iBin1, mchist_jesdown.GetBinContent(iBin2))
              newmchist_jesdown.SetBinError(iBin1, mchist_jesdown.GetBinError(iBin2))
              continue
      
        tmpRatioHist = newbasicdata.Clone()
        tmpRatioHist.SetMarkerColor(ROOT.kBlack)
        tmpRatioHist.Add(newmchist_nominal,-1)
        tmpRatioHist.Divide(newmchist_nominal)
        ## If data is 0 then there should be no ratio drawn
        for iBin in range(1, tmpRatioHist.GetNbinsX()+1):
          if newbasicdata.GetBinContent(iBin) == 0:
            tmpRatioHist.SetBinContent(iBin, 0)
            tmpRatioHist.SetBinError(iBin, 0)

        UpDownRatioHists = []
        if mchist_jesup.GetEntries() >= 0:
          tmpJESRatioHist = newmchist_jesup
          tmpJESRatioHist.Add( newmchist_nominal, -1. )
          tmpJESRatioHist.Divide( newmchist_nominal )
          tmpJESRatioHist.SetMarkerColorAlpha( ROOT.kBlue,0.15)
          tmpJESRatioHist.SetLineColorAlpha( ROOT.kBlue,0.15)
          tmpJESRatioHist.SetFillColorAlpha( ROOT.kBlue, 0.15)
          tmpJESRatioHist.SetFillStyle(1001)
          UpDownRatioHists.append(tmpJESRatioHist)
        if mchist_jesdown.GetEntries() >= 0:
          tmpJESRatioHist = newmchist_jesdown
          tmpJESRatioHist.Add( newmchist_nominal, -1. )
          tmpJESRatioHist.Divide( newmchist_nominal )
          tmpJESRatioHist.SetMarkerColorAlpha( ROOT.kBlue,0.15)
          tmpJESRatioHist.SetLineColorAlpha( ROOT.kBlue,0.15)
          tmpJESRatioHist.SetFillColorAlpha( ROOT.kBlue, 0.15)
          tmpJESRatioHist.SetFillStyle(1001)
          UpDownRatioHists.append(tmpJESRatioHist)
        outputName = outPath+"FancyFigure1_"+signalType+"_WithMCRatio"
        myPainter.drawDataAndFitWithSignalsOverSignificancesWithMCRatio(newbasicdata,newbasicBkg,None,\
                     newresidualHist, signalPlotsTeV, [], signalMassesTeV,legendlistTeV,\
                     "m_{jj} [TeV]","Events","#frac{Data-MC}{MC}","Significance",\
                     outputName,luminosity,Ecm,firstBin,lastBin,True,bumpLowEdge/1000.0,bumpHighEdge/1000.0,\
                     True,False,False, UserScaleText,True,bumpHunterPVal,True,fitRange[0],fitRange[1],\
                     newmchist_nominal,tmpRatioHist,UpDownRatioHists[0],UpDownRatioHists[1])
        outputName = outPath+"FancyFigure1_"+signalType+"_WithMCRatio_nologx"
        myPainter.drawDataAndFitWithSignalsOverSignificancesWithMCRatio(newbasicdata,newbasicBkg,None, \
                     newresidualHist, signalPlotsTeV, [],signalMassesTeV,legendlistTeV, \
                     "m_{jj} [TeV]","Events","#frac{Data-MC}{MC}","Significance",\
                     outputName,luminosity,Ecm,firstBin,lastBin,True,bumpLowEdge/1000.0,bumpHighEdge/1000.0,\
                     False,False,False, UserScaleText,True,bumpHunterPVal,True,fitRange[0],fitRange[1],\
                     newmchist_nominal,tmpRatioHist,UpDownRatioHists[0],UpDownRatioHists[1])

    searchInputFile.Close()
    del searchInputFile

    print "Done."

def GetZVal (p, excess) :
  #the function normal_quantile converts a p-value into a significance,
  #i.e. the number of standard deviations corresponding to the right-tail of 
  #a Gaussian
  if excess :
    zval = ROOT.Math.normal_quantile(1-p,1);
  else :
    zval = ROOT.Math.normal_quantile(p,1);

  return zval

def MakeHistoFromStats(statistics) :

  nentries = len(statistics)
  nBins = int(float(nentries)/10.0)

  maxVal = max(statistics)
  minVal = min(statistics)
  axisrange = maxVal - minVal;

  thismin = minVal-0.05*axisrange;
  thismax = maxVal+0.05*axisrange;

  statPlot = ROOT.TH1D("statPlot","",nBins,thismin,thismax)
  for val in range(len(statistics)) :
    statPlot.Fill(statistics[val])

  return statPlot

# when calling this script
if __name__ == "__main__":
    main()
