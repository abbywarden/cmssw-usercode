#include "JMTucker/Tools/interface/AnalysisEras.h"
#include "JMTucker/Tools/interface/TrackRescaler_wLep.h"

//commenting out until need to use it (or go through the headache of merging it in )
namespace jmt {
    //   void TrackRescaler::set_SingleLep2017(double x, double eta, auto type) {
    //     if (fabs(eta) < 1.5) {

    //       if (type == "") {
    //         const double p_dxy[] = {};
    //         const double p_dsz[] = {};
    //         const double p_dxydsz[] = {};
    //       }
    //       if (type == "electron") {
    //         const double p_dxy[] = {};
    //         const double p_dsz[] = {};
    //         const double p_dxydsz[] = {};
    //       }
    //       if (type == "muon") {
    //         const double p_dxy[] = {};
    //         const double p_dsz[] = {};
    //         const double p_dxydsz[] = {};
    //       }
    //       scales_.set(,
    //                   ,

    //                   );
    //     }
    //     else {
    //       if (type == "") {
    //         const double p_dxy[] = {};
    //         const double p_dsz[] = {};
    //         const double p_dxydsz[] = {};
    //       }
    //       if (type == "electron") {
    //         const double p_dxy[] = {};
    //         const double p_dsz[] = {};
    //         const double p_dxydsz[] = {};
    //       }
    //       if (type == "muon") {
    //         const double p_dxy[] = {};
    //         const double p_dsz[] = {};
    //         const double p_dxydsz[] = {};
    //       }
        
    //       scales_.set(,
    //                   ,

    //                   );
    //     }
    //   }


