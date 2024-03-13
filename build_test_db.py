
# Interface description
from interfaceDictionary import interfaceDictionary

dictionaryFileName = "test_db.json"

t = interfaceDictionary("NANOAOD2nanoAOD_test_interface")
t.set_comment("Test interface: ALL_CAPITAL nanoAOD -> nanoAOD dictionary")

#t.set_base_format("scalar",     "VARIABLE")
#t.set_base_format("vector",     "VARIABLE[INDEX]")
#t.set_base_format("object",     "VARIABLE_FEATURE")
#t.set_base_format("collection", "VARIABLE_FEATURE[INDEX]")


t.set_target_format("scalar",     "VARIABLE")
t.set_target_format("vector",     "VARIABLE[INDEX]")
t.set_target_format("object",     "VARIABLE_FEATURE")
t.set_target_format("collection", "VARIABLE_FEATURE[INDEX]")
t.set_target_format("counter",    "nVARIABLE")


### Muon

t.add_variable("MUON", "Muon")
t.add_variable("nMUON", "nMuon")
t.add_feature("MUON", "PT",             "pt")
t.add_feature("MUON", "ETA",            "eta")
t.add_feature("MUON", "PHI",            "phi")
t.add_feature("MUON", "MASS",           "mass")
t.add_feature("MUON", "CHARGE",         "charge")
t.add_feature("MUON", "PFRELISO03_ALL", "pfRelIso03_all")
t.add_feature("MUON", "PFRELISO04_ALL", "pfRelIso04_all")
t.add_feature("MUON", "TIGHTID",        "tightId")
t.add_feature("MUON", "SOFTID",         "softId")
t.add_feature("MUON", "DXY",            "dxy")
t.add_feature("MUON", "DXYERR",         "dxyErr")
t.add_feature("MUON", "DZ",             "dz")
t.add_feature("MUON", "DZERR",          "dzErr")
t.add_feature("MUON", "JETIDX",         "jetIdx")
t.add_feature("MUON", "GENPARTIDX",     "genPartIdx")


t.save_DB(dictionaryFileName)

print("\n ---------------------------- print_dictionary ")
t.print_dictionary()

print("\n ---------------------------- print_summary ")
t.print_summary()
