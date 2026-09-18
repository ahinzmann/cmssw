import FWCore.ParameterSet.Config as cms

XMLIdealGeometryESSource = cms.ESSource("XMLIdealGeometryESSource",
    geomXMLFiles = cms.vstring('Geometry/CMSCommonData/data/materials.xml',
                               'Geometry/CMSCommonData/data/rotations.xml',
                               'Geometry/HGCalCommonData/data/hgcalMaterial/v3/hgcalMaterial.xml',
                               'Geometry/HGCalTBCommonData/data/TB24DESYV2/cms.xml',
                               'Geometry/HGCalTBCommonData/data/TB24DESYV2/caloBase.xml',
                               #'Geometry/HGCalTBCommonData/data/TB24DESYV2/hgcalBeam.xml',
                               'Geometry/HGCalTBCommonData/data/TB24DESYV2/hgcal.xml', # adapted from Geometry/HGCalCommonData/data/hgcal/v19/hgcal.xml
                               'Geometry/HGCalCommonData/data/hgcalHEmix/v19/hgcalHEmix.xml',
                               'Geometry/HGCalCommonData/data/hgcalcell/v19/hgcalcell.xml',
                               'Geometry/HGCalCommonData/data/hgcalwafer/v19/hgcalwafer.xml',
                               'Geometry/HGCalCommonData/data/hgcalPassive/v19/hgcalPassive.xml',
                               'Geometry/HGCalCommonData/data/hgcalEE/v19/hgcalEE.xml',
                               'Geometry/HGCalCommonData/data/hgcalHEsil/v19/hgcalHEsil.xml',
                               'Geometry/HGCalCommonData/data/hgcalCons/v19/hgcalCons.xml',
                               'Geometry/HGCalCommonData/data/hgcalConsData/v19/hgcalConsData.xml',
                               'Geometry/HGCalSimData/data/hgcsensv15.xml',
                               'Geometry/HGCalTBCommonData/data/TB230/hgcProdCuts.xml',
                               ),
    rootNodeName = cms.string('cms:OCMS')
)


