#include "PhysicsTools/NanoAOD/interface/SimpleFlatTableProducer.h"

#include "DataFormats/CaloRecHit/interface/CaloRecHit.h"
typedef SimpleFlatTableProducer<CaloRecHit> SimpleCaloRecHitFlatTableProducer;

#include "DataFormats/HGCalDigi/interface/HGCalDigiCollections.h"
typedef SimpleFlatTableProducer<HGCROCChannelDataFrameElecSpec> SimpleHGCalDigiFlatTableProducer;

#include "DataFormats/HGCalDigi/interface/HGCalFlaggedECONDInfo.h"
typedef SimpleFlatTableProducer<HGCalFlaggedECONDInfo> SimpleHGCalUnpackerFlagsTableProducer;

#include "DataFormats/HGCDigi/interface/HGCDataFrame.h"
#include "DataFormats/HGCDigi/interface/HGCSample.h"
typedef SimpleFlatTableProducer<HGCDataFrame<DetId, HGCSample> > SimpleHGCDigiFlatTableProducer;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(SimpleCaloRecHitFlatTableProducer);
DEFINE_FWK_MODULE(SimpleHGCalDigiFlatTableProducer);
DEFINE_FWK_MODULE(SimpleHGCalUnpackerFlagsTableProducer);
DEFINE_FWK_MODULE(SimpleHGCDigiFlatTableProducer);
