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

## TO BE ADDED : info about the interface itself (i.e. name, comments - eventually date&time for creation/modification - to be checked ...)


import json

class testInterface:
    def __init__(self, interfaceName = "testInterface", db_file = ""):
        self.name = interfaceName
        print("[",self.name,"] testInterface object created")

        self.scalar_type     = "scalar"
        self.vector_type     = "vector"
        self.object_type     = "object"
        self.collection_type = "collection"
        self._TYPE_key       = "TYPE"

        self.types             = (self.scalar_type, self.vector_type, self.object_type, self.collection_type)
        self.typesWithIndex    = (                  self.vector_type,                   self.collection_type)
        self.typesWithFeature  = (                                    self.object_type, self.collection_type)


        #        self.scalar_target_format     = "VARIABLE"
        #        self.vector_target_format     = "VARIABLE[INDEX]"
        #        self.object_target_format     = "VARIABLE_FEATURE"
        #        self.collection_target_format = "VARIABLE_FEATURE[INDEX]"
        self.scalar_target_format     = "NOT_SET"
        self.vector_target_format     = "NOT_SET"
        self.object_target_format     = "NOT_SET"
        self.collection_target_format = "NOT_SET"


        self.vars_DB = {}

        if db_file != "":     self.load_DB(db_file)


    def __str__(self):
        return "[ "+self.name+" ] Interface class for test format input files"


    # Placeholder for input-format-specific configurations
    def configureInterface(self):
        print("[",self.name,"] Placeholder for input-format-specific configurations")



    #---#  Utilities for variables

    def is_defined(self, var_name):        return (var_name in self.vars_DB)

    def get_type(self, var_name):
        if self.is_defined(var_name):
            return self.vars_DB[var_name][self._TYPE_key]
        else:
            return "NONE"

    def type_with_features(self, var_type):        return (var_type in self.typesWithFeature)
    def type_with_index(   self, var_type):        return (var_type in self.typesWithIndex)

    def var_with_features( self, var_name):                  return self.type_with_features(self.get_type(var_name))
    def var_with_index(    self, var_name):                  return self.type_with_index(   self.get_type(var_name))
    def has_this_feature(  self, var_name, feature_name):    return (feature_name in self.vars_DB[var_name])



    #---#  Utilities for DB

    #---#  Build

    def _add_variable(self, var_origin, var_target, var_type):
        self.vars_DB[var_origin]   = {var_origin:var_target, "TYPE":var_type}

    def add_scalar(    self, var_origin, var_target): self._add_variable(var_origin, var_target, self.scalar_type) 
    def add_vector(    self, var_origin, var_target): self._add_variable(var_origin, var_target, self.vector_type) 
    def add_object(    self, var_origin, var_target): self._add_variable(var_origin, var_target, self.object_type) 
    def add_collection(self, var_origin, var_target): self._add_variable(var_origin, var_target, self.collection_type) 
 
    def add_feature(self, var_origin, feat_origin, feat_target):
        if not self.is_defined(var_origin):
            print(" ERROR  -  variable ", var_origin, "  not defined!")
            return
        else:
            self.vars_DB[var_origin][feat_origin] = feat_target



    def check_target_format(self, tFormat, keyWord_list=[]):
        _status = True
        for keyWord in keyWord_list:
            if not keyWord in tFormat:
                print("- target format(", tFormat, ") - ERROR : missing ", keyWord, " target in the format string.")
                _status = False
        return _status


    def set_scalar_target_format(self, tFormat):
        if self.check_target_format(tFormat, ["VARIABLE"]):                       self.scalar_target_format =     tFormat

    def set_vector_target_format(self, tFormat):
        if self.check_target_format(tFormat, ["VARIABLE","INDEX"]):               self.vector_target_format =     tFormat

    def set_object_target_format(self, tFormat):
        if self.check_target_format(tFormat, ["VARIABLE","FEATURE"]):             self.object_target_format =     tFormat

    def set_collection_target_format(self, tFormat):
        if self.check_target_format(tFormat, ["VARIABLE","INDEX","FEATURE"]):     self.collection_target_format = tFormat

        



    #---#  Save & Load

    def save_DB(self, dbFileName):
        with open(dbFileName, "w") as file:
            json.dump(self.vars_DB, file)


    def load_DB(self, dbFileName):
        with open(dbFileName) as file:
            self.vars_DB = json.load(file)
        self.print_summary()


    #---#  Print & Summary

    def list_variables(self, var_type="all"):
        for v in self.vars_DB:
            if (var_type == "all") or (self.get_type(v) == var_type):
                print(v.ljust(20), "-->  ", self.vars_DB[v][v].ljust(20), " (", self.vars_DB[v][self._TYPE_key], ")")


    def print_summary(self):
        counter = {self.scalar_type:0, self.vector_type:0, self.object_type:0, self.collection_type:0, "NONE":0}
        for v in self.vars_DB:    counter[self.get_type(v)] += 1
        for t in counter:         print(t.ljust(20), "-->  entries:  ", counter[t])


    def dictionary_for(self, _var):
        
        # Variable type requested
        if _var == "all":      return self.vars_DB

        if _var in self.types:
            _dict = {}
            for v in self.vars_DB:
                if (self.get_type(v) == _var):     _dict[v] = self.vars_DB[v]
            return _dict
                    
        # Variable name requested
        if self.is_defined(_var):    return self.vars_DB[_var]

        print(" ERROR  -  variable ", _var, "  not defined!")
        return {}


    def print_dictionary(self, _name = "all"):

        print(">> Dictionary for  ", _name)
        _d = self.dictionary_for(_name)
        for v in _d:     print(v.ljust(20), "-->", _d[v])







    ########### Dictionaries definition

    def define_DB(self):

        # Scalar variables (no index, no variables)
        self.vars_DB["scalar1"]   = {"scalar1":"SCALAR1",   "TYPE":self.scalar_type}
        self.vars_DB["scalar_2"]  = {"scalar_2":"SCALAR_2", "TYPE":self.scalar_type}
        self.vars_DB["s"]         = {"s":"S",               "TYPE":self.scalar_type}


        # Vector variables (index, no feature)
        self.vars_DB["vector1"]   = {"vector1":"VECTOR1",   "TYPE":self.vector_type}
        self.vars_DB["vector_2"]  = {"vector_2":"VECTOR_2", "TYPE":self.vector_type}


        # Object variables (no index, feature)
        self.vars_DB["Obj1"] = {"Obj1":"OBJ1",  "TYPE":self.object_type}
        self.vars_DB["Obj1"]["x1"] = "X1"
        self.vars_DB["Obj1"]["y1"] = "Y2"


        # Collection variables (index, feature)
        self.vars_DB["Col1"] = {"Col1":"COL1",  "TYPE":self.collection_type}
        self.vars_DB["Col1"]["pt"]   = "PT"
        self.vars_DB["Col1"]["eta"]  = "ETA"
        self.vars_DB["Col1"]["phi"]  = "PHI"
        self.vars_DB["Col1"]["a"]    = "A"
        self.vars_DB["Col1"]["a_b"]  = "A_B"

        self.vars_DB["Col2"] = {"Col2":"COL2",  "TYPE":self.collection_type}
        self.vars_DB["Col2"]["pt"]   = "PT"
        self.vars_DB["Col2"]["eta"]  = "ETA"
        self.vars_DB["Col2"]["phi"]  = "PHI"

        self.vars_DB["Col3"] = {"Col3":"Col3",  "TYPE":self.collection_type}
        self.vars_DB["Col3"]["pt"]   = "pt"
        self.vars_DB["Col3"]["eta"]  = "eta"
        self.vars_DB["Col3"]["phi"]  = "phi"


    # Target:   name             -> NAME
    # Target:   name[index]      -> NAME[index]
    # Target:   name.feat        -> NAME_FEAT
    # Target:   name[index].feat -> NAME_FEAT[index]

    #
    # Could be implemented in 2 stages: translate to target dictionary + build
    #

    #    def convert(self, sVar, sInd, sFeat):
    #
    #        typeVar = self.get_type(sVar)
    #
    #        #        convString = ""
    #        #
    #        #        if not typeVar in self.typesWithFeature:
    #        #            convString = self.vars_DB[sVar][sVar]
    #        #        else:
    #        #            convString =      self.vars_DB[sVar][sVar]
    #        #            convString += '_'+self.vars_DB[sVar][sFeat]
    #
    #        convString = self.vars_DB[sVar][sVar]
    #
    #        if self.type_with_features(typeVar):    convString += '_'+self.vars_DB[sVar][sFeat]
    #        if self.type_with_index(   typeVar):    convString += '['+sInd+']'
    #
    #        return convString



    def convert(self, sVar, sInd, sFeat):

        #        print("convert : ", sVar, "[", sInd, "]", sFeat)

        typeVar = self.get_type(sVar)

        tVar = self.vars_DB[sVar][sVar]
        if sInd  != "NONE":    tInd  = sInd
        if sFeat != "NONE":    tFeat = self.vars_DB[sVar][sFeat]
        #        if self.type_with_index(   typeVar):    tInd  = sInd
        #        if self.type_with_features(typeVar):    tFeat = self.vars_DB[sVar][sFeat]

        if   typeVar == self.scalar_type :        return (self.scalar_target_format).replace("VARIABLE", tVar)
        elif typeVar == self.vector_type :        return (self.vector_target_format).replace("VARIABLE", tVar).replace("INDEX",   tInd)
        elif typeVar == self.object_type :        return (self.object_target_format).replace("VARIABLE", tVar).replace("FEATURE", tFeat)
        elif typeVar == self.collection_type :    return (self.collection_target_format).replace("VARIABLE", tVar).replace("INDEX",   tInd).replace("FEATURE", tFeat)

        return "__TRANSLATION_TYPE_ERROR__"


# Built-in hash() function in Pyton is "salted" by a random mumber (unique per execution)
# (see: https://docs.python.org/3/reference/datamodel.html#object.__hash__ )
#    def hash_dict(self):
#        return hash(str(self.OBJs_dict))
