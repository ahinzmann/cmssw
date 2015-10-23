#include "RecoTauTag/RecoTau/interface/RecoTauBuilderPlugins.h"
#include "RecoTauTag/RecoTau/interface/RecoTauCommonUtilities.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

namespace reco { namespace tau {

// Update our reference to the PFCandidates & PVs
void RecoTauBuilderPlugin::beginEvent() {
  vertexAssociator_.setEvent(*evt());
  edm::Handle<edm::View<reco::PFCandidate> > pfCandsHandle;
  edm::Handle<std::vector<edm::FwdPtr<reco::PFCandidate> > > pfPtrCandsHandle;
  bool isPtr = evt()->getByToken(pfPtr_token, pfPtrCandsHandle); //As in RecoJets/JetProducers/plugins/VirtualJetProducer.cc
  if (!isPtr) evt()->getByToken(pf_token, pfCandsHandle);

  // Build Ptrs for all the PFCandidates
  pfCands_.clear();
  if(!isPtr)
  {
    pfCands_.reserve(pfCandsHandle->size());
    for ( size_t icand = 0; icand < pfCandsHandle->size(); ++icand ) {
      pfCands_.push_back(edm::Ptr<reco::PFCandidate>(pfCandsHandle,icand));
    }
  } else {
    pfCands_.reserve(pfPtrCandsHandle->size());
    for ( size_t icand = 0; icand < pfPtrCandsHandle->size(); ++icand ) {
     if ( (*pfPtrCandsHandle)[icand].ptr().isAvailable() ) {
       pfCands_.push_back( (*pfPtrCandsHandle)[icand].ptr() );
     }
     else if ( (*pfPtrCandsHandle)[icand].backPtr().isAvailable() ) {
       pfCands_.push_back( (*pfPtrCandsHandle)[icand].backPtr() );
     }
    }
  }
}

}}  // end namespace reco::tau

#include "FWCore/Framework/interface/MakerMacros.h"
EDM_REGISTER_PLUGINFACTORY(RecoTauBuilderPluginFactory,
                           "RecoTauBuilderPluginFactory");
EDM_REGISTER_PLUGINFACTORY(RecoTauModifierPluginFactory,
                           "RecoTauModifierPluginFactory");
EDM_REGISTER_PLUGINFACTORY(RecoTauCleanerPluginFactory,
                           "RecoTauCleanerPluginFactory");
