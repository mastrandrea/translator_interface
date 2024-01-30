
# Interface description
from interfaceDictionary import interfaceDictionary

#dictionaryFileName = "nanoAOD_db.json"
dictionaryFileName = "nanoAOD_db_BB.json"

t = interfaceDictionary("nanoAOD2nanoAOD_test_interface")
t.set_comments("Test interface for nanoAOD->nanoAOD format translation")

#t.print_summary()

t.set_base_format("scalar",     "VARIABLE")
t.set_base_format("vector",     "VARIABLE[INDEX]")
t.set_base_format("object",     "VARIABLE_FEATURE")
t.set_base_format("collection", "VARIABLE_FEATURE[INDEX]")


t.set_target_format("scalar",     "VARIABLE")
t.set_target_format("vector",     "VARIABLE[INDEX]")
t.set_target_format("object",     "VARIABLE_FEATURE")
t.set_target_format("collection", "VARIABLE_FEATURE[INDEX]")

#t.set_target_format("scalar",     "VARIABLE")
#t.set_target_format("vector",     "VARIABLE[INDEX]")
#t.set_target_format("object",     "VARIABLE.FEATURE")
#t.set_target_format("collection", "VARIABLE[INDEX].FEATURE")



## Scalar variables (no index, no variables)
#t.add_scalar("nMuon",  "nMuon")
#
## Vector variables (index, no feature)
##t.add_vector("vector1",  "VECTOR1")
#
## Object variables (no index, feature)
##t.add_object("Obj1", "OBJ1")
##t.add_feature("Obj1", "x1", "X1")
##t.add_feature("Obj1", "y1", "Y2")
#
#
## Collection variables (index, feature)
#t.add_collection("Muon", "Muon")
#t.add_feature("Muon", "pt",        "pt")
#t.add_feature("Muon", "eta",       "eta")
#t.add_feature("Muon", "iso",       "iso")
#t.add_feature("Muon", "mediumId",  "mediumId")
#
##t.add_feature("Muon", "",  "")



### Run & event

t.add_variable("BBrun",  "run")
t.add_variable("BBluminosityBlock", "luminosityBlock")
t.add_variable("BBevent",  "event")


### HLT

t.add_variable("BBHLT", "HLT")
t.add_feature("BBHLT", "IsoMu24_eta2p1",                 "IsoMu24_eta2p1")
t.add_feature("BBHLT", "IsoMu24",                        "IsoMu24")
t.add_feature("BBHLT", "IsoMu17_eta2p1_LooseIsoPFTau20", "IsoMu17_eta2p1_LooseIsoPFTau20")


### PV

t.add_variable("BBPV", "PV")
t.add_feature("BBPV", "npvs", "npvs")
t.add_feature("BBPV", "x",    "x")
t.add_feature("BBPV", "y",    "y")
t.add_feature("BBPV", "z",    "z")


### Muon

t.add_variable("BBMuon", "Muon")
t.add_variable("BBnMuon", "nMuon")
t.add_feature("BBMuon", "pt",             "pt")
t.add_feature("BBMuon", "eta",            "eta")
t.add_feature("BBMuon", "phi",            "phi")
t.add_feature("BBMuon", "mass",           "mass")
t.add_feature("BBMuon", "charge",         "charge")
t.add_feature("BBMuon", "pfRelIso03_all", "pfRelIso03_all")
t.add_feature("BBMuon", "pfRelIso04_all", "pfRelIso04_all")
t.add_feature("BBMuon", "tightId",        "tightId")
t.add_feature("BBMuon", "softId",         "softId")
t.add_feature("BBMuon", "dxy",            "dxy")
t.add_feature("BBMuon", "dxyErr",         "dxyErr")
t.add_feature("BBMuon", "dz",             "dz")
t.add_feature("BBMuon", "dzErr",          "dzErr")
t.add_feature("BBMuon", "jetIdx",         "jetIdx")
t.add_feature("BBMuon", "genPartIdx",     "genPartIdx")

#t.add_feature("BBMuon", "iso",            "iso")
#t.add_feature("BBMuon", "mediumId",       "mediumId")


### Electron

