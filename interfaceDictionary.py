
class testInterface:
    def __init__(self, t1 = "testInterface"):
        self.name = t1
        print("[",self.name,"] testInterface object created")
        self.__define_dictionaries__()

    def __str__(self):
        return "[ "+self.name+" ] Interface class for test format input files"

    # Placeholder for input-format-specific configurations
    def configureInterface(self):
        print("[",self.name,"] Placeholder for input-format-specific configurations")


    def __define_dictionaries__(self):
        self.Obj1_dict = {}
        self.Obj1_dict["OBJECT_NAME"] = "OBJ1"
        self.Obj1_dict["pt"]  = "PT"
        self.Obj1_dict["eta"] = "ETA"
        self.Obj1_dict["phi"] = "PHI"
        self.Obj1_dict["a"]   = "A"
        self.Obj1_dict["a_b"] = "A_B"

        self.Obj2_dict = {}
        self.Obj2_dict["OBJECT_NAME"] = "OBJ2"
        self.Obj2_dict["pt"]  = "PT"
        self.Obj2_dict["eta"] = "ETA"
        self.Obj2_dict["phi"] = "PHI"

        self.OBJs_dict = {}
        self.OBJs_dict["Obj1"] = self.Obj1_dict
        self.OBJs_dict["Obj2"] = self.Obj2_dict



    def convert(self, sObj, sInd, sFeat):

        tObj  = self.OBJs_dict[sObj]["OBJECT_NAME"]
        tFeat = self.OBJs_dict[sObj][sFeat]

        convString = tObj+'_'+tFeat+'['+sInd+']'

        return convString

# Built-in hash() function in Pyton is "salted" by a random mumber (unique per execution)
# (see: https://docs.python.org/3/reference/datamodel.html#object.__hash__ )
#    def hash_dict(self):
#        return hash(str(self.OBJs_dict))
