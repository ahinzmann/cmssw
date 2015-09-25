#include "CommonTools/PileupAlgos/interface/AlpacaAlgo.h"
#include "fastjet/internal/base.hh"
#include "fastjet/FunctionOfPseudoJet.hh"
#include "Math/ProbFunc.h"
#include "TMath.h"
#include <iostream>
#include <math.h>
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Utilities/interface/isFinite.h"

using namespace std;
using namespace fastjet;

AlpacaAlgo::AlpacaAlgo(const edm::ParameterSet &iConfig,FactorizedJetCorrector* iCHCorr,FactorizedJetCorrector* iEMCorr,FactorizedJetCorrector* iNHCorr) {
  //fSeparate        = iConfig.getParameter<bool>  ("separateParticle");
  fAlgoMin         = iConfig.getParameter<double>("minAlgoVal");
  fAlgo            = iConfig.getParameter<int>   ("algoId");
  fCone            = iConfig.getParameter<double>("cone");  
  fCHCorr = iCHCorr;
  fEMCorr = iEMCorr;
  fNHCorr = iNHCorr;
}
AlpacaAlgo::~AlpacaAlgo(){}
void AlpacaAlgo::initialize(const std::vector<RecoObj> &iRecoObjects,const double &iRho) {
  //Clear everything
  fRecoParticles.resize(0);
  fRho    = iRho;
  fRecoParticles = iRecoObjects;
  for (unsigned int i = 0; i < fRecoParticles.size(); i++){
    fastjet::PseudoJet curPseudoJet;
    auto pRecoParticle = fRecoParticles[i];
    curPseudoJet.reset_PtYPhiM(pRecoParticle.pt,pRecoParticle.rapidity,pRecoParticle.phi,pRecoParticle.m);
    int alpaca_register = convert(pRecoParticle.id);
    curPseudoJet.set_user_info( new AlpacaUserInfo( alpaca_register ) );
    fPFParticles.push_back(curPseudoJet);
  }
  fRho = iRho;
}
int AlpacaAlgo::convert(int iId) { 
  int lRegister = -1;
  if(iId == 130 || iId < 3) lRegister = 0;
  if(iId == 22)             lRegister = 1;
  if(lRegister == -1)       lRegister = 2; //Defer to charged hadrons
  return lRegister;
}
double AlpacaAlgo::var_within_R(int iId, const std::vector<PseudoJet> & particles, const PseudoJet& centre, double R){
    if(iId == -1) return 1;
    fastjet::Selector sel = fastjet::SelectorCircle(R);
    sel.set_reference(centre);
    vector<PseudoJet> near_particles = sel(particles);
    double var = 0;
    for(unsigned int i=0; i<near_particles.size(); i++){
        double pDEta = near_particles[i].eta()-centre.eta();
        double pDPhi = std::abs(near_particles[i].phi()-centre.phi());
        if(pDPhi > 2.*M_PI-pDPhi) pDPhi =  2.*M_PI-pDPhi;
        double pDR2 = pDEta*pDEta+pDPhi*pDPhi;
        if(std::abs(pDR2)  <  0.0001) continue;
        if(iId == 0) var += (near_particles[i].pt()/pDR2);
        if(iId == 1) var += near_particles[i].pt();
        if(iId == 2) var += (1./pDR2);
        if(iId == 3) var += (1./pDR2);
        if(iId == 4) var += near_particles[i].pt();
        if(iId == 5) var += (near_particles[i].pt() * near_particles[i].pt()/pDR2);
    }
    if(iId == 1) var += centre.pt(); //Sum in a cone
    if(iId == 0 && var != 0) var = log(var);
    if(iId == 3 && var != 0) var = log(var);
    if(iId == 5 && var != 0) var = log(var);
    return var;
}
double AlpacaAlgo::getScale(int iId,fastjet::PseudoJet &iJet) { 
  int lId       = convert(iId);
  double pScale = 1.;
  double pVal   = var_within_R(fAlgo,fPFParticles,iJet,fCone);
  if(pVal < fAlgoMin) pVal = fAlgoMin;
  if(lId == 0) pScale = correct(fNHCorr,iJet,pVal);
  if(lId == 1) pScale = correct(fEMCorr,iJet,pVal);
  if(lId == 2) pScale = correct(fCHCorr,iJet,pVal);
  return pScale;
}
double AlpacaAlgo::correct(FactorizedJetCorrector *iCorr,fastjet::PseudoJet &iJet,double iVal) { 
  iCorr->setJetPt(iVal);
  iCorr->setJetEta(iJet.eta());
  iCorr->setJetPhi(iJet.phi());
  iCorr->setJetE(iVal);
  iCorr->setRho(fRho);
  iCorr->setJetA(fCone*fCone*TMath::Pi());
  iCorr->setJetEMF(-99.0);
  return iCorr->getCorrection();
}
