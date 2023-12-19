import FWCore.ParameterSet.Config as cms

XMLIdealGeometryESSource = cms.ESSource("XMLIdealGeometryESSource",
    geomXMLFiles = cms.vstring('Geometry/CMSCommonData/data/materials.xml',
                               'Geometry/CMSCommonData/data/rotations.xml',
                               'Geometry/HGCalCommonData/data/hgcalMaterial/v2/hgcalMaterial.xml',
                               'Geometry/HGCalTBCommonData/data/TB24DESY/cms.xml',
                               'Geometry/HGCalTBCommonData/data/TB24DESY/caloBase.xml',
                               'Geometry/HGCalTBCommonData/data/TB24DESY/hgcal.xml',
                               'Geometry/HGCalTBCommonData/data/TB24DESY/hgcalBeam.xml',
                               'Geometry/HGCalCommonData/data/hgcalcell/v17/hgcalcell.xml',
                               'Geometry/HGCalCommonData/data/hgcalwafer/v17/hgcalwafer.xml',
                               'Geometry/HGCalCommonData/data/hgcalHEmix/v17/hgcalHEmix.xml',
                               'Geometry/HGCalTBCommonData/data/TB24DESY/hgcalCons.xml',
                               'Geometry/HGCalTBCommonData/data/TB24DESY/hgcalConsData.xml',
                               'Geometry/HGCalTBCommonData/data/TB24DESY/hgcalsense.xml',
                               'Geometry/HGCalTBCommonData/data/TB230/hgcProdCuts.xml',
                               ),
    rootNodeName = cms.string('cms:OCMS')
)


