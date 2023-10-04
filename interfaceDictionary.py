##
##     var_name[index].feature
##
## Types of codification for variables:
##  - Scalar:     no index, no feature         e.g. RunNumber
##  - Vector:        INDEX, no feature         e.g. MC_weights[i]
##  - Object:     no index,    FEATURE         e.g. MET.x, MET.y
##  - Collection:    INDEX,    FEATURE         e.e. electron[i].pT
##
##

class testInterface:
    def __init__(self, t1 = "testInterface"):
        self.name = t1
        print("[",self.name,"] testInterface object created")

        self.types             = ("scalar", "vector", "object", "collection")
        self.typesWithIndex    = ("vector", "collection")
        self.typesWithFeature  = ("object", "collection")

        self.SCALARs_dict      = {}
        self.VECTORs_dict      = {}
        self.OBJECTs_dict      = {}
        self.COLLECTIONs_dict  = {}

        self.dictionaries_dict = {}
        self.variables_dict    = {}

        self.__define_dictionaries__()
        self.__build_derived_dictionaries__()


    def __str__(self):
        return "[ "+self.name+" ] Interface class for test format input files"


    # Placeholder for input-format-specific configurations
    def configureInterface(self):
        print("[",self.name,"] Placeholder for input-format-specific configurations")



    #---#  Utilities for variables

    def is_defined(self, var_name):
        return (var_name in self.variables_dict)


    def type_with_features(self, var_type):
        return (var_type in self.typesWithFeature)


    def type_with_index(self, var_type):
        return (var_type in self.typesWithIndex)


    def has_this_feature(self, var_name, feature_name):
        vT = self.get_type(var_name)
        return (feature_name in self.dictionaries_dict[vT][var_name])


    def get_type(self, var_name):
        return self.variables_dict[var_name]



    #---#  Utilities for dictionaries

    def __build_derived_dictionaries__(self):

        self.dictionaries_dict["scalar"]     = self.SCALARs_dict
        self.dictionaries_dict["vector"]     = self.VECTORs_dict
        self.dictionaries_dict["object"]     = self.OBJECTs_dict
        self.dictionaries_dict["collection"] = self.COLLECTIONs_dict

        for _vt in self.types:
            for _var in self.dictionaries_dict[_vt]:
                self.variables_dict[_var] = _vt



    def dictionary_for(self, _var):
        
        if self.is_defined(_var):
            _var_type = self.get_type(_var)

            if self.type_with_features(_var_type):
                return self.dictionaries_dict[_var_type][_var]
            else:
                return self.dictionaries_dict[_var_type]

        print(" ERROR  -  variable ", _var, "  not defined in any dictionary!")
        return {}


    def __print_dict(self, d1):
        for v in d1:
            print(v.ljust(20), "-->", d1[v])
        return


    def print_dictionary(self, _name):

        print(">> Dictionary  ", _name)

        if _name in self.types:
            _d = self.dictionaries_dict[_name]
        else:
            _d = self.dictionary_for(_name)

        self.__print_dict(_d)

        return





    ########### Dictionaries definition

    def __define_dictionaries__(self):

        # Scalar variables (no index, no variables)
        self.SCALARs_dict["scalar1"]  = "SCALAR1"
        self.SCALARs_dict["scalar_2"] = "SCALAR_2"
        self.SCALARs_dict["s"]        = "S"

        # Vector variables (index, no feature)
        self.VECTORs_dict["vector1"]  = "VECTOR1"
        self.VECTORs_dict["vector_2"] = "VECTOR_2"

        # Object variables (no index, feature)
        self.Obj1_dict = {}
        self.Obj1_dict["VAR_NAME"] = "OBJ1"
        self.Obj1_dict["x1"] = "X1"
        self.Obj1_dict["y1"] = "Y2"

        self.OBJECTs_dict["Obj1"] = self.Obj1_dict

        # Collection variables (index, feature)
        self.Col1_dict = {}
        self.Col1_dict["VAR_NAME"] = "COL1"
        self.Col1_dict["pt"]  = "PT"
        self.Col1_dict["eta"] = "ETA"
        self.Col1_dict["phi"] = "PHI"
        self.Col1_dict["a"]   = "A"
        self.Col1_dict["a_b"] = "A_B"

        self.Col2_dict = {}
        self.Col2_dict["VAR_NAME"] = "COL2"
        self.Col2_dict["pt"]  = "PT"
        self.Col2_dict["eta"] = "ETA"
        self.Col2_dict["phi"] = "PHI"

        self.Col3_dict = {}
        self.Col3_dict["VAR_NAME"] = "Col3"
        self.Col3_dict["pt"]  = "pt"
        self.Col3_dict["eta"] = "eta"
        self.Col3_dict["phi"] = "phi"

        self.COLLECTIONs_dict["Col1"] = self.Col1_dict
        self.COLLECTIONs_dict["Col2"] = self.Col2_dict
        self.COLLECTIONs_dict["Col3"] = self.Col3_dict


    # Target:   name             -> NAME
    # Target:   name[index]      -> NAME[index]
    # Target:   name.feat        -> NAME_FEAT
    # Target:   name[index].feat -> NAME_FEAT[index]

    #
    # Could be implemented in 2 stages: translate to target dictionary + build
    #

    def convert(self, sVar, sInd, sFeat):

        typeVar = self.variables_dict[sVar]

        convString = ""

        if not typeVar in self.typesWithFeature:
            convString = self.dictionaries_dict[typeVar][sVar]
        else:
            convString =      self.dictionaries_dict[typeVar][sVar]["VAR_NAME"]
            convString += '_'+self.dictionaries_dict[typeVar][sVar][sFeat]

        if typeVar in self.typesWithIndex:
            convString += '['+sInd+']'

        return convString

# Built-in hash() function in Pyton is "salted" by a random mumber (unique per execution)
# (see: https://docs.python.org/3/reference/datamodel.html#object.__hash__ )
#    def hash_dict(self):
#        return hash(str(self.OBJs_dict))
