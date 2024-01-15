
# Interface description
#from interfaceDictionary import interfaceDictionary

# Translator tool
from translator import translator


###################################
# Test
###################################

dbFile = 'db.json'

print("")
tX = translator(dbFile)

#tI.configureInterface()


tX.ID.add_feature("Col2", "abc", "ABC")


def test_translate(tX, sTest):
    print("")
    print("....................   0         1         2         3         4         5         6         7         8")
    print("....................   012345678901234567890123456789012345678901234567890123456789012345678901234567890")
    print("Input string        = ", sTest)
    print("Translated string   = ", tX.translate_string(sTest))
    print("")



test_translate(tX, "scalar_222 = header+Col2_pt[2]-scalar1/scalar_1-scalar_21+scalar_2_ +ascalar_2+s-1 * vec_abc[5] = Col3_pt[scalar2 - 3. Col1_eta[2]] + Obj1_x1 - footer s")




### Test strings

test_translate(tX, "1 && Jet[Jet_ind[0]].pt > 20 && Jet_eta[1] < 1.2")
test_translate(tX, "1 && Jet_pt[0] > 20 && Jet_eta[1] < 1.2")
test_translate(tX, "Best Col2_pt[0] > 20")

test_translate(tX, "header  Col1_pt[alpha_index] > 20 footer")
test_translate(tX, "header  Col1_pt[Col2_phi[2]] > 20 footer")
test_translate(tX, "header  Col1_pt[3.0 * fun(Col2_phi[2] + 2)] > 20 && Col1_pt[10] = 3. footer")

#### Base test
test_translate(tX, "header  Col1_a_b[3.0 * fun(Col2_phi[2] + 2)] > 20 && Col2_abc[10] = 3. footer")

test_translate(tX, "header  Col1_a_b_c_d[3.0 * fun(Col2_phi[2] + 2)] > 20 && Col2_abc[10] = 3. footer")

### base
test_translate(tX, "header  Col1_pt[3.0 * fun(Col2_phi[2] + 2 * vec[5])]> 20 && Col2[10] = 3. footer")

### Test with unmapped feature
test_translate(tX, "header  Col1_a_b[3.0 * fun(Col2_phi[2] + 2)] > 20 && Col2_alpha[10] = 3. footer")


#---------- Scalar

test_translate(tX, "header + scalar1 / scalar_1 - scalar2 * vec_abc[5] = 3. footer")



#---------- Error conditions check

# reference
test_translate(tX, "header + scalar1 + vector1[0] + Obj1_x1 + Col1_pt[0] + footer")


# scalar with index
test_translate(tX, "header + scalar1[0] + vector1[0] + Obj1_x1 + Col1_pt[0] + footer")

# scalar with feature
test_translate(tX, "header + scalar1_pt + vector1[0] + Obj1_x1 + Col1_pt[0] + footer")

# scalar with index and feature
test_translate(tX, "header + scalar1_pt[0] + vector1[0] + Obj1_x1 + Col1_pt[0] + footer")



# vector with NO index
test_translate(tX, "header + scalar1 + vector1 + Obj1_x1 + Col1_pt[0] + footer")

# vector with feature
test_translate(tX, "header + scalar1 + vector1_pt[0] + Obj1_x1 + Col1_pt[0] + footer")

# vector with NO index and feature
test_translate(tX, "header + scalar1 + vector1_pt + Obj1_x1 + Col1_pt[0] + footer")



# object with index
test_translate(tX, "header + scalar1 + vector1[0] + Obj1_x1[0] + Col1_pt[0] + footer")

# object with NO feature
test_translate(tX, "header + scalar1 + vector1[0] + Obj1 + Col1_pt[0] + footer")

# object with index and NO feature
test_translate(tX, "header + scalar1 + vector1[0] + Obj1[0] + Col1_pt[0] + footer")



# collection with NO index
test_translate(tX, "header + scalar1 + vector1[0] + Obj1_x1 + Col1_pt + footer")

# collection with NO feature
test_translate(tX, "header + scalar1 + vector1[0] + Obj1_x1 + Col1[0] + footer")

# collection with NO index and NO feature
test_translate(tX, "header + scalar1 + vector1[0] + Obj1_x1 + Col1 + footer")


# test of the "SKIP" feature for variables with index - [] -> no index in the translated string
test_translate(tX, "header + scalar1 + vector1[] + Obj1_x1 + Col1_pt[] + footer")


