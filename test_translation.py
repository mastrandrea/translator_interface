
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
#    tX = translator(db_file)
    print("")
    print("....................   0         1         2         3         4         5         6         7         8")
    print("....................   012345678901234567890123456789012345678901234567890123456789012345678901234567890")
    print("Input string        = ", sTest)
    print("Translated string   = ", tX.translate_string(sTest))
    print("")



test_translate(tX, "scalar_222 = header+Col2[2].pt-scalar1/scalar_1-scalar_21+scalar_2_ +ascalar_2+s-1 * vec[5].abc = Col3[scalar_2 - 3. Col1[2].eta].pt + Obj1.x1 - footer s")




### Test strings

test_translate(tX, "1 && Jet[Jet[0].ind].pt > 20 && Jet[1].eta < 1.2")
test_translate(tX, "1 && Jet[0].pt > 20 && Jet[1].eta < 1.2")
test_translate(tX, "Best Col2[0].pt > 20")

test_translate(tX, "header  Col1[alpha_index].pt > 20 footer")
test_translate(tX, "header  Col1[Col2[2].phi].pt > 20 footer")
test_translate(tX, "header  Col1[3.0 * fun(Col2[2].phi + 2)].pt > 20 && Col1[10].pt = 3. footer")

#### Base test
test_translate(tX, "header  Col1[3.0 * fun(Col2[2].phi + 2)].a_b > 20 && Col2[10].abc = 3. footer")

test_translate(tX, "header  Col1[3.0 * fun(Col2[2].phi + 2)].a_b_c_d > 20 && Col2[10].abc = 3. footer")

### base
test_translate(tX, "header  Col1[3.0 * fun(Col2[2].phi + 2 * vec[5])].pt> 20 && Col2[10] = 3. footer")

### Test with unmapped feature
test_translate(tX, "header  Col1[3.0 * fun(Col2[2].phi + 2)].a_b > 20 && Col2[10].alpha = 3. footer")


#---------- Scalar

test_translate(tX, "header + scalar1 / scalar_1 - scalar_2 * vec[5].abc = 3. footer")



#---------- Error conditions check

# reference
test_translate(tX, "header + scalar1 + vector1[0] + Obj1.x1 + Col1[0].pt + footer")


# scalar with index
test_translate(tX, "header + scalar1[0] + vector1[0] + Obj1.x1 + Col1[0].pt + footer")

# scalar with feature
test_translate(tX, "header + scalar1.pt + vector1[0] + Obj1.x1 + Col1[0].pt + footer")

# scalar with index and feature
test_translate(tX, "header + scalar1[0].pt + vector1[0] + Obj1.x1 + Col1[0].pt + footer")



# vector with NO index
test_translate(tX, "header + scalar1 + vector1 + Obj1.x1 + Col1[0].pt + footer")

# vector with feature
test_translate(tX, "header + scalar1 + vector1[0].pt + Obj1.x1 + Col1[0].pt + footer")

# vector with NO index and feature
test_translate(tX, "header + scalar1 + vector1.pt + Obj1.x1 + Col1[0].pt + footer")



# object with index
test_translate(tX, "header + scalar1 + vector1[0] + Obj1[0].x1 + Col1[0].pt + footer")

# object with NO feature
test_translate(tX, "header + scalar1 + vector1[0] + Obj1 + Col1[0].pt + footer")

# object with index and NO feature
test_translate(tX, "header + scalar1 + vector1[0] + Obj1[0] + Col1[0].pt + footer")



# collection with NO index
test_translate(tX, "header + scalar1 + vector1[0] + Obj1.x1 + Col1.pt + footer")

# collection with NO feature
test_translate(tX, "header + scalar1 + vector1[0] + Obj1.x1 + Col1[0] + footer")

# collection with NO index and NO feature
test_translate(tX, "header + scalar1 + vector1[0] + Obj1.x1 + Col1 + footer")


