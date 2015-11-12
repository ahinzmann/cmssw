## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *
## switch to uncheduled mode
process.options.allowUnscheduled = cms.untracked.bool(True)
#process.Tracer = cms.Service('Tracer')

process.load("PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff")

# An example where the jet correction are reapplied
process.patJetCorrFactorsReapplyJEC = process.patJetCorrFactorsUpdated.clone(
  src = cms.InputTag("slimmedJets"),
  levels = ['L1FastJet', 
        'L2Relative', 
        'L3Absolute'] )
process.patJetsReapplyJEC = process.patJetsUpdated.clone(
  jetSource = cms.InputTag("slimmedJets"),
  jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
  )
process.patJetsReapplyJEC.userData.userFloats.src = []
process.out.outputCommands += ['keep *_patJetsReapplyJEC_*_*']

####################################################################################################
#THE JET TOOLBOX

#load the various tools

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#pileupJetID

process.load('RecoJets.JetProducers.PileupJetID_cfi')

process.pileupJetIdCalculator.jets = cms.InputTag("slimmedJets")
process.pileupJetIdEvaluator.jets = cms.InputTag("slimmedJets")
process.pileupJetIdCalculator.inputIsCorrected = True
process.pileupJetIdEvaluator.inputIsCorrected = True
process.pileupJetIdCalculator.vertexes = cms.InputTag("offlineSlimmedPrimaryVertices")
process.pileupJetIdEvaluator.vertexes = cms.InputTag("offlineSlimmedPrimaryVertices")

process.patJetsReapplyJEC.userData.userFloats.src += ['pileupJetIdEvaluator:fullDiscriminant']
process.patJetsReapplyJEC.userData.userInts.src += ['pileupJetIdEvaluator:cutbasedId','pileupJetIdEvaluator:fullId']
process.out.outputCommands += ['keep *_pileupJetIdEvaluator_*_*']

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#QGTagger

process.load('RecoJets.JetProducers.QGTagger_cfi')
process.QGTagger.srcJets = cms.InputTag("slimmedJets")
process.QGTagger.srcVertexCollection = cms.InputTag("offlineSlimmedPrimaryVertices")
process.patJetsReapplyJEC.userData.userFloats.src += ['QGTagger:qgLikelihood']
process.out.outputCommands += ['keep *_QGTagger_*_*']


####################################################################################################

## ------------------------------------------------------
#  In addition you usually want to change the following
#  parameters:
## ------------------------------------------------------
#
#   process.GlobalTag.globaltag =  ...    ##  (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')
#                                         ##
from PhysicsTools.PatAlgos.patInputFiles_cff import filesRelValProdTTbarAODSIM
#process.source.fileNames = cms.untracked.vstring('/store/relval/CMSSW_7_6_0/RelValTTbar_13/GEN-SIM-RECO/PUpmx25ns_76X_mcRun2_asymptotic_v11_gs7120p2rlBS-v1/00000/0CD8CEBC-D983-E511-ACC9-0025905A60CA.root',
#       '/store/relval/CMSSW_7_6_0/RelValTTbar_13/GEN-SIM-RECO/PUpmx25ns_76X_mcRun2_asymptotic_v11_gs7120p2rlBS-v1/00000/A044CADA-BA83-E511-A7E1-0025905938A8.root',
#       '/store/relval/CMSSW_7_6_0/RelValTTbar_13/GEN-SIM-RECO/PUpmx25ns_76X_mcRun2_asymptotic_v11_gs7120p2rlBS-v1/00000/FC490EDE-C683-E511-8229-0025905A605E.root')
process.source.fileNames = cms.untracked.vstring('/store/relval/CMSSW_7_6_0/RelValTTbar_13/MINIAODSIM/PUpmx25ns_76X_mcRun2_asymptotic_v11_gs7120p2rlBS-v1/00000/48525870-3184-E511-8F62-0025905A6066.root',
       '/store/relval/CMSSW_7_6_0/RelValTTbar_13/MINIAODSIM/PUpmx25ns_76X_mcRun2_asymptotic_v11_gs7120p2rlBS-v1/00000/AC429137-3284-E511-8D93-003048FFD796.root')
#                                         ##
process.maxEvents.input = 5
#                                         ##
#   process.out.outputCommands = [ ... ]  ##  (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#                                         ##
process.out.fileName = 'testJetTools.root'
#                                         ##
#   process.options.wantSummary = False   ##  (to suppress the long output at the end of the job)
