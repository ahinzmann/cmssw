import FWCore.ParameterSet.Config as cms

from CommonTools.PileupAlgos.Puppi_cff import *
from CommonTools.PileupAlgos.PhotonPuppi_cff        import setupPuppiPhoton,setupPuppiPhotonMiniAOD

def makePuppies( process ):
    
    process.load('CommonTools.PileupAlgos.Puppi_cff')
    process.puppiNoLep = process.puppi.clone()
    process.puppiNoLep.noLepPdgIds = cms.vint32(11,13)
    process.load('CommonTools.PileupAlgos.PhotonPuppi_cff')
    process.puppiForMET = process.puppiPhoton.clone()
    #Line below points puppi MET to puppi no lepton which increases the response
    process.puppiForMET.puppiCandName    = 'puppiNoLep'


def makePuppiesFromMiniAOD( process, createScheduledSequence=False ):
    process.load('CommonTools.PileupAlgos.Puppi_cff')
    process.puppi.candName = cms.InputTag('packedPFCandidates')
    process.puppi.clonePackedCands = cms.bool(True)
    process.puppi.vertexName = cms.InputTag('offlineSlimmedPrimaryVertices')
    process.puppiNoLep = process.puppi.clone()
    process.puppiNoLep.noLepPdgIds = cms.vint32(11,13)
    process.puppiNoLep.useWeightsNoLep = cms.bool(True)
    process.load('CommonTools.PileupAlgos.PhotonPuppi_cff')
    process.puppiForMET = process.puppiPhoton.clone()
    process.puppiForMET.candName = cms.InputTag('packedPFCandidates')
    process.puppiForMET.photonName = cms.InputTag('slimmedPhotons')
    process.puppiForMET.runOnMiniAOD = cms.bool(True)
    setupPuppiPhotonMiniAOD(process)
    #Line below points puppi MET to puppi no lepton which increases the response
    process.puppiForMET.puppiCandName    = 'puppiNoLep'
    #Avoid recomputing the weights available in MiniAOD
    process.puppi.useExistingWeights = True
    process.puppiNoLep.useExistingWeights = True

    #making a sequence for people running the MET tool in scheduled mode
    if createScheduledSequence:
        puppiMETSequence = cms.Sequence(process.puppi*process.pfLeptonsPUPPET*process.pfNoLepPUPPI*process.puppiNoLep*process.puppiMerged*process.puppiForMET)
        setattr(process, "puppiMETSequence", puppiMETSequence)
