
# Interface description
from interfaceDictionary import testInterface

# Translator tool
from translator import translator


###################################
# Test
###################################

print("")

tI  = testInterface('int_test_1')
#tI2 = testInterface()


print(tI)
print("[",tI.name,"]",tI.COLLECTIONs_dict)

print("")

### Eventual additions
tI.COLLECTIONs_dict["Col2"]["abc"] = "aBc"
#tI.OBJs_dict["Obj2"]["alpha"] = "ALPHA"
tI.COLLECTIONs_dict["Col1"]["a_b_c_d"] = "A_B_C_D"

#print("[",tI.name,"]",tI.COLLECTIONs_dict)
#print("[",tI2.name,"]",tI2.COLLECTIONs_dict)

print("")

### Check of the dictionaries 
for col in tI.COLLECTIONs_dict:
    print(col)
    for feat in tI.COLLECTIONs_dict[col]:
        print(col, feat, "-->", (tI.COLLECTIONs_dict[col])[feat])

print("")

tI.configureInterface()

print("")

tX = translator(tI)

print("------------>>>>>>> variables_dict")
print(tI.variables_dict)
        
print("------------>>>>>>> dictionaries_dict")
print(tI.dictionaries_dict)



print("")
print("***")
print("***")
print("")
print("")
tX.tI.print_dictionary("scalar")
print("")
print("")
tX.tI.print_dictionary("vector")
print("")
print("")
tX.tI.print_dictionary("Obj1")
print("")
print("")
tX.tI.print_dictionary("Col1")
print("")
print("")
tX.tI.print_dictionary("Col3")
print("")
print("")
print("***")
print("***")
print("")

        

### Test strings

#test_string = "1 && Jet[Jet[0].ind].pt > 20 && Jet[1].eta < 1.2"
#test_string = "1 && Jet[0].pt > 20 && Jet[1].eta < 1.2"
#test_string = "Best Col2[0].pt > 20"

#test_string = "header  Col1[alpha_index].pt > 20 footer"
#test_string = "header  Col1[Col2[2].phi].pt > 20 footer"
#test_string = "header  Col1[3.0 * fun(Col2[2].phi + 2)].pt > 20 && Col1[10].pt = 3. footer"

# Base test
#test_string = "header  Col1[3.0 * fun(Col2[2].phi + 2)].a_b > 20 && Col2[10].abc = 3. footer"

##test_string = "header  Col1[3.0 * fun(Col2[2].phi + 2)].a_b_c_d > 20 && Col2[10].abc = 3. footer"

## base
#test_string = "header  Col1[3.0 * fun(Col2[2].phi + 2 * vec[5])].a_b_c_d > 20 && Col2[10].abc = 3. footer"

# Test with unmapped feature
#test_string = "header  Col1[3.0 * fun(Col2[2].phi + 2)].a_b > 20 && Col2[10].alpha = 3. footer"


#---------- Scalar

#test_string = "header + scalar1 / scalar_1 - scalar_2 * vec[5].abc = 3. footer"
test_string = "scalar_222 = header+Col2[2].pt-scalar1/scalar_1-scalar_21+scalar_2_ +ascalar_2+s-1 * vec[5].abc = Col3[scalar_2 - 3. Col1[2].eta].pt + Obj1.x1 - footer s"
#test_string = "header + scalar1[4] / scalar_1 - scalar_2 * vec[5].abc = 3. footer"

#---------- Vector



#---------- Object
#---------- Collection
#---------- Mixed





print("Input string        = ", test_string)
print("....................   012345678901234567890123456789012345678901234567890123456789012345678901234567890")
print("....................   0         1         2         3         4         5         6         7         8")
print("")

translated_string = tX.translate_string(test_string)

print("")
print("Input string        = ", test_string)
print("Translated string   = ", translated_string)
print("....................   012345678901234567890123456789012345678901234567890123456789012345678901234567890")
print("....................   0         1         2         3         4         5         6         7         8")



print(tX.tI.dictionary_for("scalar1"))
print(tX.tI.dictionary_for("scalar_2"))
print(tX.tI.dictionary_for("s"))
print(tX.tI.dictionary_for("vector1"))
print(tX.tI.dictionary_for("vector_2"))
print(tX.tI.dictionary_for("Obj1"))
print(tX.tI.dictionary_for("Col1"))
print(tX.tI.dictionary_for("Col2"))

print(tX.tI.dictionary_for("Col3"))

#print("Input string        = ", test_string)
#print("....................   012345678901234567890123456789012345678901234567890123456789012345678901234567890")
#print("....................   0         1         2         3         4         5         6         7         8")

#stringShift = 0
#
#while stringShift < len(test_string):
#
#    t1, t1_pos = tX.get_token(test_string[stringShift:])
#
#    stringShift += (t1_pos + len(t1))
#    print(t1+";  ", t1_pos, "  ", len(t1))
