#ifndef JMTucker_Tools_TrackRescaler_wLep_h
#define JMTucker_Tools_TrackRescaler_wLep_h

#ifndef JMT_STANDALONE
#include "DataFormats/TrackReco/interface/Track.h"
#endif

namespace jmt {
  class TrackRescaler_wLep {
  public:
    class Scales {
    public:
      Scales() : dxyerr_(1), dszerr_(1), dxydszcov_(1) {}
      void reset() { dxyerr_ = dszerr_ = dxydszcov_ = 1; }
      void set(double dxyerr, double dszerr, double dxydszcov) {
        dxyerr_ = dxyerr;
        dszerr_ = dszerr;
        dxydszcov_ = dxydszcov;
      }

      double dxyerr() const { return dxyerr_; }
      double dszerr() const { return dszerr_; }
      double dxydszcov() const { return dxydszcov_; }
      double dxycov() const { return pow(dxyerr_, 2); }
      double dszcov() const { return pow(dszerr_, 2); }

      double dxycov(double c) const { return c * dxycov(); }
      double dszcov(double c) const { return c * dszcov(); }
      double dxydszcov(double c) const { return c * dxydszcov(); }

    private:
      double dxyerr_;
      double dszerr_;
      double dxydszcov_;
    };

    TrackRescaler_wLep() : enable_(false), era_(0), which_(w_SingleLep), type_("") {}
    void setup(bool enable, int era, int which, std::string type) { enable_ = enable; era_ = era; which_ = which; type_ = type; }
    void enable(bool enable) { enable_ = enable; }

    enum { w_SingleLep, w_max };

    void set_SingleLep2017(double pt, double eta, std::string type);
    void set_SingleLep2018(double pt, double eta, std::string type);

    void set(double era, int which, double pt, double eta, std::string type);
    void set(double pt, double eta, std::string type) { set(era_, which_, pt, eta, type); }

    const Scales& scales() const { return scales_; }
    bool enable() const { return enable_; }
    int era() const { return era_; }
    int which() const { return which_; }
    std::string type() const { return type_; }

#ifndef JMT_STANDALONE
    struct ret_t {
      reco::Track tk;
      reco::Track rescaled_tk;
    };

    ret_t scale(const reco::Track& tk, std::string type);
#endif

  private:
    Scales scales_;
    bool enable_;
    int era_;
    int which_;
    std::string type_;
  };
}

#endif
