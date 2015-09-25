// system include files
#include <memory>
#include "TMath.h"

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/Common/interface/Association.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

//Main File
#include "fastjet/PseudoJet.hh"
#include "CommonTools/PileupAlgos/plugins/AlpacaProducer.h"


// ------------------------------------------------------------------------------------------
AlpacaProducer::AlpacaProducer(const edm::ParameterSet& iConfig) {
  fTokenPFCandidates     = consumes<CandidateView>(iConfig.getParameter<edm::InputTag>("candName"));
  fTokenRho              = consumes<double>       (iConfig.getParameter<edm::InputTag>("rhoName"));

  produces<edm::ValueMap<float> > ();
  produces< edm::ValueMap<reco::CandidatePtr> >(); 
  produces<PFOutputCollection>();
  //FactorizedJetCorrector* lCHCorr = 0;
  //FactorizedJetCorrector* lEMCorr = 0;
  //FactorizedJetCorrector* lNHCorr = 0;

  std::vector<std::string> empty_vstring;
  fCHCorr = initJetCorr(iConfig.getUntrackedParameter< std::vector<std::string> >("chJecFiles",empty_vstring));
  fEMCorr = initJetCorr(iConfig.getUntrackedParameter< std::vector<std::string> >("emJecFiles",empty_vstring));
  fNHCorr = initJetCorr(iConfig.getUntrackedParameter< std::vector<std::string> >("nhJecFiles",empty_vstring));
  fAlpacaAlgo =  std::unique_ptr<AlpacaAlgo> (  new AlpacaAlgo(iConfig,fCHCorr,fEMCorr,fNHCorr));
}
// ------------------------------------------------------------------------------------------
AlpacaProducer::~AlpacaProducer(){}
// ------------------------------------------------------------------------------------------
FactorizedJetCorrector* AlpacaProducer::initJetCorr(const std::vector<std::string> &jecFiles) {
  std::string cmssw_base_src = getenv("CMSSW_BASE");
  cmssw_base_src += "/src/";
  std::vector<JetCorrectorParameters> corrParams;
  for(unsigned int icorr=0; icorr<jecFiles.size(); icorr++) {
    corrParams.push_back(JetCorrectorParameters(cmssw_base_src + jecFiles[icorr]));
  }
  FactorizedJetCorrector * lJetCorr = new FactorizedJetCorrector(corrParams);
  return lJetCorr;
}
// ------------------------------------------------------------------------------------------
void AlpacaProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  // Get PFCandidate Collection
  edm::Handle<CandidateView> hPFProduct;
  iEvent.getByToken(fTokenPFCandidates,hPFProduct);
  const CandidateView *pfCol = hPFProduct.product();

  // Get vertex collection w/PV as the first entry?
  edm::Handle<double> hRhoIso;
  iEvent.getByToken(fTokenRho,hRhoIso);
  double rho = *hRhoIso;

  static const reco::PFCandidate dummySinceTranslateIsNotStatic;
  fAlpacaCandidates.reset( new PFOutputCollection );
  std::vector<reco::CandidatePtr> values(hPFProduct->size());

  fRecoObjCollection.clear();
  for(CandidateView::const_iterator itPF = pfCol->begin(); itPF!=pfCol->end(); itPF++) {
    RecoObj pReco;
    pReco.pt       = itPF->pt();
    pReco.eta      = itPF->eta();
    pReco.rapidity = itPF->rapidity();
    pReco.phi      = itPF->phi();
    pReco.m        = itPF->mass();
    pReco.charge   = itPF->charge(); 
    pReco.id       = itPF->pdgId();
    fRecoObjCollection.push_back(pReco);
  }
  std::vector<double> lWeights;
  fAlpacaAlgo->initialize(fRecoObjCollection,rho);
  for ( auto i0 = hPFProduct->begin(),  i0end = hPFProduct->end(); i0 != i0end; ++i0 ) {
    auto id = dummySinceTranslateIsNotStatic.translatePdgIdToType(i0->pdgId());
    const reco::PFCandidate *pPF = dynamic_cast<const reco::PFCandidate*>(&(*i0));
    reco::PFCandidate pCand( pPF ? *pPF : reco::PFCandidate(i0->charge(), i0->p4(), id) );
    fastjet::PseudoJet pJet;
    pJet.reset_PtYPhiM(i0->pt(),i0->rapidity(),i0->phi(),i0->mass());
    double pScale = fAlpacaAlgo->getScale(i0->pdgId(),pJet);
    LorentzVector pVec = i0->p4();
    pVec.SetPxPyPzE(i0->px()*pScale,i0->py()*pScale,i0->pz()*pScale,i0->energy()*pScale);
    pCand.setP4(pVec);
    fAlpacaCandidates->push_back(pCand);
    lWeights.push_back(pScale);
  }
  std::auto_ptr<edm::ValueMap<float> > lAlpOut(new edm::ValueMap<float>());
  edm::ValueMap<float>::Filler  lAlpFiller(*lAlpOut);
  lAlpFiller.insert(hPFProduct,lWeights.begin(),lWeights.end());
  lAlpFiller.fill();  
  edm::OrphanHandle<reco::PFCandidateCollection> oh = iEvent.put( fAlpacaCandidates );
  for(unsigned int ic=0, nc = oh->size(); ic < nc; ++ic) {
      reco::CandidatePtr pkref( oh, ic );
      values[ic] = pkref;
    
   }  
  std::auto_ptr<edm::ValueMap<reco::CandidatePtr> > pfMap_p(new edm::ValueMap<reco::CandidatePtr>());
  edm::ValueMap<reco::CandidatePtr>::Filler filler(*pfMap_p);
  filler.insert(hPFProduct, values.begin(), values.end());
  filler.fill();
  iEvent.put(pfMap_p);
}
// ------------------------------------------------------------------------------------------
void AlpacaProducer::beginJob() {
}
// ------------------------------------------------------------------------------------------
void AlpacaProducer::endJob() {
}
// ------------------------------------------------------------------------------------------
void AlpacaProducer::beginRun(edm::Run&, edm::EventSetup const&) {
}
// ------------------------------------------------------------------------------------------
void AlpacaProducer::endRun(edm::Run&, edm::EventSetup const&) {
}
// ------------------------------------------------------------------------------------------
void AlpacaProducer::beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&) {
}
// ------------------------------------------------------------------------------------------
void AlpacaProducer::endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&) {
}
// ------------------------------------------------------------------------------------------
void AlpacaProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(AlpacaProducer);
