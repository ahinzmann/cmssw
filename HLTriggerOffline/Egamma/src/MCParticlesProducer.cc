// -*- C++ -*-
//
// Package:    MCParticlesProducer
// Class:      MCParticlesProducer
// 
/**\class MCParticlesProducer MCParticlesProducer.cc HLTriggerOffline/Egamma/src/MCParticlesProducer.cc

 Description: <one line class summary>

 Implementation:
     <Notes on implementation>
*/
//
// Original Author:  Joshua Berger
//         Created:  Mon Jul 23 22:52:31 CEST 2007
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Candidate/interface/Particle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleCandidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleCandidateFwd.h"
#include "SimDataFormats/HepMCProduct/interface/HepMCProduct.h"

//
// class decleration
//

class MCParticlesProducer : public edm::EDProducer {
   public:
      explicit MCParticlesProducer(const edm::ParameterSet&);
      ~MCParticlesProducer();

   private:
      virtual void beginJob(const edm::EventSetup&) ;
      virtual void produce(edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;
      
      // ----------member data ---------------------------
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
MCParticlesProducer::MCParticlesProducer(const edm::ParameterSet& iConfig)
{
   //register your products
/* Examples
   produces<ExampleData2>();

   //if do put with a label
   produces<ExampleData2>("label");
*/

   produces<reco::GenParticleCandidateCollection>();
   //now do what ever other initialization is needed

}


MCParticlesProducer::~MCParticlesProducer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to produce the data  ------------
void
MCParticlesProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;
   using namespace reco;

   Handle<HepMCProduct> mcProd;
   iEvent.getByLabel("source", mcProd);
   const HepMC::GenEvent * mcEvent = mcProd->GetEvent();

   std::auto_ptr<GenParticleCandidateCollection> mcParts(new GenParticleCandidateCollection);

   for(HepMC::GenEvent::particle_const_iterator mcpart = mcEvent->particles_begin(); mcpart != mcEvent->particles_end(); ++ mcpart ) {
     Particle::LorentzVector p((*mcpart)->momentum().x(), (*mcpart)->momentum().y(), (*mcpart)->momentum().z(), (*mcpart)->momentum().t());
     Particle::Point vtx(0, 0, 0);
     if ((*mcpart)->production_vertex() != NULL) {
       const double x = (*mcpart)->production_vertex()->point3d().x();
       const double y = (*mcpart)->production_vertex()->point3d().y();
       const double z = (*mcpart)->production_vertex()->point3d().z();
       vtx = Particle::Point(x, y, z);
     }
     GenParticleCandidate keeper((*mcpart)->pdg_id() / abs((*mcpart)->pdg_id()), p, vtx, (*mcpart)->pdg_id(), (*mcpart)->status(), false);
     mcParts->push_back(keeper);
   }

   iEvent.put(mcParts);
}

// ------------ method called once each job just before starting event loop  ------------
void 
MCParticlesProducer::beginJob(const edm::EventSetup&)
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
MCParticlesProducer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(MCParticlesProducer);
