#ifndef RecoLocalCalo_HGCalRecAlgos_HGCalUncalibRecHitRecWeightsAlgo_HH
#define RecoLocalCalo_HGCalRecAlgos_HGCalUncalibRecHitRecWeightsAlgo_HH

/** \class HGalUncalibRecHitRecWeightsAlgo
  *  compute amplitude, pedestal, time jitter, chi2 of a pulse
  *  using a weights method, a la Ecal 
  *
  *  \author Valeri Andreev
  *  
  *
  */

#include "RecoLocalCalo/HGCalRecAlgos/interface/HGCalUncalibRecHitRecAbsAlgo.h"
#include <vector>
#include <cmath>

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "Geometry/HGCalGeometry/interface/HGCalGeometry.h"

#include "SimCalorimetry/HGCalSimAlgos/interface/HGCalSciNoiseMap.h"

template <class C>
class HGCalUncalibRecHitRecWeightsAlgo {
public:
  // destructor
  virtual ~HGCalUncalibRecHitRecWeightsAlgo() {}

  void set_isSiFESim(const bool isSiFE) { isSiFESim_ = isSiFE; }
  bool isSiFESim() const { return isSiFESim_; }

  void set_ADCLSB(const double adclsb) { adcLSB_ = adclsb; }
  void set_TDCLSB(const double tdclsb) { tdcLSB_ = tdclsb; }

  void set_toaLSBToNS(const double lsb2ns) { toaLSBToNS_ = lsb2ns; }

  void set_tdcOnsetfC(const double tdcOnset) { tdcOnsetfC_ = tdcOnset; }

  void set_tofDelay(const double tofDelay) { tofDelay_ = tofDelay; }

  void set_fCPerMIP(const std::vector<double>& fCPerMIP) {
    if (std::any_of(fCPerMIP.cbegin(), fCPerMIP.cend(), [](double conv) { return conv <= 0.0; })) {
      throw cms::Exception("BadConversionFactor") << "At least one of fCPerMIP is zero!" << std::endl;
    }
    fCPerMIP_ = fCPerMIP;
  }

  bool setGeometry(const edm::ESHandle<HGCalGeometry>& geom) {
    geom_ = geom.isValid() ? geom.product() : nullptr;
    if (isSiFESim_ && geom_)
      ddd_ = &(geom_->topology().dddConstants());
    else
      ddd_ = nullptr;
    return geom_ != nullptr;
  }
  
  float desat(double sig, double g, int m=39998) {
	double n = sig/g;
	double ans = -m/n*log(1-(n/m));
	return ans;
  }

float pde(float ov){
float pdei;
pdei = (-0.72*ov*ov)+(10.0*ov)+4.41;
return pdei;
}

float lyVsize(int type, int phase, float edge, float sipm=4.0, float ov=4.0){

//type = Cast or Molded; Molded = 2, Cast = 1 (??) // Should be like that in CMSSW
//phase = 10 = pre-series, 0 = production // Daria's addition to create a single map for the function parameters

// Values A and C parameters for LY function for production tiles if 2 and 1, 12 and 11 if pre-series (by adding 10):
std::map<int, std::vector<float>> LY_params{{2, {2066.53, -7.6}},{1, {1378.53, 32.34}}, {12, {1854.5, -6.52}},{11, {1110.5, 54.8}}};


float LYi, sipmfactor, ovfactor, A, c;
int key;
sipmfactor = sipm/4;  // ratio between SiPM areas in mm^2, nominal is 4 mm^2 
ovfactor = pde(ov)/pde(4); // ratio of PDE at a given overvoltage and nominal (4V)

key = type+phase;
std::vector<float>Z = LY_params.at(key);
A = Z[0];
c = Z[1];
LYi = ((A/edge) + c)*sipmfactor*ovfactor;
//std::cout << "A: " << A << " c: " << c << std::endl;

return LYi;
}

