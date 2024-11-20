#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /afs/desy.de/user/h/hinzmann/hgcal/el9/CMSSW_13_2_0_pre3/src/Geometry/HGCalTBCommonData/test/python/
cmsenv
echo "Working in /tmp/job$1/"
mkdir /tmp/job$1
cd /tmp/job$1
cmsRun /afs/desy.de/user/h/hinzmann/hgcal/el9/CMSSW_13_2_0_pre3/src/Geometry/HGCalTBCommonData/test/python/testHGCalTB24DESYV2_cfg.py seed=$1
echo "Writing output to /nfs/dust/cms/user/hinzmann/hgcal"
mkdir /nfs/dust/cms/user/hinzmann/hgcal
mkdir /nfs/dust/cms/user/hinzmann/hgcal/job$1
mv *.root /nfs/dust/cms/user/hinzmann/hgcal/job$1
rm -r /tmp/job$1
