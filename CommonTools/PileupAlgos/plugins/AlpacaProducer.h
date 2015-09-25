#ifndef CommonTools_Puppi_AlpacaProducer_h_
#define CommonTools_Puppi_AlpacaProducer_h_
// system include files
#include <memory>
#include "TTree.h"
#include "TFile.h"

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Math/interface/PtEtaPhiMass.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CommonTools/PileupAlgos/interface/AlpacaAlgo.h"

class AlpacaProducer : public edm::stream::EDProducer<> {
 public:
  explicit AlpacaProducer(const edm::ParameterSet& iConfig);
  ~AlpacaProducer();
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
  typedef math::XYZTLorentzVector                        LorentzVector;
  typedef std::vector<LorentzVector>                     LorentzVectorCollection;
  typedef edm::View<reco::Candidate>                     CandidateView;
  typedef std::vector< reco::PFCandidate >               PFInputCollection;
  typedef std::vector< reco::PFCandidate >               PFOutputCollection;
  typedef edm::View<reco::PFCandidate>                   PFView;

 private:
  FactorizedJetCorrector* initJetCorr(const std::vector<std::string> &jecFiles);

  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void beginJob();
  virtual void endJob();
  virtual void beginRun(edm::Run&, edm::EventSetup const&);
  virtual void endRun(edm::Run&, edm::EventSetup const&);
  virtual void beginLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
  virtual void endLuminosityBlock(edm::LuminosityBlock&, edm::EventSetup const&);
  
  edm::EDGetTokenT< CandidateView >    fTokenPFCandidates;
  edm::EDGetTokenT< double >           fTokenRho;

  std::unique_ptr<AlpacaAlgo>         fAlpacaAlgo;
  std::vector<RecoObj>                fRecoObjCollection;
  std::auto_ptr< PFOutputCollection > fAlpacaCandidates;

  FactorizedJetCorrector* fCHCorr;
  FactorizedJetCorrector* fEMCorr;
  FactorizedJetCorrector* fNHCorr;
};

#endif
