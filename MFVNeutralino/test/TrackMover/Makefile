include $(CMSSW_BASE)/src/JMTucker/MFVNeutralino/NtupleMakefile.in

SHADOWDEPS += utils.h

all: hists.exe histslow.exe histshigh.exe mctruth.exe tests.exe

hists.exe: hists.cc BTagSFHelper.o $(SHADOWDEPS)
	g++ -o $@ $< BTagSFHelper.o $(FLAGS)

histslow.exe: histslow.cc BTagSFHelper.o $(SHADOWDEPS)
	g++ -o $@ $< BTagSFHelper.o $(FLAGS)

histshigh.exe: histshigh.cc BTagSFHelper.o $(SHADOWDEPS)
	g++ -o $@ $< BTagSFHelper.o $(FLAGS)

BTagCalibrationStandalone.h:
	ln -sf $(CMSSW_RELEASE_BASE)/src/CondTools/BTau/test/BTagCalibrationStandalone.h BTagCalibrationStandalone.h

BTagCalibrationStandalone.cc:
	ln -sf $(CMSSW_RELEASE_BASE)/src/CondTools/BTau/test/BTagCalibrationStandalone.cpp BTagCalibrationStandalone.cc

BTagSFHelper.o: BTagCalibrationStandalone.cc BTagCalibrationStandalone.h BTagSFHelper.h 
	g++ -c -o $@ $< $(FLAGS) -Wno-deprecated-declarations

clean:	
	-rm -f *.exe *.o BTagCalibrationStandalone.*
