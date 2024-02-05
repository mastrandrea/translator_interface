
# Interface description
#from interfaceDictionary import interfaceDictionary

# Translator tool
from translator import translator


###################################
# Test
###################################

dbFile = 'nanoAOD_db_BB.json'

print("")
tX = translator(dbFile)
#tX = translator("NO_TRANSLATION")

#tI.configureInterface()




def test_translate(tX, sTest, targetResult=""):
    print("")
    print("....................   0         1         2         3         4         5         6         7         8")
    print("....................   012345678901234567890123456789012345678901234567890123456789012345678901234567890")
    print("Input string        = ", sTest)
    s2 = tX.translate_string(sTest)
    print("Translated string   = ", s2)
    v2 = tX.get_var_list(sTest)
    print("Variables list      = ", v2)
    if not targetResult == "":
        print("Expected output     = ", targetResult, "       Match = ",(targetResult == s2))
    print("")



#x1 = "BBMuon_iso < 0.25 && BBMuon_mediumId && BBMuon_pt > 20. && abs(BBMuon_eta) < 2.4"
#x2 = "BBMuon[].iso < 0.25 && BBMuon[].mediumId && BBMuon[].pt > 20. && abs(BBMuon[].eta) < 2.4"
#
#test_translate(tX, x2)
#
#print("Expected output     = ", x1, "       Match = ",(x1 == tX.translate_string(x2)))
#
#y1 = "Nonzero(MuMu0_charge != MuMu1_charge)"
#
#test_translate(tX, y1)

d_target = {}
d_source = {}


#d_target["base"]  = "BBMuon_iso < 0.25 && BBMuon_mediumId && BBMuon_pt > 20. && abs(BBMuon_eta) < 2.4"
#d_source["base"]  = "BBMuon[].iso < 0.25 && BBMuon[].mediumId && BBMuon[].pt > 20. && abs(BBMuon[].eta) < 2.4"
#
#d_target["base1"] = "BBMuon_iso < 0.25 && BBMuon_mediumId && BBMuon_pt > 20. && abs(BBMuon_eta) < 2.4"
#d_source["base1"] = "BBMuon.iso < 0.25 && BBMuon.mediumId && BBMuon.pt > 20. && abs(BBMuon.eta) < 2.4"

#test_translate(tX, d_source["base"], d_target["base"])


# target ###################################################

d_target["BBMuon_m"]                  =  "0*Muon_pfRelIso04_all+0.1056f"
d_target["BBMuon_p4"]                 =  "vector_map_t<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > >(Muon_pt , Muon_eta, Muon_phi, Muon_m)"
d_target["BBMuon_iso"]                =  "Muon_pfRelIso04_all"

d_target["SelectedMuon"]              =  "Muon_iso < 0.25 && Muon_tightId && Muon_pt > 20. && abs(Muon_eta) < 2.4"

d_target["twoMuons"]                  =  "nSelectedMuon==2"

d_target["MuMu"]                      =  "SelectedMuon"

d_target["OppositeSignMuMu"]          =  "Nonzero(MuMu0_charge != MuMu1_charge)"

d_target["twoOppositeSignMuons"]      =  "OppositeSignMuMu.size() > 0"

d_target["Mu"]                        =  "At(OppositeSignMuMu,0,-200)"

d_target["Higgs_p4"]                  =  "Mu0_p4+Mu1_p4"
d_target["Higgs_m"]                   =  "Higgs_p4.M()"

d_target["SortedSelectedMuonIndices"] =  "Argsort(-SelectedMuon_pt)"
d_target["LeadMuon"]                  =  "SortedSelectedMuonIndices[0]"
d_target["SubMuon"]                   =  "SortedSelectedMuonIndices[1]"

d_target["PreSel"]                    =  "twoOppositeSignMuons && LeadMuon_pt > 26 && SubMuon_pt > 20  && abs(SubMuon_eta) <2.4 && abs(LeadMuon_eta) < 2.4"
d_target["MassWindow"]                =  "abs(Higgs_m-nominalHMass)<higgsMassWindowWidth"



# source ###################################################

# Define
d_source["BBMuon_m"]                    =  "0*BBMuon_pfRelIso04_all+0.1056f"
tX.add_to_dictionary("BBMuon_m")

d_source["BBMuon_p4"]                   =  "vector_map_t<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float> > >(BBMuon_pt , BBMuon_eta, BBMuon_phi, BBMuon_m)"
tX.add_to_dictionary("BBMuon_p4")

d_source["BBMuon_iso"]                  =  "BBMuon_pfRelIso04_all"
tX.add_to_dictionary("BBMuon_iso")

# Subcollection
d_source["SelectedMuon"]              =  "BBMuon_iso < 0.25 && BBMuon_tightId && BBMuon_pt > 20. && abs(BBMuon_eta) < 2.4"
tX.add_to_dictionary("SelectedMuon")
tX.add_features_from("SelectedMuon", "BBMuon")


# Selection
d_source["twoMuons"]                  =  "nSelectedMuon==2"
tX.add_to_dictionary("twoMuons")

# Distinct
d_source["MuMu"]                      =  "SelectedMuon"
tX.add_to_dictionary("MuMu_allpairs")
tX.add_to_dictionary("MuMu_ind")
tX.add_to_dictionary("MuMu0")
tX.add_features_from("MuMu0", "SelectedMuon")
tX.add_to_dictionary("MuMu1")
tX.add_features_from("MuMu1", "SelectedMuon")


# Define
d_source["OppositeSignMuMu"]          =  "Nonzero(MuMu0_charge != MuMu1_charge)"
tX.add_to_dictionary("OppositeSignMuMu")

# Selection
d_source["twoOppositeSignMuons"]      =  "OppositeSignMuMu.size() > 0"
tX.add_to_dictionary("twoOppositeSignMuons")

# TakePair
d_source["Mu"]                        =  "At(OppositeSignMuMu,0,-200)"
tX.add_to_dictionary("Mu_index")
tX.add_to_dictionary("Mu0")
tX.add_features_from("Mu0", "MuMu0")
tX.add_to_dictionary("Mu1")
tX.add_features_from("Mu1", "MuMu1")
    


# Define
d_source["Higgs_p4"]                  =  "Mu0_p4+Mu1_p4"
tX.add_to_dictionary("Higgs_p4")

d_source["Higgs_m"]                   =  "Higgs_p4.M()"
tX.add_to_dictionary("Higgs_m")

d_source["SortedSelectedMuonIndices"] =  "Argsort(-SelectedMuon_pt)"
tX.add_to_dictionary("SortedSelectedMuonIndices")


# ObjectAt
d_source["LeadMuon"]                  =  "SortedSelectedMuonIndices[0]"
tX.add_to_dictionary("LeadMuon")
tX.add_features_from("LeadMuon", "SelectedMuon")

d_source["SubMuon"]                   =  "SortedSelectedMuonIndices[1]"
tX.add_to_dictionary("SubMuon")
tX.add_features_from("SubMuon", "SelectedMuon")

# Selection
d_source["PreSel"]                    =  "twoOppositeSignMuons && LeadMuon_pt > 26 && SubMuon_pt > 20  && abs(SubMuon_eta) <2.4 && abs(LeadMuon_eta) < 2.4"
tX.add_to_dictionary("PreSel")

d_source["MassWindow"]                =  "abs(Higgs_m-nominalHMass)<higgsMassWindowWidth"
tX.add_to_dictionary("MassWindow")







for i in d_target:
    print("-------> ", i)
    test_translate(tX, d_source[i], d_target[i])


tX.ID.save_DB("out.json")

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
