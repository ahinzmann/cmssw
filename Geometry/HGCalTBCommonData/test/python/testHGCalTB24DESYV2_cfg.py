import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Modifier_hgcaltb_cff import hgcaltb

process = cms.Process('GENSIMDIGI', hgcaltb)

# import of standard configurations
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Geometry.HGCalTBCommonData.testTB24DESYV2XML_cfi')
process.load('Geometry.HGCalCommonData.hgcalNumberingInitialization_cfi')
process.load('Geometry.HGCalCommonData.hgcalParametersInitialization_cfi')
process.load('Geometry.HcalTestBeamData.hcalTB06Parameters_cff')
process.load('Geometry.ForwardCommonData.hfnoseNumberingInitialization_cfi') # for HFnose
process.load('Geometry.ForwardCommonData.hfnoseParametersInitialization_cfi') # for HFnose
process.load('Geometry.CaloEventSetup.HFNoseTopology_cfi') # for HFnose
process.load('Geometry.CaloEventSetup.HGCalTopology_cfi')
process.load('Geometry.CaloEventSetup.CaloTopology_cfi')
process.load('Geometry.CaloEventSetup.CaloGeometryBuilder_cfi')
process.CaloGeometryBuilder = cms.ESProducer(
   "CaloGeometryBuilder",
   SelectedCalos = cms.vstring("HGCalEESensitive", "HGCalHESiliconSensitive", "HGCalHEScintillatorSensitive", "HGCalHFNoseSensitive")
)
process.load('Geometry.HGCalGeometry.HGCalGeometryESProducer_cfi')
process.HGCalHFNoseGeometryESProducer = cms.ESProducer("HGCalGeometryESProducer",
                                              Name = cms.untracked.string("HGCalHFNoseSensitive")
                                              ) # for HF nose
