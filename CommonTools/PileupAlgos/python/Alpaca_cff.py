import FWCore.ParameterSet.Config as cms

is_data_flag = False

jecFilesData = ( cms.untracked.vstring('BaconProd/Utils/data/Summer15_25nsV2_DATA_L1FastJet_AK4PF.txt',
                                       'BaconProd/Utils/data/Summer15_25nsV2_DATA_L2Relative_AK4PF.txt',
                                       'BaconProd/Utils/data/Summer15_25nsV2_DATA_L3Absolute_AK4PF.txt',
                                       'BaconProd/Utils/data/Summer15_25nsV2_DATA_L2L3Residual_AK4PF.txt') )

jecFilesMC   = ( cms.untracked.vstring('BaconProd/Utils/data/Summer15_25nsV2_MC_L1FastJet_AK4PF.txt',
                                       'BaconProd/Utils/data/Summer15_25nsV2_MC_L2Relative_AK4PF.txt',
				       'BaconProd/Utils/data/Summer15_25nsV2_MC_L3Absolute_AK4PF.txt') )
	       

alpaca = cms.EDProducer("AlpacaProducer",
                        algoId         = cms.int32(1),
                        cone           = cms.double(0.4),
                        candName       = cms.InputTag('particleFlow'),
                        rhoName        = cms.InputTag('fixedGridRhoFastjetAll'),
                        chJecFiles     = jecFilesData if is_data_flag else jecFilesMC,
                        emJecFiles     = jecFilesData if is_data_flag else jecFilesMC,
                        nhJecFiles     = jecFilesData if is_data_flag else jecFilesMC,
                        minAlgoVal     = cms.double(10.),
                        )

alpacaData = cms.EDProducer("AlpacaProducer",
                            algoId         = cms.int32(1),
                            cone           = cms.double(0.4),
                            candName       = cms.InputTag('particleFlow'),
                            rhoName        = cms.InputTag('fixedGridRhoFastjetAll'),
                            chJecFiles     = jecFilesData,
                            emJecFiles     = jecFilesData,
                            nhJecFiles     = jecFilesData,
                            minAlgoVal     = cms.double(10.),
                            )


alpacaMC   = cms.EDProducer("AlpacaProducer",
                            algoId         = cms.int32(1),
                            cone           = cms.double(0.4),
                            candName       = cms.InputTag('particleFlow'),
                            rhoName        = cms.InputTag('fixedGridRhoFastjetAll'),
                            chJecFiles     = jecFilesMC,
                            emJecFiles     = jecFilesMC,
                            nhJecFiles     = jecFilesMC,
                            minAlgoVal     = cms.double(10.),
                            )

