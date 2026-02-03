print("import")

from ROOT import gROOT,gStyle,TH1F,TChain,TCanvas,TLegend,TH2F,kLightTemperature
import ROOT
import array, math
#import numpy as np
import os
from math import *
from DataFormats.FWLite import Events, Handle
import pickle
gStyle.SetPalette(kLightTemperature)
gROOT.SetBatch(True)

print("start")

#! /usr/bin/env python         

if __name__=="__main__":

 pointsX=array.array("f",[])
 pointsXErr=array.array("f",[])
 pointsYresponse=array.array("f",[])
 pointsYresponseErr=array.array("f",[])
 pointsYresolution=array.array("f",[])
 pointsYresolutionErr=array.array("f",[])
 
 def layer(id):
   kHGCalLayerOffset = 17
   kHGCalLayerMask = 0x1F
   return ((int(id) >> kHGCalLayerOffset) & kHGCalLayerMask) - (7 if layers<10 else 0) # remove 7 silicon-only layers
 
 #particle="Electron"
 particle="Muon"
 #particle="delay0" #noDigi, delay13, delay15, localTime
 x_offset=0 #cm
 
 scenario="HE-30-Sector"

 sci_trigger=0
 if sci_trigger>0:
   postfix2="_sci_trigger"+str(sci_trigger)
 else:
   postfix2="_no_trigger"
 #postfix2+="_test"
 
 if scenario=="D":
   # D Module
   postfix="random_cosmics_xFlat_yFlat_z400_phiFlat_cos2Theta"
   r_min=153.705 # D-Module
   r_max=183.017 # D-Module
   degree=10
   layerClusters="hgcalLayerClustersHSci"
   layerClusterName="LayerCluster"
   part="HEback"
   layers=9
   y_offset=160 #cm
   z_offset=406.581 #cm (zHGCal6=zHGCalHEmix1)
   z_max=10*15 #cm
   flux=150000 # per hour (60x50x50)
   y_min=-100
   y_max=100
   x_max=50 #cm
   layer_positions=[(1,10,20),(2,25,35),(3,40,50),(4,55,65),(5,70,80),(6,75,85),(7,100,110),(8,115,125),(9,130,140)] # Muon teststand
   only_layercluster_plots=False

 elif scenario=="E":
   # E Module
   postfix="random_cosmics_xFlat60_yFlat200_z400_phiFlat_cos2Theta"
   r_min=183.017 # E-Module
   r_max=217.920 # E-Module
   degree=10
   layerClusters="hgcalLayerClustersHSci"
   layerClusterName="LayerCluster"
   part="HEback"
   layers=9
   y_offset=200 #cm
   z_offset=406.581 #cm (zHGCal6=zHGCalHEmix1)
   z_max=10*15 #cm
   flux=216000 # per hour
   y_min=-50
   y_max=50
   x_max=50 #cm
   layer_positions=[(1,10,20),(2,25,35),(3,40,50),(4,55,65),(5,70,80),(6,75,85),(7,100,110),(8,115,125),(9,130,140)] # Muon teststand
   only_layercluster_plots=False

 elif scenario=="HEback-Sci-Sector":
   # Sector with Sci
   postfix="random_cosmics_"+part+"_sci_xFlat70_yFlat_z400_phiFlat_cos2Theta"
   r_min=41.86 #rMinHGCal6
   r_max=263.45 #rPosV2
   degree=10
   layerClusters="hgcalLayerClustersHSci"
   layerClusterName="LayerCluster"
   layers=14
   y_offset=0 #cm
   z_offset=406.581 #cm (zHGCal6=zHGCalHEmix1)
   z_max=10*15 #cm
   flux=1302000 # per hour
   y_min=0
   y_max=310
   x_max=70 #cm
   layer_positions=[(1,10,20),(2,25,35),(3,40,50),(4,55,65),(5,70,80),(6,75,85),(7,100,110),(8,115,125),(9,130,140)] # Muon teststand
   only_layercluster_plots=True

 elif scenario=="HEback-Sector":
   # Sector with Si+Sci
   postfix="random_cosmics_"+part+"_xFlat70_yFlat_z400_phiFlat_cos2Theta"
   r_min=41.86 #rMinHGCal6
   r_max=263.45 #rPosV2
   degree=10
   layerClusters="hgcalMergeLayerClusters"
   layerClusterName="LayerCluster"
   layers=14
   y_offset=0 #cm
   z_offset=406.581 #cm (zHGCal1=zHGCalEE1=zPosV0)
   z_max=10*15 #cm
   flux=1302000 # per hour
   y_min=0
   y_max=310
   x_max=70 #cm
   layer_positions=[(1,10,20),(2,25,35),(3,40,50),(4,55,65),(5,70,80),(6,75,85),(7,100,110),(8,115,125),(9,130,140)] # Muon teststand
   only_layercluster_plots=True

 elif scenario=="HE-10-Sector":
   # Sector with Si+Sci
   postfix="random_cosmics_he_10deg_xFlat_yFlat_z360_phiFlat_cos2Theta_thrSci0p25_thrSi0p5"
   r_min=41.86 #rMinHGCal6
   r_max=263.45 #rPosV2
   degree=10
   layerClusters="hgcalMergeLayerClusters"
   layerClusterName="Hit"
   layers=21
   y_offset=0 #cm
   z_offset=361.971 #cm (zHGCal2=zHGCalHEsil1)
   z_max=160 #cm
   flux=15000000 # per hour
   y_min=0
   y_max=310
   x_max=70 #cm
   layer_positions=[(1,0,10),(2,10,15),(3,15,20),(4,20,30),(5,30,35),(6,35,40),(7,40,45),
                    (8,45,55),(9,55,60),(10,60,65),(11,65,75),
                    (12,75,80),(13,80,90),(14,90,95),(15,95,105),(16,105,115),(17,115,125),(18,125,130),(19,130,140),(20,140,145),(21,145,155)] # HE
   only_layercluster_plots=True

 elif scenario=="HE-30-Sector":
   # Sector with Si+Sci
   postfix="random_cosmics_he_30deg_xFlat_yFlat_z360_phiFlat_cos2Theta_thrSci0p25_noCluster_time0_son6"
   r_min=41.86 #rMinHGCal6
   r_max=263.45 #rPosV2
   degree=30
   layerClusters="hgcalMergeLayerClusters"
   layerClusterName="Hit"
   part="HEfront"
   layers=21
   y_offset=0 #cm
   z_offset=361.971 #cm (zHGCal2=zHGCalHEsil1)
   z_max=160 #cm
   flux=15000000./3.  # per hour - including 1/3 for timing window efficiency
   y_min=0
   y_max=310
   x_max=100 #cm
   layer_positions=[(1,0,10),(2,10,15),(3,15,20),(4,20,30),(5,30,35),(6,35,40),(7,40,45),
                    (8,45,55),(9,55,60),(10,60,65),(11,65,75),
                    (12,75,80),(13,80,90),(14,90,95),(15,95,105),(16,105,115),(17,115,125),(18,125,130),(19,130,140),(20,140,145),(21,145,155)] # HE
   only_layercluster_plots=True

 elif scenario=="HE-60-Sector":
   # Sector with Si+Sci
   postfix="random_cosmics_he_60deg_xFlat_yFlat_z360_phiFlat_cos2Theta_thrSci0p25_thrSi0p5"
   r_min=41.86 #rMinHGCal6
   r_max=263.45 #rPosV2
   degree=60
   layerClusters="hgcalMergeLayerClusters"
   layerClusterName="Hit"
   layers=21
   y_offset=0 #cm
   z_offset=361.971 #cm (zHGCal2=zHGCalHEsil1)
   z_max=160 #cm
   flux=15000000  # per hour
   y_min=0
   y_max=310
   x_max=140 #cm
   layer_positions=[(1,0,10),(2,10,15),(3,15,20),(4,20,30),(5,30,35),(6,35,40),(7,40,45),
                    (8,45,55),(9,55,60),(10,60,65),(11,65,75),
                    (12,75,80),(13,80,90),(14,90,95),(15,95,105),(16,105,115),(17,115,125),(18,125,130),(19,130,140),(20,140,145),(21,145,155)] # HE
   only_layercluster_plots=True

 elif scenario=="HGCAL-Sector":
   # Sector with Si+Sci
   postfix="random_cosmics_hgcal_xFlat70_yFlat_z400_phiFlat_cos2Theta"
   r_min=41.86 #rMinHGCal6
   r_max=263.45 #rPosV2
   degree=10
   layerClusters="hgcalMergeLayerClusters"
   layerClusterName="Hit"
   layers=47
   y_offset=0 #cm
   z_offset=321.05 #cm (zHGCal1=zHGCalEE1=zPosV0)
   z_max=235 #cm
   flux=1302000 # per hour
   y_min=0
   y_max=310
   x_max=70 #cm
   only_layercluster_plots=True

 else:
   wrongscenario
 
 if flux!=0:
   varlabel="per hour"
   eventlabel="Events per hour"
 else:
   varlabel="per event"
   eventlabel="Fraction of events"

 def inRegion(x,y,z):
    return y>r_min and y<r_max and abs(x)<y*tan(degree/360*2*pi/2) and z>0
  
 simulation_output={}
 for particleEnergy in ([1,1.6,2,3,4,5,5.6] if particle=="Electron" else [5]): #[2,3,4,5,6,7,8,9,10]
  
  version=str(particleEnergy)+"GeV"+particle

  print("start ROOT")
  gROOT.Reset()
  gROOT.SetStyle("Plain")
  gROOT.SetBatch(True)
  gStyle.SetOptStat(0)
  gStyle.SetOptFit(0)
  gStyle.SetTitleOffset(1.2,"Y")
  gStyle.SetTitleOffset(1.3,"Z")
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
  ("LayerCluster_n_vs_layer",0.5,layers+0.5,layers,"recoCaloClusters_"+layerClusters+"__GENSIMDIGIRECO","energy","Layer number",layerClusterName+"s per layer"),
  ("LayerCluster_energy",0,5,100,"recoCaloClusters_"+layerClusters+"__GENSIMDIGIRECO","energy",layerClusterName+" Energy [GeV]",layerClusterName+" "+varlabel),
  ("LayerCluster_x_vs_z",0,z_max,100,"recoCaloClusters_"+layerClusters+"__GENSIMDIGIRECO","x",layerClusterName+" z [cm]",layerClusterName+" x [cm]"),
  ("LayerCluster_y_vs_z",0,z_max,100,"recoCaloClusters_"+layerClusters+"__GENSIMDIGIRECO","y",layerClusterName+" z [cm]",layerClusterName+" y [cm]"),
  ("LayerCluster_y_vs_x",-x_max,x_max,100,"recoCaloClusters_"+layerClusters+"__GENSIMDIGIRECO","y",layerClusterName+" x [cm]",layerClusterName+" y [cm]"),
    ]
  if not only_layercluster_plots:
    histograms+=[
  ("n_LayerClusters",0,100,100,"recoCaloClusters_"+layerClusters+"__GENSIMDIGIRECO","size","Number of "+layerClusterName,"Events"),
  ("LayerCluster_x",-x_max,x_max,100,"recoCaloClusters_"+layerClusters+"__GENSIMDIGIRECO","x",layerClusterName+" x [cm]",layerClusterName+" "+varlabel),
  ("LayerCluster_y",y_min,y_max,100,"recoCaloClusters_"+layerClusters+"__GENSIMDIGIRECO","y",layerClusterName+" y [cm]",layerClusterName+" "+varlabel),
  ("LayerCluster_z",0,z_max,100,"recoCaloClusters_hgcalLayerClustersHSci__GENSIMDIGIRECO","z",layerClusterName+" z [cm]",layerClusterName+" "+varlabel),
  ("LayerCluster_energy_vs_z",0,z_max,100,"recoCaloClusters_"+layerClusters+"__GENSIMDIGIRECO","energy",layerClusterName+" z [cm]","Energy sum per event [GeV]"),
  ("LayerCluster_energy_integral",0,10,100,"recoCaloClusters_"+layerClusters+"__GENSIMDIGIRECO","energy","Reconstructed Energy [GeV]",eventlabel),
  ("n_SimHits",0,1000,100,"PCaloHits_g4SimHits_HGCHits"+part+"_GENSIMDIGIRECO","size","Number of SimHits","Events"),
  ("SimHit_n_vs_layer",0.5,layers+0.5,layers,"PCaloHits_g4SimHits_HGCHits"+part+"_GENSIMDIGIRECO","energy","Layer number","SimHits per layer"),
  ("SimHit_energy",0,0.005,100,"PCaloHits_g4SimHits_HGCHits"+part+"_GENSIMDIGIRECO","energy","SimHit energy [GeV]","Hits "+varlabel),
  ("SimHit_energy_vs_layer",0.5,layers+0.5,layers,"PCaloHits_g4SimHits_HGCHits"+part+"_GENSIMDIGIRECO","energy","Layer number","SimHit energy per layer [GeV]"),
  ("n_Digis",0,100,100,"DetIdHGCSampleHGCDataFramesSorted_mix_HGCDigis"+part+"_GENSIMDIGIRECO","size","Number of Digis","Events"),
  ("Digi_n_vs_layer",0.5,layers+0.5,layers,"DetIdHGCSampleHGCDataFramesSorted_mix_HGCDigis"+part+"_GENSIMDIGIRECO","data","Layer number","Number of Digis per layer"),
  ("Digi_n_integral",-0.5,80.5,81,"DetIdHGCSampleHGCDataFramesSorted_mix_HGCDigis"+part+"_GENSIMDIGIRECO","data","Number of Digis "+varlabel,eventlabel),
  ("Digi_data",0,500,100,"DetIdHGCSampleHGCDataFramesSorted_mix_HGCDigis"+part+"_GENSIMDIGIRECO","data","ADC counts","Hits "+varlabel),
  ("Digi_data_integral",0,4000,200,"DetIdHGCSampleHGCDataFramesSorted_mix_HGCDigis"+part+"_GENSIMDIGIRECO","data","ADC count sum "+varlabel,eventlabel),
  ("Digi_data_vs_layer",0.5,layers+0.5,layers,"DetIdHGCSampleHGCDataFramesSorted_mix_HGCDigis"+part+"_GENSIMDIGIRECO","data","Layer number","ADC counts per layer"),
  ("Digi_dataoutoftime",0,500,100,"DetIdHGCSampleHGCDataFramesSorted_mix_HGCDigis"+part+"_GENSIMDIGIRECO","data","Out-of-time ADC counts","Hits "+varlabel),
  ("Digi_dataoutoftime_vs_layer",0.5,layers+0.5,layers,"DetIdHGCSampleHGCDataFramesSorted_mix_HGCDigis"+part+"_GENSIMDIGIRECO","data","Layer number","Out-of-time ADC counts per layer"),
  ("n_UncalibratedRecHits",0,100,100,"HGCUncalibratedRecHitsSorted_HGCalUncalibRecHit_HGC"+part.replace("HEback","HEB").replace("HEfront","HEF")+"UncalibRecHits_GENSIMDIGIRECO","size","Number of uncalibrated RecHits","Events"),
  ("UncalibratedRecHits_n_vs_layer",0.5,layers+0.5,layers,"HGCUncalibratedRecHitsSorted_HGCalUncalibRecHit_HGC"+part.replace("HEback","HEB").replace("HEfront","HEF")+"UncalibRecHits_GENSIMDIGIRECO","amplitude","Layer number","Number of RecHits per layer"),
  ("UncalibratedRecHits_amplitude",0,100,100,"HGCUncalibratedRecHitsSorted_HGCalUncalibRecHit_HGC"+part.replace("HEback","HEB").replace("HEfront","HEF")+"UncalibRecHits_GENSIMDIGIRECO","amplitude","Number of MIPs","Hits "+varlabel),
  ("UncalibratedRecHits_amplitude_vs_layer",0.5,layers+0.5,layers,"HGCUncalibratedRecHitsSorted_HGCalUncalibRecHit_HGC"+part.replace("HEback","HEB").replace("HEfront","HEF")+"UncalibRecHits_GENSIMDIGIRECO","amplitude","Layer number","Number of MIPs per layer"),
  ("n_RecHits",0,100,100,"HGCRecHits_HGCalRecHit_HGC"+part.replace("HEback","HEB").replace("HEfront","HEF")+"RecHits_GENSIMDIGIRECO","size","Number of calibrated RecHits","Events"),
  ("RecHits_n_vs_layer",0.5,layers+0.5,layers,"HGCRecHits_HGCalRecHit_HGC"+part.replace("HEback","HEB").replace("HEfront","HEF")+"RecHits_GENSIMDIGIRECO","energy","Layer number","Number of RecHits per layer"),
  ("RecHits_energy",0,5,100,"HGCRecHits_HGCalRecHit_HGC"+part.replace("HEback","HEB").replace("HEfront","HEF")+"RecHits_GENSIMDIGIRECO","energy","Calibrated RecHit Energy [GeV]","Hits "+varlabel),
  ("RecHits_energy_vs_layer",0.5,layers+0.5,layers,"HGCRecHits_HGCalRecHit_HGC"+part.replace("HEback","HEB").replace("HEfront","HEF")+"RecHits_GENSIMDIGIRECO","energy","Layer number","Energy sum per layer [GeV]"),
  ("n_MultiClusters",0,10,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","size","Number of MultiClusters","Events"),
  ("MultiCluster_energy",0,5,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","energy","MultiCluster Energy [GeV]","Clusters "+varlabel),
  ("MultiCluster_x",-x_max,x_max,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","x","MultiCluster x [cm]","Cluster "+varlabel),
  ("MultiCluster_y",y_min,y_max,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","y","MultiCluster y [cm]","Clusters "+varlabel),
  ("MultiCluster_z",0,z_max,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","z","MultiCluster z [cm]","Clusters "+varlabel),
  ("MultiCluster_energy_vs_z",0,z_max,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","energy","MultiCluster z [cm]","Energy sum per event [GeV]"),
  ("MultiCluster_theta",-2,2,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","theta","MultiCluster #theta","Clusters "+varlabel),
  ("MultiCluster_phi",0,6.2831,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","phi","MultiCluster #phi","Clusters "+varlabel),
  ("MultiCluster_x_vs_z",0,z_max,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","x","MultiCluster z [cm]","MultiCluster x [cm]"),
  ("MultiCluster_y_vs_z",0,z_max,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","y","MultiCluster z [cm]","MultiCluster y [cm]"),
  ("MultiCluster_y_vs_x",-x_max,x_max,100,"recoHGCalMultiClusters_hgcalMultiClusters__GENSIMDIGIRECO","y","MultiCluster x [cm]","MultiCluster y [cm]"),
    ]

  #histograms=[]
  for l in range(1,layers+1):
    histograms+=[
  ("LayerCluster_y_vs_x_in_layer"+str(l),-x_max,x_max,1000,"recoCaloClusters_"+layerClusters+"__GENSIMDIGIRECO","y",layerClusterName+" x [cm]",layerClusterName+" y [cm]"),
  ("LayerCluster_y_vs_x_rebinned-in_layer"+str(l),-x_max,x_max,1000,"recoCaloClusters_"+layerClusters+"__GENSIMDIGIRECO","y",layerClusterName+" x [cm]",layerClusterName+" y [cm]"),
    ]
    if not only_layercluster_plots:
      histograms+=[
  ("SimHit_n_integral_in_layer"+str(l),0,1000,100,"PCaloHits_g4SimHits_HGCHits"+part+"_GENSIMDIGIRECO","energy","Number of SimHits per layer",eventlabel),
  ("SimHit_energy_integral_in_layer"+str(l),0,0.005,100,"PCaloHits_g4SimHits_HGCHits"+part+"_GENSIMDIGIRECO","energy","SimHit energy sum per layer[GeV]",eventlabel),
  ("Digi_n_integral_in_layer"+str(l),-0.5,40.5,41,"DetIdHGCSampleHGCDataFramesSorted_mix_HGCDigis"+part+"_GENSIMDIGIRECO","data","Number of Digis per layer",eventlabel),
  ("Digi_data_integral_in_layer"+str(l),0,2000,200,"DetIdHGCSampleHGCDataFramesSorted_mix_HGCDigis"+part+"_GENSIMDIGIRECO","data","ADC count sum per layer",eventlabel),
  ("UncalibratedRecHits_n_integral_in_layer"+str(l),0,100,100,"HGCUncalibratedRecHitsSorted_HGCalUncalibRecHit_HGC"+part.replace("HEback","HEB").replace("HEfront","HEF")+"UncalibRecHits_GENSIMDIGIRECO","amplitude","Number of RecHits per layer",eventlabel),
  ("UncalibratedRecHits_amplitude_integral_in_layer"+str(l),0,100,100,"HGCUncalibratedRecHitsSorted_HGCalUncalibRecHit_HGC"+part.replace("HEback","HEB").replace("HEfront","HEF")+"UncalibRecHits_GENSIMDIGIRECO","amplitude","Number of MIP sum per layer",eventlabel),
  ("RecHits_n_integral_in_layer"+str(l),0,100,100,"HGCRecHits_HGCalRecHit_HGC"+part.replace("HEback","HEB").replace("HEfront","HEF")+"RecHits_GENSIMDIGIRECO","energy","Number of RecHits per layer",eventlabel),
  ("RecHits_energy_integral_in_layer"+str(l),0,5,100,"HGCRecHits_HGCalRecHit_HGC"+part.replace("HEback","HEB").replace("HEfront","HEF")+"RecHits_GENSIMDIGIRECO","energy","Calibrated RecHit Energy sum per layer [GeV]",eventlabel),
    ]

  hists={}
  
  files=[]
  #b="/data/dust/user/hinzmann/hgcal"
  #for d in os.listdir(b):
  #  for f in os.listdir(b+"/"+d):
  #     if "gensimdigireco_muon5_"+postfix.replace("_sci","").replace("_10deg","").replace("_30deg","").replace("_60deg","") in f and ".root" in f:
  #       files+=[b+"/"+d+"/"+f]
  b="/data/dust/user/hinzmann/hgcal/he_son6"
  #b="/afs/desy.de/user/h/hinzmann/hgcal/CMSSW_15_1_0_pre5/src"
  for f in os.listdir(b):
       if "gensimdigireco_muon5_"+postfix.replace("_sci","").replace("_10deg","").replace("_30deg","").replace("_60deg","") in f and ".root" in f:
         files+=[b+"/"+f]
  print(files)
  events=TChain("Events")
  #total=0
  for f in files:
    events.Add(f,-1)
    #total+=10
  i=0
  passed_1=0
  passed_3=0
  multihit_1=0
  multihit_3=0
  passed_any_1=0
  passed_any_2=0
  passed_any_3=0
  for event in events:
    if i%100==0 or "test" in postfix2: print("event",i)
    #if i>1000: break
    i+=1
    sci_hits=None
    hits={}
    for l,z1,z2 in layer_positions:
      hits[l]=0
    for name,xmin,xmax,nbins,branch_name,var,xtitle,ytitle in histograms:
      if (not name in hists.keys()) and ("_x_vs_z" in name or "_y_vs_z" in name or "_y_vs_x" in name):
        hists[name]=TH2F(name,name,nbins,xmin,xmax,(1000 if "in_layer" in name else 100),(y_min if "y_vs" in name else -x_max),(y_max if "y_vs" in name else x_max))
      elif not name in hists.keys():
        hists[name]=TH1F(name,name,nbins,xmin,xmax)
      prod=getattr(event,branch_name).product()
      if sci_hits==None and "LayerCluster" in name: # count scintillator hits
        sci_hits=[]
        for p in prod:
         for l,z1,z2 in layer_positions:
           if (getattr(p,"z")()-z_offset)>z1 and (getattr(p,"z")()-z_offset)<z2:
             hits[l]+=1
             if ((int(p.hitsAndFractions()[0][0]) >> 28) & 0xF)==10:
              if not l in sci_hits:
               sci_hits+=[l]
      #if sci_hits!=None: print(sci_hits,[l for l in sci_hits if (l-1 in sci_hits or l-2 in sci_hits) and (l+1 in sci_hits or l+2 in sci_hits)])
      if sci_trigger>0 and (len(sci_hits)<sci_trigger or len([l for l in sci_hits if (l-1 in sci_hits or l-2 in sci_hits) and (l+1 in sci_hits or l+2 in sci_hits)])<sci_trigger-2):
         break
      if var=="size":
        hists[name].Fill(len(prod))
      elif "vs" in name:
        for p in prod:
         if hasattr(p,"x") and not inRegion(getattr(p,"x")(),getattr(p,"y")(),getattr(p,"z")()): continue
         if "_x_vs_z" in name or "_y_vs_z" in name or "_y_vs_x" in name:
           if "in_layer" in name:
             found=False
             for l,z1,z2 in layer_positions:
               if (getattr(p,"z")()-z_offset)>z1 and (getattr(p,"z")()-z_offset)<z2:
                  if l==int(name.split("_")[-1].strip("layer")):
                    found=True
             if not found: continue
           hists[name].Fill(getattr(p,name.split("_")[-1-2*("in_layer" in name)])()-z_offset*("vs_z" in name)-x_offset*("vs_x" in name),getattr(p,var)()-x_offset*("_x_vs" in name)-y_offset*("_y_vs" in name),flux)
         elif "vs_layer" in name:
          if "DetIdHGCSampleHGCDataFramesSorted" in branch_name:
           if "outoftime" in name:
            #print([getattr(p,var)()[i].data() for i in range(5)])
            y=sum([getattr(p,var)()[i].data() if i!=2 else 0 for i in range(5)])
           else:
            y=getattr(p,var)()[2].data() # index 2 of 5 time-samples
          else:
           y=getattr(p,var)()
          if "_n_" in name:
           y=1 if y>0 else 0
          
          if "PCaloHits_g4SimHits_HGCHits"+part+"_GENSIMDIGIRECO" in branch_name:
           l=layer(p.id())
          elif "LayerCluster" in name:
           l=0
           for l0,z1,z2 in layer_positions:
             if (getattr(p,"z")()-z_offset)>z1 and (getattr(p,"z")()-z_offset)<z2:
               l=l0
               break
          else:
           l=layer(p.id().rawId())
          if l>layers: continue
          hists[name].Fill(l,y)
         else: 
           if hasattr(p,"z"):
             z=p.z()
             if z-z_offset>z_max: continue
           x=getattr(p,name.split("_")[-1])()
           if "vs_z" in name:
              x-=z_offset
           hists[name].Fill(x,getattr(p,var)())
        #if ("_x_vs_z" in name or "_y_vs_z" in name) and len(prod)>0:
        #  hists[name].Scale(1./len(prod))
        if name=="LayerCluster_x_vs_z":
         if hits[3] or hits[6] or hits[9]:
          passed_1+=1
         if hits[3] and hits[6] and hits[9]:
          passed_3+=1
         if hits[3]>1 or hits[6]>1 or hits[9]>1:
          multihit_1+=1
         if hits[3]>1 and hits[6]>1 and hits[9]>1:
          multihit_3+=1
         anyhits=0
         for h in hits.keys():
          if hits[h]>0:
            anyhits+=1
         if anyhits>0:
          passed_any_1+=1            
         if anyhits>1:
          passed_any_2+=1            
         if anyhits>2:
          passed_any_3+=1            
      else:
        integral=0
        for p in prod:
         if "data" in var and "DetIdHGCSampleHGCDataFramesSorted" in branch_name:
          if "outoftime" in name:
           x=sum([getattr(p,var)()[i].data() if i!=2 else 0 for i in range(5)])
          else:
           x=getattr(p,var)()[2].data() # index 2 of 5 time-samples
         else:
          x=getattr(p,var)()
         if "_n_" in name:
          x=1 if x>0 else 0

         if hasattr(p,"id"):
           if "PCaloHits_g4SimHits_HGCHits"+part+"_GENSIMDIGIRECO" in branch_name:
             l=layer(p.id())
           else:
             l=layer(p.id().rawId())
           if l>layers: continue
           if "in_layer" in name and str(l)!=name.split("_")[-1].strip("layer"): continue
         if hasattr(p,"z"):
           z=p.z()
           if z-z_offset>z_max: continue
           if not inRegion(getattr(p,"x")(),getattr(p,"y")(),getattr(p,"z")()): continue
         if "_z" in name:
            x-=z_offset
         if "_x" in name:
            x-=x_offset
         if "_y" in name:
            x-=y_offset

         integral+=x
         if not "integral" in name:
          hists[name].Fill(min(xmax-1e-5,x),flux) # make an overflow bin
        if "integral" in name:
         hists[name].Fill(min(xmax-1e-5,integral),flux) # make an overflow bin

  for name,xmin,xmax,nbins,branch_name,var,xtitle,ytitle in histograms:
    print("plotting", name)
    canvas = TCanvas(name+"_", name+"_", 0, 0, 300, 300)

    if not var=="size":
      hists[name].Scale(1./i)
    
    if "_x_vs_z" in name or "_y_vs_z" in name or "_y_vs_x" in name:
      canvas.SetRightMargin(0.20)
      hists[name].Draw("colz")
    else:
      hists[name].Draw("hist")
    hists[name].SetTitle("")
    hists[name].GetXaxis().SetTitle(xtitle)
    hists[name].GetYaxis().SetTitle(ytitle)
    hists[name].GetXaxis().SetRangeUser(xmin,xmax)
    if "_x_vs_z" in name or "_y_vs_z" in name or "_y_vs_x" in name:
      hists[name].GetYaxis().SetRangeUser((y_min if "_y_vs" in name else -x_max),(y_max if "_y_vs" in name else x_max))
      hists[name].GetZaxis().SetTitle(eventlabel)
      #hists[name].GetZaxis().SetRangeUser(0,hists[name].GetMaximum()*1.1)
      canvas.SetLogz()
      if "in_layer" in name and "rebinned" in name:
        hists[name].GetZaxis().SetTitle(eventlabel+" per channel")
        minbin1={}
        maxbin1={}
        minbin2=-1
        maxbin2=0
        rebinfactor=20
        for b2 in range(hists[name].GetNbinsY()):
         if not (int(b2/rebinfactor)) in minbin1.keys(): minbin1[int(b2/rebinfactor)]=-1
         if not (int(b2/rebinfactor)) in maxbin1.keys(): maxbin1[int(b2/rebinfactor)]=0
         for b1 in range(hists[name].GetNbinsX()):
          if hists[name].GetBinContent(b1+1,b2+1)>0:
           if minbin2==-1: minbin2=b2
           maxbin2=b2
           if minbin1[int(b2/rebinfactor)]==-1 or b1<minbin1[int(b2/rebinfactor)]: minbin1[int(b2/rebinfactor)]=b1
           if b1>maxbin1[int(b2/rebinfactor)]: maxbin1[int(b2/rebinfactor)]=b1
        lastbin={}
        for b2 in range(minbin2,maxbin2+1):
         for b1 in range(minbin1[int(b2/rebinfactor)],maxbin1[int(b2/rebinfactor)]+1):
           if hists[name].GetBinContent(b1+1,b2+1)>0:
             lastbin[int(b1/rebinfactor)]=hists[name].GetBinContent(b1+1,b2+1)
           elif int(b1/rebinfactor) in lastbin.keys():
             hists[name].SetBinContent(b1+1,b2+1,lastbin[int(b1/rebinfactor)])
        hists[name].Rebin2D(rebinfactor,rebinfactor)
        hists[name].Scale(1./rebinfactor/rebinfactor)
      hists[name].GetZaxis().SetRangeUser(1,(3000 if "in_layer" in name else hists[name].GetMaximum()*1.1))
    else:
      hists[name].GetYaxis().SetRangeUser(0,hists[name].GetMaximum()*1.1)
   
    l=TLegend(0.2,0.88,0.9,0.9,str(particleEnergy)+" GeV "+particle)
    l.SetFillStyle(0)
    l.SetTextSize(0.05)
    l.Draw("same")
    l2=TLegend(0.6,0.8,0.9,0.9,"Integral: {:.2f}".format(hists[name].Integral()))
    l2.SetFillStyle(0)
    l2.SetTextSize(0.05)
    if not ("_x_vs_z" in name or "_y_vs_z" in name or "_y_vs_x" in name):
      l2.Draw("same")
    prob=array.array('d',[0.5,0.34,0.68])
    q=array.array('d',[0,0,0])
    if not ("_x_vs_z" in name or "_y_vs_z" in name or "_y_vs_x" in name):
      hists[name].GetQuantiles(3,q,prob)
    l4=TLegend(0.6,0.75,0.9,0.8,"Median: {:.2f}".format(q[0]))
    l4.SetFillStyle(0)
    l4.SetTextSize(0.05)
    if not ("_x_vs_z" in name or "_y_vs_z" in name or "_y_vs_x" in name):
      l4.Draw("same")
    if "in_layer" in name:
      l3=TLegend(0.55,0.88,0.9,0.9,"Layer: "+name.split("_")[-1].strip("layer"))
      l3.SetFillStyle(0)
      l3.SetTextSize(0.05)
      l3.Draw("same")
    if not ("_x_vs_z" in name or "_y_vs_z" in name or "_y_vs_x" in name):
      simulation_output["legend"]=("Integral","Mean","RMS","Median","34% quantile", "68% quantile", "bin edges", "bin content")
      simulation_output[name+"_"+version]=(hists[name].Integral(),hists[name].GetMean(),hists[name].GetStdDev(),q[0],q[1],q[2],
      [hists[name].GetBinLowEdge(b+1) for b in range(hists[name].GetNbinsX())]+[hists[name].GetBinLowEdge(hists[name].GetNbinsX()-1)+hists[name].GetBinWidth(hists[name].GetNbinsX()-1)],
      [hists[name].GetBinContent(b+1) for b in range(hists[name].GetNbinsX())]+[hists[name].GetBinContent(hists[name].GetNbinsX()-1)])

  #// writing the lumi information and the CMS "logo"
  #CMS_lumi( c, iPeriod, iPos );
    
    canvas.SaveAs(name+"_"+version+"_"+postfix+postfix2+".pdf")
    canvas.SaveAs(name+"_"+version+"_"+postfix+postfix2+".root")
    
    #if "LayerCluster_energy_integral" in name:
    if "Digi_data_integral" in name and not "layer" in name:
       pointsX.append(particleEnergy)
       pointsXErr.append(0)
       pointsYresponse.append(hists[name].GetMean())
       pointsYresponseErr.append(hists[name].GetMeanError())
       pointsYresolution.append(hists[name].GetStdDev()/hists[name].GetMean()*100.)
       pointsYresolutionErr.append(hists[name].GetStdDevError()/hists[name].GetMean()*100.)

  total=float(i) # account for missing files
  if layers==9:
    print(i,"events", f'{100*passed_1/total:.4}',"% passed 1 layer, ", f'{100*passed_3/total:.4}',"% passed 3 layers", f'{100*multihit_3/total:.4}',"% have multihit")
    print(f'{passed_1/total*flux:.0f}',"% passed 1 layer, ", f'{passed_3/total*flux:.0f}',"% passed 3 layers")
  print(i,"events", f'{100*passed_any_1/total:.4}',"% passed any 1 layer, ", f'{100*passed_any_2/total:.4}',"% passed any 2 layers, ", f'{100*passed_any_3/total:.4}',"% passed any 3 layers")
  print(f'{passed_any_1/total*flux:.0f}',"% passed any 1 layer, ", f'{passed_any_2/total*flux:.0f}',"% passed any 2 layers, ", f'{passed_any_3/total*flux:.0f}',"% passed any 3 layers")

 #print(simulation_output)
 with open('simulation_output.pkl', 'wb') as f:
    pickle.dump(simulation_output, f)

if len(pointsX)>1:
  canvas = TCanvas("Energy_reconstruction_response", "Energy_reconstruction_response", 0, 0, 300, 300)
  g=TGraphErrors(len(pointsX),pointsX,pointsYresponse,pointsXErr,pointsYresponseErr)
  g.SetMarkerColor(1)
  g.SetMarkerSize(1)
  g.SetLineWidth(2)
  g.SetMarkerStyle(24)
  g.Draw("ap")
  f=TF1("fit","pol1")
  g.Fit(f,"")
  f.Draw("lsame")
  g.SetTitle("")
  g.GetXaxis().SetTitle("Beam energy [GeV]")
  #g.GetYaxis().SetTitle("Reconstructed energy [GeV]")
  g.GetYaxis().SetTitle("ADC count sum")
  canvas.SaveAs("Energy_reconstruction_response_"+postfix+postfix2+".pdf")
  #canvas.SaveAs("Energy_reconstruction_response_"+postfix+postfix2+".root")

  canvas = TCanvas("Energy_reconstruction_resolution", "Energy_reconstruction_resolution", 0, 0, 300, 300)
  g=TGraphErrors(len(pointsX),pointsX,pointsYresolution,pointsXErr,pointsYresolutionErr)
  g.SetMarkerColor(1)
  g.SetMarkerSize(1)
  g.SetLineWidth(2)
  g.SetMarkerStyle(24)
  g.Draw("apl")
  g.SetTitle("")
  g.GetXaxis().SetTitle("Beam energy [GeV]")
  g.GetYaxis().SetTitle("Energy resolution [%]")
  canvas.SaveAs("Energy_reconstruction_resolution_"+postfix+postfix2+".pdf")
  #canvas.SaveAs("Energy_reconstruction_resolution_"+postfix+postfix2+".root")