process.load('Configuration.StandardSequences.MagneticField_0T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('GeneratorInterface.Core.generatorSmeared_cfi')
process.load('IOMC.EventVertexGenerators.VtxSmearedFlat_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('SimG4CMS.HGCalTestBeam.DigiHGCalTB24DESYV2_cff')
process.load('RecoLocalCalo.Configuration.hgcalLocalReco_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.Validation_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
#process.load('SimG4CMS.HGCalTestBeam.HGCalTB23Analyzer_cfi')

process.load('DPGAnalysis.HGCalNanoAOD.hgcRecHits_cff')


#process.load('Configuration.StandardSequences.Accelerators_cff')
#process.load('HeterogeneousCore.AlpakaCore.ProcessAcceleratorAlpaka_cfi')

#
# TRANSLATOR TO PHASE I COLLECTION
#
#process.load('RecoLocalCalo.HGCalRecAlgos.hgCalRecHitsFromSoAproducer_cfi')

#
# CONDITIONS AND CONFIGURATIONS
#
# Configuration from YAML files
#process.load('CalibCalorimetry.HGCalPlugins.hgCalConfigESSourceFromYAML_cfi')  # read yaml config file(s)
#process.hgCalConfigESSourceFromYAML.filename = f"{os.environ['CMSSW_BASE']}/src/CalibCalorimetry/HGCalPlugins/test/test_hgcal_yamlmapper.yaml"
#if options.charMode in [0, 1]:  # manually override YAML files
#    process.hgCalConfigESSourceFromYAML.charMode = options.charMode
#if options.gain in [1, 2, 4]:  # manually override YAML files
#    process.hgCalConfigESSourceFromYAML.gain = options.gain

# Alpaka ESProducer
#process.hgcalCalibrationParameterESRecord = cms.ESSource('EmptyESSource',
#                                                         recordName=cms.string('HGCalCondSerializableModuleInfoRcd'),
#                                                         iovIsRunNotTime=cms.bool(True),
#                                                         firstValid=cms.vuint32(1)
#                                                         )

# ESProducer to load calibration parameters from txt file, like pedestal
#process.hgcalCalibESProducer = cms.ESProducer('hgcalrechit::HGCalCalibrationESProducer@alpaka',
#                                              filename=cms.string(''),  # to be set up in configTBConditions
#                                              moduleInfoSource=cms.ESInputTag('')
#                                              )

# ESProducer to load configuration parameters from YAML files, like gain
#process.hgcalConfigESProducer = cms.ESProducer('hgcalrechit::HGCalConfigurationESProducer@alpaka',
#                                               # gain = options.gain, # manually override gain
#                                               configSource=cms.ESInputTag('')
#                                               )

# CONDITIONS
# RecHit producer: pedestal txt file for DIGI -> RECO calibration
# Logical mapping
# process.load('CalibCalorimetry.HGCalPlugins.hgCalPedestalsESSource_cfi') # superseded by hgcalCalibESProducer
#process.load('Geometry.HGCalMapping.hgCalModuleInfoESSource_cfi')
#process.load('Geometry.HGCalMapping.hgCalSiModuleInfoESSource_cfi')

#process.load('HeterogeneousCore.CUDACore.ProcessAcceleratorCUDA_cfi')
#process.hgcalRecHit = cms.EDProducer('alpaka_serial_sync::HGCalRecHitProducer',
#                                         digis=cms.InputTag('hgcalDigis', '', 'TEST'),
#                                         calibSource=cms.ESInputTag('hgcalCalibESProducer', ''),
#                                         configSource=cms.ESInputTag('hgcalConfigESProducer', ''),
#                                         n_hits_scale=cms.int32(1),
#                                         n_blocks=cms.int32(1024),
#                                         n_threads=cms.int32(4096)
#                                         )





process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

if 'MessageLogger' in process.__dict__:
    process.MessageLogger.G4cerr=dict()
    process.MessageLogger.G4cout=dict()
    process.MessageLogger.HGCSim=dict()
    process.MessageLogger.CaloSim=dict()
    process.MessageLogger.FlatThetaGun=dict()
    process.MessageLogger.FlatEvtVtx=dict()

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('SingleElectronE100_cfi nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.EDMoutput = cms.OutputModule("PoolOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW'),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('file:gensimdigi.root'),
    #outputCommands = process.EDMEventContent.outputCommands,
    #outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
    outputCommands = cms.untracked.vstring("keep *"),
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition
process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string('TBGenSimDigi.root')
                                   )

process.NANOAODoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:nanoaod.root'),
    outputCommands = process.NANOAODEventContent.outputCommands
)
process.NANOAODoutput.compressionAlgorithm = 'ZSTD'
process.NANOAODoutput.compressionLevel = 5

process.DQMoutput = cms.OutputModule("DQMRootOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('DQMIO'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:dqm.root'),
    outputCommands = process.DQMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T21', '')

process.generator = cms.EDProducer("FlatRandomEGunProducer",
    AddAntiParticle = cms.bool(False),
    PGunParameters = cms.PSet(
        MinE = cms.double(100),
        MaxE = cms.double(100),
        MinEta = cms.double(1e10),
        MaxEta = cms.double(1e10),
        MinPhi = cms.double(0),
        MaxPhi = cms.double(0),
        XOffset = cms.double(1.0), # 1cm away from middle
        YOffset = cms.double(150.0), # somewwhere in the middle of HGCAL
        ZPosition = cms.double(0.0),
        PartID = cms.vint32(11) # 11 for electrons, 2212 for protons
    ),
    Verbosity = cms.untracked.int32(1),
    firstRun = cms.untracked.uint32(1),
    psethack = cms.string('single electron E 100')
)
#process.generator = cms.EDProducer("FlatRandomEThetaGunProducer",
#    AddAntiParticle = cms.bool(False),
#    PGunParameters = cms.PSet(
#        MinE = cms.double(99.99),
#        MaxE = cms.double(100.01),
#        MinTheta = cms.double(0.0),
#        MaxTheta = cms.double(0.0),
#        MinPhi = cms.double(-3.14159265359),
#        MaxPhi = cms.double(3.14159265359),
#        PartID = cms.vint32(11) # 11 for electrons, 2212 for protons
#    ),
#    Verbosity = cms.untracked.int32(1),
#    firstRun = cms.untracked.uint32(1),
#    psethack = cms.string('single electron E 10')
#)
#process.generator = cms.EDProducer("BeamMomentumGunProducer",
#    AddAntiParticle = cms.bool(False),
#    PGunParameters = cms.PSet(
#        FileName = cms.FileInPath('SimG4CMS/HGCalTestBeam/data/HGCTBeamProfTree_PosE100.root'),
#        MinTheta = cms.double(0),
#        MaxTheta = cms.double(0),
#        MinPhi = cms.double(0),
#        MaxPhi = cms.double(0),
#        XOffset = cms.double(1.0), # 1cm away from middle
#        YOffset = cms.double(150.0), # somewwhere in the middle of HGCAL
#        ZPosition = cms.double(0.0),
#        PartID = cms.vint32(11)
#    ),
#    Verbosity = cms.untracked.int32(1),
#    firstRun = cms.untracked.uint32(1),
#    psethack = cms.string('single electron E 100')
#)
process.VtxSmeared.MinZ = -0.1
process.VtxSmeared.MaxZ = 0.1
#process.VtxSmeared.MinX = -1.0
#process.VtxSmeared.MaxX =  1.0
#process.VtxSmeared.MinY = -1.0
#process.VtxSmeared.MaxY =  1.0
process.g4SimHits.OnlySDs = ['HGCalSensitiveDetector','HGCScintillatorSensitiveDetector', 'HcalTB06BeamDetector','HFNoseSensitiveDetector']
process.g4SimHits.HGCSD.Detectors = 1
process.g4SimHits.HGCSD.RejectMouseBite = False
process.g4SimHits.HGCSD.RotatedWafer    = False

process.g4SimHits.CaloTrkProcessing.TestBeam = True
process.g4SimHits.HCalSD.ForTBHCAL = True
process.g4SimHits.NonBeamEvent = True
process.g4SimHits.UseMagneticField = False

process.g4SimHits.EventVerbose = 2
process.g4SimHits.SteppingVerbosity = 2
process.g4SimHits.StepVerboseThreshold= 0.1
process.g4SimHits.VerboseEvents = [1]
process.g4SimHits.VertexNumber = []
process.g4SimHits.VerboseTracks =[]

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.digitisation_step = cms.Path(process.mix)
process.raw2digi_step = cms.Path(process.hgcalDigis)
process.reconstruction_step = cms.Path(cms.Sequence(process.HGCalUncalibRecHit*process.HGCalRecHit*process.hgcalRecHitMapProducer*process.hgcalLayerClustersEE*process.hgcalLayerClustersHSi*process.hgcalLayerClustersHSci*process.hgcalMergeLayerClusters))
process.hgcalnano_step = cms.Path(cms.Sequence(process.hgcRecHitsTask))
#process.analysis_step = cms.Path(process.HGCalTB23Analyzer)
process.prevalidation_step7 = cms.Path(process.globalPrevalidationHGCal)
#process.validation_step9 = cms.EndPath(process.globalValidationHGCal)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.EDMoutput_step = cms.EndPath(process.EDMoutput)
process.NANOAODoutput_step = cms.EndPath(process.NANOAODoutput)
process.DQMoutput_step = cms.EndPath(process.DQMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,
				process.genfiltersummary_step,
				process.simulation_step,
				process.digitisation_step,
                                process.raw2digi_step,
				process.reconstruction_step,
				process.hgcalnano_step,
			        #process.analysis_step,
                                process.prevalidation_step7,
                                #process.validation_step9,
				process.endjob_step,
				process.EDMoutput_step,
                                process.NANOAODoutput_step,
                                process.DQMoutput_step
				)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq 

from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# Automatic addition of the customisation function from DPGAnalysis.HGCalTools.tb2023_cfi
#from DPGAnalysis.HGCalTools.tb2023_cfi import addPerformanceReports,configTBConditions_default 

#call to customisation function addPerformanceReports imported from DPGAnalysis.HGCalTools.tb2023_cfi
#process = addPerformanceReports(process)

#call to customisation function configTBConditions_default imported from DPGAnalysis.HGCalTools.tb2023_cfi
#process = configTBConditions_default(process)
