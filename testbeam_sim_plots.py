from ROOT import *
import ROOT
import array, math
import os
from math import *
from DataFormats.FWLite import Events, Handle

#! /usr/bin/env python         

if __name__=="__main__":

 pointsX=array.array("f",[])
 pointsY=array.array("f",[])
 
 def layer(id):
   kHGCalLayerOffset = 17
   kHGCalLayerMask = 0x1F
   return (int(id) >> kHGCalLayerOffset) & kHGCalLayerMask
 
 #for particleEnergy in [2,3,4,5,7,8,9,10]:
 for particleEnergy in [5]:
  
  particle="Muon"
  version=str(particleEnergy)+"GeV"+particle

  print("start ROOT")
  gROOT.Reset()
  gROOT.SetStyle("Plain")
  gROOT.SetBatch()
  gStyle.SetOptStat(0)
  gStyle.SetOptFit(0)
  gStyle.SetTitleOffset(1.2,"Y")
  gStyle.SetPadLeftMargin(0.16)
  gStyle.SetPadBottomMargin(0.16)
  gStyle.SetPadTopMargin(0.05)
  gStyle.SetPadRightMargin(0.05)
  gStyle.SetMarkerSize(2.5)
  gStyle.SetHistLineWidth(1)
  gStyle.SetStatFontSize(0.020)
  gStyle.SetTitleSize(0.06, "XYZ")
  gStyle.SetLabelSize(0.05, "XYZ")
  gStyle.SetNdivisions(505, "XYZ")
  gStyle.SetLegendBorderSize(0)
  gStyle.SetPadTickX(1)
  gStyle.SetPadTickY(1)
  gStyle.SetEndErrorSize(5)

  #print "start CMS_lumi"

  #gROOT.LoadMacro("CMS_lumi.C");
  #iPeriod = 4;       #// 1=7TeV, 2=8TeV, 3=7+8TeV, 7=7+8+13TeV 
  #iPos = 11;
    
  histograms=[
  ("n_SimHits",0,1000,100,"PCaloHits_g4SimHits_HGCHitsHEback_GENSIMDIGIRECO","size","Number of SimHits","Events"),
  ("SimHit_n_vs_layer",0,35,36,"PCaloHits_g4SimHits_HGCHitsHEback_GENSIMDIGIRECO","n","Layer number","SimHits per layer"),
  ("SimHit_energy",0,0.01,100,"PCaloHits_g4SimHits_HGCHitsHEback_GENSIMDIGIRECO","energy","SimHit energy [GeV]","Hits per event"),
  ("SimHit_energy_vs_layer",0,35,36,"PCaloHits_g4SimHits_HGCHitsHEback_GENSIMDIGIRECO","energy","Layer number","SimHit energy per layer [GeV]"),
  #("n_DigisNano",0,100,100,"nanoaodFlatTable_hgcDigiHEbackTable__GENSIMDIGIRECO","size","Number of Digis","Events"),
  #("DigiNano_data",0,500,100,"nanoaodFlatTable_hgcDigiHEbackTable__GENSIMDIGIRECO","data","ADC counts","Hits per event"),
  ("n_Digis",0,100,100,"DetIdHGCSampleHGCDataFramesSorted_mix_HGCDigisHEback_GENSIMDIGIRECO","size","Number of Digis","Events"),
  ("Digi_n_vs_layer",0,35,36,"DetIdHGCSampleHGCDataFramesSorted_mix_HGCDigisHEback_GENSIMDIGIRECO","n","Layer number","Number of Digis per layer"),
  ("Digi_data",0,500,100,"DetIdHGCSampleHGCDataFramesSorted_mix_HGCDigisHEback_GENSIMDIGIRECO","data","ADC counts","Hits per event"),
  ("Digi_data_vs_layer",0,35,36,"DetIdHGCSampleHGCDataFramesSorted_mix_HGCDigisHEback_GENSIMDIGIRECO","data","Layer number","ADC counts per layer"),
  ("n_UncalibratedRecHits",0,100,100,"HGCUncalibratedRecHitsSorted_HGCalUncalibRecHit_HGCHEBUncalibRecHits_GENSIMDIGIRECO","size","Number of uncalibrated RecHits","Events"),
  ("UncalibratedRecHits_n_vs_layer",0,35,36,"HGCUncalibratedRecHitsSorted_HGCalUncalibRecHit_HGCHEBUncalibRecHits_GENSIMDIGIRECO","n","Layer number","Number of RecHits per layer"),
  ("UncalibratedRecHits_amplitude",0,100,100,"HGCUncalibratedRecHitsSorted_HGCalUncalibRecHit_HGCHEBUncalibRecHits_GENSIMDIGIRECO","amplitude","Number of MIPs","Hits per event"),
  ("UncalibratedRecHits_amplitude_vs_layer",0,35,36,"HGCUncalibratedRecHitsSorted_HGCalUncalibRecHit_HGCHEBUncalibRecHits_GENSIMDIGIRECO","amplitude","Layer number","Number of MIPs per layer"),
  ("n_RecHits",0,100,100,"HGCRecHitsSorted_HGCalRecHit_HGCHEBRecHits_GENSIMDIGIRECO","size","Number of calibrated RecHits","Events"),
  ("RecHits_n_vs_layer",0,35,36,"HGCRecHitsSorted_HGCalRecHit_HGCHEBRecHits_GENSIMDIGIRECO","n","Layer number","Number of RecHits per layer"),
  ("RecHits_energy",0,5,100,"HGCRecHitsSorted_HGCalRecHit_HGCHEBRecHits_GENSIMDIGIRECO","energy","Calibrated RecHit Energy [GeV]","Hits per event"),
  ("RecHits_energy_vs_layer",0,35,36,"HGCRecHitsSorted_HGCalRecHit_HGCHEBRecHits_GENSIMDIGIRECO","energy","Layer number","Energy sum per layer [GeV]"),
  ("n_LayerClusters",0,100,100,"recoCaloClusters_hgcalLayerClustersHSci__GENSIMDIGIRECO","size","Number of LayerClusters","Events"),
  ("LayerCluster_energy",0,5,100,"recoCaloClusters_hgcalLayerClustersHSci__GENSIMDIGIRECO","energy","LayerCluster Energy [GeV]","Clusters per event"),
  ("LayerCluster_x",-100,100,100,"recoCaloClusters_hgcalLayerClustersHSci__GENSIMDIGIRECO","x","LayerCluster x [cm]","Clusters per event"),
  ("LayerCluster_y",0,200,100,"recoCaloClusters_hgcalLayerClustersHSci__GENSIMDIGIRECO","y","LayerCluster y [cm]","Clusters per event"),
  ("LayerCluster_z",400,550,100,"recoCaloClusters_hgcalLayerClustersHSci__GENSIMDIGIRECO","z","LayerCluster z [cm]","Clusters per event"),
  ("LayerCluster_energy_vs_z",400,550,100,"recoCaloClusters_hgcalLayerClustersHSci__GENSIMDIGIRECO","energy","LayerCluster z [cm]","Energy sum per event [GeV]"),
  ("LayerCluster_x_vs_z",400,550,100,"recoCaloClusters_hgcalLayerClustersHSci__GENSIMDIGIRECO","x","LayerCluster z [cm]","Average |x| per cluster"),
  ("LayerCluster_y_vs_z",400,550,100,"recoCaloClusters_hgcalLayerClustersHSci__GENSIMDIGIRECO","y","LayerCluster z [cm]","Average |y| per cluster"),
  ("n_MultiClusters",0,10,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","size","Number of MultiClusters","Events"),
  ("MultiCluster_energy",0,5,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","energy","MultiCluster Energy [GeV]","Clusters per event"),
  ("MultiCluster_x",-100,100,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","x","MultiCluster x [cm]","Cluster per events"),
  ("MultiCluster_y",0,200,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","y","MultiCluster y [cm]","Clusters per event"),
  ("MultiCluster_z",400,550,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","z","MultiCluster z [cm]","Clusters per event"),
  ("MultiCluster_energy_vs_z",400,550,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","energy","MultiCluster z [cm]","Energy sum per event [GeV]"),
  ("MultiCluster_x_vs_z",400,550,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","x","MultiCluster z [cm]","Average |x| per cluster"),
  ("MultiCluster_y_vs_z",400,550,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","y","MultiCluster z [cm]","Average |y| per cluster"),
    ]
  hists={}
  
  for name,xmin,xmax,nbins,branch_name,var,xtitle,ytitle in histograms:
    canvas = TCanvas(name+"_", name+"_", 0, 0, 300, 300)
    hists[name]=TH1F(name,name,nbins,xmin,xmax)
    events=TChain("Events")
    events.Add("gensimdigireco_"+particle.lower().replace("electron","")+str(particleEnergy)+".root")
    for event in events:
      prod=getattr(event,branch_name).product()
      if var=="size":
        hists[name].Fill(len(prod))
      elif "nanoaod" in branch_name:
        for c in range(prod.nColumns()):
          if var==prod.columnName(c):
            for r in range(prod.nRows()):
              hists[name].Fill(prod.getAnyValue(r,c))
      elif "vs" in name:
        for p in prod:
         if "_x_vs_z" in name or "_y_vs_z" in name:
           hists[name].Fill(getattr(p,name.split("_")[-1])(),abs(getattr(p,var)()-160.*("_y_vs_z" in name)))
         elif "vs_layer" in name:
          if "n_vs_layer" in name:
           y=1
          elif "DetIdHGCSampleHGCDataFramesSorted" in branch_name:
           y=getattr(p,var)()[2].data() # index 2 of 5 time-samples
          else:
           y=getattr(p,var)()
          if "PCaloHits_g4SimHits_HGCHitsHEback_GENSIMDIGIRECO" in branch_name:
           x=layer(p.id())
          else:
           x=layer(p.id().rawId())
          hists[name].Fill(x,y)
         else: 
           hists[name].Fill(getattr(p,name.split("_")[-1])(),getattr(p,var)())
        if ("_x_vs_z" in name or "_y_vs_z" in name) and len(prod)>0:
          hists[name].Scale(1./len(prod))
      else:
        for p in prod:
         if "data" in name and "DetIdHGCSampleHGCDataFramesSorted" in branch_name:
          hists[name].Fill(getattr(p,var)()[2].data()) # index 2 of 5 time-samples
         else:
          hists[name].Fill(getattr(p,var)())
    if not var=="size":
      hists[name].Scale(1./events.GetEntries())
        
    hists[name].Draw("hist")
    hists[name].SetTitle("")
    hists[name].GetXaxis().SetTitle(xtitle)
    hists[name].GetYaxis().SetTitle(ytitle)
    hists[name].GetXaxis().SetRangeUser(xmin,xmax)
    #hists[name].GetYaxis().SetRangeUser(0.0005,1)
    
    l=TLegend(0.6,0.88,0.9,0.9,str(particleEnergy)+" GeV "+particle)
    l.SetFillStyle(0)
    l.SetTextSize(0.05)
    l.Draw("same")
    l2=TLegend(0.6,0.8,0.9,0.9,"Integral: {:.2f}".format(hists[name].Integral()))
    l2.SetFillStyle(0)
    l2.SetTextSize(0.05)
    l2.Draw("same")

  #// writing the lumi information and the CMS "logo"
  #CMS_lumi( c, iPeriod, iPos );
    
    canvas.SaveAs(name+"_"+version+".pdf")
    
    if "energy_vs_z" in name:
       pointsX.append(particleEnergy)
       pointsY.append(hists[name].Integral())

 canvas = TCanvas("Energy_reconstruction_linearity", "Energy_reconstruction_linearity", 0, 0, 300, 300)
 g=TGraph(len(pointsX),pointsX,pointsY)
 g.SetMarkerColor(1)
 g.SetMarkerSize(1)
 g.SetLineWidth(2)
 g.Draw("apl")
 g.SetTitle("")
 g.GetXaxis().SetTitle("Beam energy [GeV]")
 g.GetYaxis().SetTitle("Reconstructed energy [GeV]")
 canvas.SaveAs("Energy_reconstruction_linearity.pdf")
