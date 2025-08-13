
#ifndef FlatRandomAngleEGunProducer_H
#define FlatRandomAngleEGunProducer_H

/** \class FlatRandomAngleEGunProducer
 *
 * Generates single particle gun in HepMC format
 * Julia Yarba 10/2005 
 ***************************************/

#include "IOMC/ParticleGuns/interface/BaseFlatGunProducer.h"
namespace edm {

  class FlatRandomAngleEGunProducer : public BaseFlatGunProducer {
  public:
    FlatRandomAngleEGunProducer(const ParameterSet& pset);
    ~FlatRandomAngleEGunProducer() override;

    void produce(Event& e, const EventSetup& es) override;

  private:
    // Energy range
    double fMinE;  // Minimum energy
    double fMaxE;  // Maximum energy

    // Theta (zenith angle) range
    double fMinTheta;  // Minimum zenith angle
    double fMaxTheta;  // Maximum zenith angle

    // Data members for position offsets
    double zpos_;  // Z position
    std::vector<double> xCoords_;  // Multiple X positions
    std::vector<double> yCoords_;  // Multiple Y positions
    int particlesPerPosition_;  // Number of particles per position

    // Constants
    static constexpr double mm2cm_ = 0.1;  // Conversion from mm to cm
    static constexpr double cm2mm_ = 10.0;  // Conversion from cm to mm
  };
}  // namespace edm

#endif

