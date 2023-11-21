
# Interface description
from interfaceDictionary import interfaceDictionary

dictionaryFileName = "db.json"

t = interfaceDictionary("i1_test")
t.set_comments("Test interface - comment here")

#t.print_summary()

t.set_target_format("scalar",     "VARIABLE")
t.set_target_format("vector",     "VARIABLE[INDEX]")
t.set_target_format("object",     "VARIABLE_FEATURE")
t.set_target_format("collection", "VARIABLE_FEATURE[INDEX]")



# Scalar variables (no index, no variables)
t.add_scalar("scalar1",  "SCALAR1")
t.add_scalar("scalar_2", "SCALAR_2")
t.add_scalar("s",        "S")


# Vector variables (index, no feature)
t.add_vector("vector1",  "VECTOR1")
t.add_vector("vector_2", "VECTOR_2")


# Object variables (no index, feature)
t.add_object("Obj1", "OBJ1")
t.add_feature("Obj1", "x1", "X1")
t.add_feature("Obj1", "y1", "Y2")


# Collection variables (index, feature)
t.add_collection("Col1", "COL1")
t.add_feature("Col1", "pt",  "PT")
t.add_feature("Col1", "eta", "ETA")
t.add_feature("Col1", "phi", "PHI")
t.add_feature("Col1", "a",   "A")
t.add_feature("Col1", "a_b", "A_B")

t.add_collection("Col2", "COL2")
t.add_feature("Col2", "pt",  "PT")
t.add_feature("Col2", "eta", "ETA")
t.add_feature("Col2", "phi", "PHI")

t.add_collection("Col3", "Col3")
t.add_feature("Col3", "pt",  "pt")
t.add_feature("Col3", "eta", "eta")
t.add_feature("Col3", "phi", "phi")

t.save_DB(dictionaryFileName)

print("\n ---------------------------- print_dictionary ")
t.print_dictionary()

print("\n ---------------------------- print_summary ")
t.print_summary()