  /// Compute HGCUncalibratedRecHit from DataFrame
  virtual HGCUncalibratedRecHit makeRecHit(const C& dataFrame, const bool computeLocalTime) {
    double amplitude_(-1.), pedestal_(-1.), jitter_(-99.), chi2_(-1.);
    uint32_t flag = 0;

    constexpr int iSample = 2;  //only in-time sample
    const auto& sample = dataFrame.sample(iSample);

    // Were digis done w/ the complete digitization and using signal shape?
    // (originally done only for the silicon, while for scitillator it was trivial. Fomr 11_ also scinti uses shape)
    if (isSiFESim_) {

      if (dataFrame.id().det() == DetId::HGCalHSc) {
        double gain=fCPerMIP_[1];
        double nTotalPx=fCPerMIP_[2];
        HGCScintillatorDetId scId(dataFrame.id().rawId());
        if ((scId.layer()==7+4) || (scId.layer()==7+7) || (scId.layer()==7+8)) { // TESTBEAM
          gain=1.84;
          nTotalPx=8649;
        } else {
          gain=1.47;
          nTotalPx=17459;
        }
        GlobalPoint global = geom_->getPosition(scId);
        double radius = std::sqrt(std::pow(global.x(), 2) + std::pow(global.y(), 2));
  	constexpr double factor = 2 * M_PI * 1. / 288.; // 1.25 degrees
  	double edge = 10*(radius * factor);
        double ly;
        if ((scId.layer()==7+4) || (scId.layer()==7+7) || (scId.layer()==7+8)) // CERN stack FNAL layers with 2mm2
          ly = lyVsize(2,10,edge,2,4);
        else if ((scId.layer()==7+9) && ((scId.ring()==16+3) || (scId.ring()==16+4))) // CERN stack cast tiles
          ly = lyVsize(1,10,edge,4,4);
        else
          ly = lyVsize(2,10,edge,4,4);
        double expadc=gain*ly;
        double adcs=sample.data();
        if (sample.mode())
          adcs *= 2.5;
        double satmipss = adcs/expadc;
        amplitude_ = satmipss*desat(adcs, gain, nTotalPx);
      } else {

      // mode == true: TDC readout was activated and amplitude comes from TimeOverThreshold
      if (sample.mode()) {
        flag = !sample.threshold();  // raise flag if busy cell
        // LG (23/06/2015):
        // to get a continuous energy spectrum we must add here the maximum value in fC ever
        // reported by the ADC. Namely: floor(tdcOnset/adcLSB_) * adcLSB_
        // need to increment by one so TDC doesn't overlap with ADC last bin
        // LG (11/04/2016):
        // offset the TDC upwards to reflect the bin center
        amplitude_ = (std::floor(tdcOnsetfC_ / adcLSB_) + 1.0) * adcLSB_ + (double(sample.data()) + 0.5) * tdcLSB_;
      } else {
        amplitude_ = double(sample.data()) * adcLSB_;  // why do we not have +0.5 here ?
      }  //isSiFESim_
      
      }
    }  //mode()

    // trivial digitization, i.e. no signal shape
    else {
      amplitude_ = double(sample.data()) * adcLSB_;
    }

    if (sample.getToAValid()) {
      const auto& dist2center = geom_ ? geom_->getPosition(dataFrame.id()).mag() : 0;
      jitter_ = computeLocalTime ? double(sample.toa()) * toaLSBToNS_ - tofDelay_
                                 : double(sample.toa()) * toaLSBToNS_ - dist2center / c_cm_ns - tofDelay_;
    }

    int thickness = (ddd_ != nullptr) ? ddd_->waferType(dataFrame.id(), false) : 0;
    amplitude_ = amplitude_ / fCPerMIP_[thickness];

    LogDebug("HGCUncalibratedRecHit") << "isSiFESim_: " << isSiFESim_ << " ADC+: set the charge to: " << amplitude_
                                      << ' ' << sample.data() << ' ' << adcLSB_ << ' '
                                      << "               TDC+: set the ToA to: " << jitter_ << ' ' << sample.toa()
                                      << ' ' << toaLSBToNS_ << ' ' << tdcLSB_
                                      << "               getToAValid(): " << sample.getToAValid()
                                      << " mode(): " << sample.mode() << std::endl;
    LogDebug("HGCUncalibratedRecHit") << "Final uncalibrated amplitude : " << amplitude_ << std::endl;

    return HGCUncalibratedRecHit(dataFrame.id(), amplitude_, pedestal_, jitter_, chi2_, flag);
  }

private:
  static constexpr float c_cm_ns = CLHEP::c_light * CLHEP::ns / CLHEP::cm;
  double adcLSB_, tdcLSB_, toaLSBToNS_, tdcOnsetfC_, tofDelay_;
  bool isSiFESim_;
  std::vector<double> fCPerMIP_;
  const HGCalDDDConstants* ddd_;
  const HGCalGeometry* geom_;
};
#endif
