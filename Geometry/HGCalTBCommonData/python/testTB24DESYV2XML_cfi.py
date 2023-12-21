import FWCore.ParameterSet.Config as cms

XMLIdealGeometryESSource = cms.ESSource("XMLIdealGeometryESSource",
    geomXMLFiles = cms.vstring('Geometry/CMSCommonData/data/materials.xml',
                               'Geometry/CMSCommonData/data/rotations.xml',
                               'Geometry/HGCalCommonData/data/hgcalMaterial/v2/hgcalMaterial.xml',
                               'Geometry/HGCalTBCommonData/data/TB24DESYV2/cms.xml',
                               'Geometry/HGCalTBCommonData/data/TB24DESYV2/caloBase.xml',
                               'Geometry/HGCalTBCommonData/data/TB24DESYV2/hgcalBeam.xml',
                               'Geometry/HGCalTBCommonData/data/TB24DESYV2/hgcal.xml',
                               'Geometry/HGCalCommonData/data/hgcalcell/v17/hgcalcell.xml',
                               'Geometry/HGCalCommonData/data/hgcalwafer/v17/hgcalwafer.xml',
                               'Geometry/HGCalCommonData/data/hgcalEE/v17/hgcalEE.xml',
                               'Geometry/HGCalCommonData/data/hgcalHEsil/v17/hgcalHEsil.xml',
                               'Geometry/HGCalCommonData/data/hgcalHEmix/v17/hgcalHEmix.xml',
                               'Geometry/HGCalCommonData/data/hgcalCons/v17/hgcalCons.xml',
                               'Geometry/HGCalCommonData/data/hgcalConsData/v17/hgcalConsData.xml',
                               'Geometry/HGCalSimData/data/hgcsensv15.xml',
                               'Geometry/HGCalTBCommonData/data/TB230/hgcProdCuts.xml',
                               ),
    rootNodeName = cms.string('cms:OCMS')
)