  void TrackRescaler_wLep::set_SingleLep2018(double x, double eta, std::string type) {
    if (fabs(eta) < 1.5) {
      if (type == "") {
        const double p_dxy[7] = {1.03112461560515, 0.027939954186664222, -0.0024777135470085247, 1.1198254046663294, -0.0013579297509143465, 1.0600577441006154, 6.09296042624434e-05};
        const double p_dsz[7] = {1.0800117878149493, 0.013423192619346155, 1.1340111602074219, -0.0013106472963789876, 1.1196923400312397, 3.2650883372812786e-05, -7.481787581617157e-07};
        const double p_dxydsz[9] = {1.1423316786920164, -0.025569852427499856, -0.004756678626186833, 0.0006733460884134249, 0.9520196829959118, -0.001750557944344104, 0.0003240758473373313, 1.0499787839829393, 6.349483450061242e-05};

        scales_.set( (x<=6)*(p_dxy[0]+p_dxy[1]*x+p_dxy[2]*pow(x,2))+(x>=6&&x<=44)*(p_dxy[3]+p_dxy[4]*x)+(x>=44&&x<=200)*(p_dxy[5]+p_dxy[6]*x)+(x>200)*(p_dxy[5]+p_dxy[6]*x),
                     (x<=4)*(p_dsz[0]+p_dsz[1]*x)+(x>=4&&x<=10)*(p_dsz[2]+p_dsz[3]*x)+(x>=10&&x<=200)*(p_dsz[4]+p_dsz[5]*x+p_dsz[6]*pow(x,2))+(x>200)*(p_dsz[4]+p_dsz[5]*x+p_dsz[6]*pow(x,2)),
                     (x<=8)*(p_dxydsz[0]+p_dxydsz[1]*x+p_dxydsz[2]*pow(x,2)+p_dxydsz[3]*pow(x,3))+(x>=8&&x<=18)*(p_dxydsz[4]+p_dxydsz[5]*x+p_dxydsz[6]*pow(x,2))+(x>=18&&x<=200)*(p_dxydsz[7]+p_dxydsz[8]*x)+(x>200)*(p_dxydsz[7]+p_dxydsz[8]*x)
        );

      }
      if (type == "electron") {
        const double p_dxy[2] = {1.099165067126334, 0.00018389219215817973};
        const double p_dsz[2] = {1.082789131643491, 3.772593088459831e-05};
        const double p_dxydsz[5] = {1.7127876374625464, -0.034731212907271755, 0.0003816857926977358, 0.896242742480523, 0.0013219868022166306}; 

        scales_.set((x>=20&&x<=200)*(p_dxy[0]+p_dxy[1]*x)+(x>200)*(p_dxy[0]+p_dxy[1]*x),
                    (x>=20&&x<=200)*(p_dsz[0]+p_dsz[1]*x)+(x>200)*(p_dsz[0]+p_dsz[1]*x),
                    (x>=20&&x<=56)*(p_dxydsz[0]+p_dxydsz[1]*x+p_dxydsz[2]*pow(x,2))+(x>56&&x<=200)*(p_dxydsz[3]+p_dxydsz[4]*x)+(x>200)*(p_dxydsz[3]+p_dxydsz[4]*x)
        );
      }
      if (type == "muon") {
        const double p_dxy[2] = {1.0771137416042647, -0.0002944517341002609};
        const double p_dsz[2] = {1.0980008599346949, -4.3607720433033736e-05};
        const double p_dxydsz[5] = {0.8873675573834777, 0.00651830296147308, -6.333660048737822e-05, 1.0357490911388614, 0.000291023640918533};

        scales_.set((x>=20&&x<=200)*(p_dxy[0]+p_dxy[1]*x)+(x>200)*(p_dxy[0]+p_dxy[1]*x),
                    (x>=20&&x<=200)*(p_dsz[0]+p_dsz[1]*x)+(x>200)*(p_dsz[0]+p_dsz[1]*x),
                    (x>=20&&x<=56)*(p_dxydsz[0]+p_dxydsz[1]*x+p_dxydsz[2]*pow(x,2))+(x>56&&x<=200)*(p_dxydsz[3]+p_dxydsz[4]*x)+(x>200)*(p_dxydsz[3]+p_dxydsz[4]*x)
                    );
      }

    }
    else {
      if (type == "") {
        const double p_dxy[7] = {1.0133027312506913, 0.022318204661493413, 1.0132560573122338, 0.030203922649456587, -0.0011920662142896792, 1.2075301903740283, -0.0009030071324799313};
        const double p_dsz[7] = {1.0122428157879715, 0.007255082361121984, 1.0128200774147489, 0.00966372174191818, -0.00040699524051006656, 1.079658308344396, -0.0002488112151517263};
        const double p_dxydsz[11] = {1.3166283744401028, 0.08185582853274989, -0.02577622285830496, 0.0009324392251916928, 0.00011486069705164841, 1.2095572705954116, -0.007444915625685196, 0.0008944005459964158, -2.5539279747627624e-05, 0.9557625567755772, 0.002860260280510063}; // no values yet 

        scales_.set((x<=4)*(p_dxy[0]+p_dxy[1]*x)+(x>=4&&x<=15)*(p_dxy[2]+p_dxy[3]*x+p_dxy[4]*pow(x,2))+(x>=15&&x<=200)*(p_dxy[5]+p_dxy[6]*x)+(x>200)*(p_dxy[5]+p_dxy[6]*x),
                    (x<=4)*(p_dsz[0]+p_dsz[1]*x)+(x>=4&&x<=15)*(p_dsz[2]+p_dsz[3]*x+p_dsz[4]*pow(x,2))+(x>=15&&x<=200)*(p_dsz[5]+p_dsz[6]*x)+(x>200)*(p_dsz[5]+p_dsz[6]*x),
                    (x<=8)*(p_dxydsz[0]+p_dxydsz[1]*x+p_dxydsz[2]*pow(x,2)+p_dxydsz[3]*pow(x,3)+p_dxydsz[4]*pow(x,4))+(x>=8&&x<=32)*(p_dxydsz[5]+p_dxydsz[6]*x+p_dxydsz[7]*pow(x,2)+p_dxydsz[8]*pow(x,3))+(x>=32&&x<=200)*(p_dxydsz[9]+p_dxydsz[10]*x)+(x>200)*(p_dxydsz[9]+p_dxydsz[10]*x)
                    );
      }
      if (type == "electron") {
        const double p_dxy[2] = {1.1751514975615347, -0.0003876098750689068};
        const double p_dsz[2] = {1.064929992984938, 0.00010390378131054125};
        const double p_dxydsz[2] = {1.202563534368814, -0.001312167352572044}; // no values yet 

        scales_.set((x>=20&&x<=200)*(p_dxy[0]+p_dxy[1]*x)+(x>200)*(p_dxy[0]+p_dxy[1]*x),
                    (x>=20&&x<=200)*(p_dsz[0]+p_dsz[1]*x)+(x>200)*(p_dsz[0]+p_dsz[1]*x),
                    (x>=20&&x<=200)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>200)*(p_dxydsz[0]+p_dxydsz[1]*x)
                    );
      }
      if (type == "muon") {
        const double p_dxy[2] = {1.171998902227447, -0.00020640715873641857};
        const double p_dsz[2] = {1.056127201515852, -3.531929262842737e-05};
        const double p_dxydsz[2] = {1.1176629427965068, 0.0003558852632608422};

        scales_.set((x>=20&&x<=200)*(p_dxy[0]+p_dxy[1]*x)+(x>200)*(p_dxy[0]+p_dxy[1]*x),
                    (x>=20&&x<=200)*(p_dsz[0]+p_dsz[1]*x)+(x>200)*(p_dsz[0]+p_dsz[1]*x),
                    (x>=20&&x<=200)*(p_dxydsz[0]+p_dxydsz[1]*x)+(x>200)*(p_dxydsz[0]+p_dxydsz[1]*x)
                    );
      }

    }
  }


  void TrackRescaler_wLep::set(double era, int /*which*/, double pt, double eta, std::string type) {
    if (enable()) {
        //   if      (era == jmt::AnalysisEras::e_2017B || era == jmt::AnalysisEras::e_2017C || 
        //            era == jmt::AnalysisEras::e_2017D || era == jmt::AnalysisEras::e_2017E || era == jmt::AnalysisEras::e_2017F) set_SingleLep2017(pt, eta, type)
        if (era == jmt::AnalysisEras::e_2018A || era == jmt::AnalysisEras::e_2018B || 
            era == jmt::AnalysisEras::e_2018C || era == jmt::AnalysisEras::e_2018D) set_SingleLep2018(pt, eta, type);
      else throw std::out_of_range("bad era");
    }
    else
      scales_.reset();
  }

  TrackRescaler_wLep::ret_t TrackRescaler_wLep::scale(const reco::Track& tk, std::string type) {
    ret_t r;
    r.tk = tk;
    if (enable()) {
      set(era_, which_, tk.pt(), tk.eta(), type);
      reco::TrackBase::CovarianceMatrix cov = tk.covariance();

      const int i_dxy = reco::TrackBase::i_dxy;
      const int i_dsz = reco::TrackBase::i_dsz;

      for (int idim = 0; idim < reco::TrackBase::dimension; ++idim) {
        if (idim == i_dxy) cov(idim, i_dxy) *= scales_.dxycov();
        else               cov(idim, i_dxy) *= scales_.dxyerr();
      }

      for (int idim = 0; idim < reco::TrackBase::dimension; ++idim) {
        if (idim == i_dsz) cov(idim, i_dsz) *= scales_.dszcov();
        else               cov(idim, i_dsz) *= scales_.dszerr();
      }

      cov(i_dxy, i_dsz) *= scales_.dxydszcov();

      r.rescaled_tk = reco::Track(tk.chi2(), tk.ndof(), tk.referencePoint(), tk.momentum(), tk.charge(), cov, tk.algo());
      r.rescaled_tk.setQualityMask(tk.qualityMask());
      r.rescaled_tk.setNLoops(tk.nLoops());
      (*const_cast<reco::HitPattern*>(&r.rescaled_tk.hitPattern())) = tk.hitPattern(); // lmao
    }
    else
      r.rescaled_tk = tk;

    return r;
  }
}