t.add_variable("BBElectron", "Electron")
t.add_variable("BBnElectron", "nElectron")
t.add_feature("BBElectron", "pt",             "pt")
t.add_feature("BBElectron", "eta",            "eta")
t.add_feature("BBElectron", "phi",            "phi")
t.add_feature("BBElectron", "mass",           "mass")
t.add_feature("BBElectron", "charge",         "charge")
t.add_feature("BBElectron", "pfRelIso03_all", "pfRelIso03_all")
t.add_feature("BBElectron", "dxy",             "dxy")
t.add_feature("BBElectron", "dxyErr",          "dxyErr")
t.add_feature("BBElectron", "dz",              "dz")
t.add_feature("BBElectron", "dzErr",           "dzErr")
t.add_feature("BBElectron", "cutBasedId",      "cutBasedId")
t.add_feature("BBElectron", "pfId",            "pfId")
t.add_feature("BBElectron", "jetIdx",          "jetIdx")
t.add_feature("BBElectron", "genPartIdx",      "genPartIdx")


### Tau

t.add_variable("BBTau", "Tau")
t.add_variable("BBnTau", "nTau")
t.add_feature("BBTau", "pt",              "pt")
t.add_feature("BBTau", "eta",             "eta")
t.add_feature("BBTau", "phi",             "phi")
t.add_feature("BBTau", "mass",            "mass")
t.add_feature("BBTau", "charge",          "charge")
t.add_feature("BBTau", "decayMode",       "decayMode")
t.add_feature("BBTau", "relIso_all",      "relIso_all")
t.add_feature("BBTau", "jetIdx",          "jetIdx")
t.add_feature("BBTau", "genPartIdx",      "genPartIdx")
t.add_feature("BBTau", "idDecayMode",     "idDecayMode")
t.add_feature("BBTau", "idIsoRaw",        "idIsoRaw")
t.add_feature("BBTau", "idIsoVLoose",     "idIsoVLoose")
t.add_feature("BBTau", "idIsoLoose",      "idIsoLoose")
t.add_feature("BBTau", "idIsoMedium",     "idIsoMedium")
t.add_feature("BBTau", "idIsoTight",      "idIsoTight")
t.add_feature("BBTau", "idAntiEleLoose",  "idAntiEleLoose")
t.add_feature("BBTau", "idAntiEleMedium", "idAntiEleMedium")
t.add_feature("BBTau", "idAntiEleTight",  "idAntiEleTight")
t.add_feature("BBTau", "idAntiMuLoose",   "idAntiMuLoose")
t.add_feature("BBTau", "idAntiMuMedium",  "idAntiMuMedium")
t.add_feature("BBTau", "idAntiMuTight",   "idAntiMuTight")


### Photon

t.add_variable("BBPhoton", "Photon")
t.add_variable("BBnPhoton", "nPhoton")
t.add_feature("BBPhoton", "pt",             "pt")
t.add_feature("BBPhoton", "eta",            "eta")
t.add_feature("BBPhoton", "phi",            "phi")
t.add_feature("BBPhoton", "mass",           "mass")
t.add_feature("BBPhoton", "charge",         "charge")
t.add_feature("BBPhoton", "pfRelIso03_all", "pfRelIso03_all")
t.add_feature("BBPhoton", "jetIdx",          "jetIdx")
t.add_feature("BBPhoton", "genPartIdx",      "genPartIdx")


### MET

t.add_variable("BBMET", "MET")
t.add_feature("BBMET", "pt",           "pt")
t.add_feature("BBMET", "phi",          "phi")
t.add_feature("BBMET", "sumet",        "sumet")
t.add_feature("BBMET", "significance", "significance")
t.add_feature("BBMET", "CovXX",        "CovXX")
t.add_feature("BBMET", "CovXY",        "CovXY")
t.add_feature("BBMET", "CovYY",        "CovYY")


### Jet

t.add_variable("BBJet", "Jet")
t.add_variable("BBnJet", "nJet")
t.add_feature("BBJet", "pt",   "pt")
t.add_feature("BBJet", "eta",  "eta")
t.add_feature("BBJet", "phi",  "phi")
t.add_feature("BBJet", "mass", "mass")
t.add_feature("BBJet", "puId", "puId")
t.add_feature("BBJet", "btag", "btag")


t.save_DB(dictionaryFileName)

print("\n ---------------------------- print_dictionary ")
t.print_dictionary()

print("\n ---------------------------- print_summary ")
t.print_summary()
