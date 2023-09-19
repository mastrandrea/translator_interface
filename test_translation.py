
# Interface description
from interfaceDictionary import testInterface

# Translator tool
from translator import translator


###################################
# Test
###################################

print("")

tI  = testInterface('int_test_1')
tI2 = testInterface()


print(tI)
print("[",tI.name,"]",tI.OBJs_dict)

print("")

### Eventual additions
tI.OBJs_dict["Obj2"]["abc"] = "aBc"
#tI.OBJs_dict["Obj2"]["alpha"] = "ALPHA"
tI.OBJs_dict["Obj1"]["a_b_c_d"] = "A_B_C_D"

print("[",tI.name,"]",tI.OBJs_dict)
print("[",tI2.name,"]",tI2.OBJs_dict)

print("")

### Check of the dictionaries 
for obj in tI.OBJs_dict:
    print(obj)
    for feat in tI.OBJs_dict[obj]:
        print(obj, feat, "-->", (tI.OBJs_dict[obj])[feat])

print("")

tI.configureInterface()

print("")

#tX = translator()
#tX.set_interface(tI)

tX = translator(tI)

print("")

        

### Test strings

#test_string = "1 && Jet[Jet[0].ind].pt > 20 && Jet[1].eta < 1.2"
#test_string = "1 && Jet[0].pt > 20 && Jet[1].eta < 1.2"
#test_string = "Best Obj2[0].pt > 20"

#test_string = "header  Obj1[alpha_index].pt > 20 footer"
#test_string = "header  Obj1[Obj2[2].phi].pt > 20 footer"
#test_string = "header  Obj1[3.0 * fun(Obj2[2].phi + 2)].pt > 20 && Obj1[10].pt = 3. footer"

# Base test
#test_string = "header  Obj1[3.0 * fun(Obj2[2].phi + 2)].a_b > 20 && Obj2[10].abc = 3. footer"

##test_string = "header  Obj1[3.0 * fun(Obj2[2].phi + 2)].a_b_c_d > 20 && Obj2[10].abc = 3. footer"

test_string = "header  Obj1[3.0 * fun(Obj2[2].phi + 2 * vec[5])].a_b_c_d > 20 && Obj2[10].abc = 3. footer"

# Test with unmapped feature
#test_string = "header  Obj1[3.0 * fun(Obj2[2].phi + 2)].a_b > 20 && Obj2[10].alpha = 3. footer"


print("test_string       = ", test_string)
print("..................   01234567890123456789012345678901234567890")
print("..................   0         1         2         3         4")
print("")

#translated_string = translate_string(test_string)
translated_string = tX.translate_string(test_string)

print("")
print("test_string       = ", test_string)
print("translated_string = ", translated_string)
print("..................   01234567890123456789012345678901234567890")
print("..................   0         1         2         3         4")


