#ifndef CommonTools_PileupAlgos_AlpacaAlgo_h
#define CommonTools_PileupAlgos_AlpacaAlgo_h
#include "CommonTools/PileupAlgos/interface/RecoObj.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "fastjet/internal/base.hh"
#include "fastjet/PseudoJet.hh"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include <vector>

class AlpacaAlgo{ 
public:
  class AlpacaUserInfo : public fastjet::PseudoJet::UserInfoBase {
   public : 
     AlpacaUserInfo( int alpaca_register = -1) : alpaca_register_(alpaca_register) {}
     virtual ~AlpacaUserInfo(){}
     void set_alpaca_register(int i) { alpaca_register_ = i; }
     inline int alpaca_register() const { return alpaca_register_; }
   protected : 
     int alpaca_register_;     /// Used by puppi algorithm to decide neutrals vs PV vs PU
  };


  AlpacaAlgo(const edm::ParameterSet &iConfig,FactorizedJetCorrector* iCHCorr,FactorizedJetCorrector* iEMCorr,FactorizedJetCorrector* iNHCorr);
  ~AlpacaAlgo();
  void   initialize(const std::vector<RecoObj> &iRecoObjects,const double &iRho);
  int    convert(int iId);
  double var_within_R(int iId, const std::vector<fastjet::PseudoJet> & particles, const fastjet::PseudoJet& centre, double R);
  double getScale(int iId,fastjet::PseudoJet &iJet);
  double correct(FactorizedJetCorrector *iCorr,fastjet::PseudoJet &iJet,double iVal);

private:  
  //bool   fSeparate;
  double fAlgoMin;
  int    fAlgo;
  double fCone;
  double fRho;
  std::vector<RecoObj>   fRecoParticles;
  std::vector<fastjet::PseudoJet> fPFParticles;
  
  FactorizedJetCorrector* fCHCorr;
  FactorizedJetCorrector* fEMCorr;
  FactorizedJetCorrector* fNHCorr;
};


#endif
