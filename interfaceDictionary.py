##
##  Rewriting for NAIL/nanoAOD as baseline format
##
##     variable_feature[index]
##
##     - variable CANNOT contain "_"
##     - feature  can contain multiple "_"
##     - index is frequently omissed (due to automatic internal loop)
##     - a token ending with a "(" is a function/method, NOT a variable/feature
##
## Types of codification for variables:
##  - Scalar:     no index, no feature         e.g. RunNumber
##  - Vector:        INDEX, no feature         e.g. MCweights[i]
##  - Object:     no index,    FEATURE         e.g. MET_x, MET_y
##  - Collection:    INDEX,    FEATURE         e.e. electron_pT[i]
##
##

import json

class interfaceDictionary:
    def __init__(self, interfaceName = "", db_file = ""):

        self.scalar_type     = "scalar"
        self.vector_type     = "vector"
        self.object_type     = "object"
        self.collection_type = "collection"
        self._TYPE_key       = "TYPE"

        self.types             = (self.scalar_type, self.vector_type, self.object_type, self.collection_type)
        self.typesWithIndex    = (                  self.vector_type,                   self.collection_type)
        self.typesWithFeature  = (                                    self.object_type, self.collection_type)

        self.VARIABLE_label = "VARIABLE"
        self.INDEX_label    = "INDEX"
        self.FEATURE_label  = "FEATURE"

        self.DB = {}
        self.DB["interface_info"]   = {}
        self.DB["original_formats"] = {}
        self.DB["target_formats"]   = {}
        self.DB["vars"]             = {}

        self.DB["interface_info"]["name"]     = ""
        self.DB["interface_info"]["comments"] = ""

        for t in self.types:   self.DB["target_formats"][t] = "NOT_SET"

        if db_file != "":      self.load_DB(db_file)


        if interfaceName != "":
            if interfaceName != self.DB["interface_info"]["name"]:
                print("Interface renamed :  ", self.DB["interface_info"]["name"], "  ->  ", interfaceName)
            self.DB["interface_info"]["name"] = interfaceName

        print("[",self.DB["interface_info"]["name"],"] interfaceDictionary object created")


        
    def __str__(self):
        return "[ "+self.DB["interface_info"]["name"]+" ] Interface class for test format input files \n"+self.DB["interface_info"]["comments"]


    def name(self):         return self.DB["interface_info"]["name"]
    def comments(self):     return self.DB["interface_info"]["comments"]

    def set_comments(self, comment_text):
        self.DB["interface_info"]["comments"] = comment_text



    #---# Placeholder for input-format-specific configurations
    def configureInterface(self):
        print("[",self.DB["interface_info"]["name"],"] Placeholder for input-format-specific configurations")



    #---#  Utilities for variables

    def is_defined(self, var_name):        return (var_name in self.DB["vars"])

    def get_type(self, var_name):
        if self.is_defined(var_name):
            return self.DB["vars"][var_name][self._TYPE_key]
        else:
            return "NONE"

    def type_with_features(self, var_type):                  return (var_type in self.typesWithFeature)
    def type_with_index(   self, var_type):                  return (var_type in self.typesWithIndex)

    def var_with_features( self, var_name):                  return self.type_with_features(self.get_type(var_name))
    def var_with_index(    self, var_name):                  return self.type_with_index(   self.get_type(var_name))
    def has_this_feature(  self, var_name, feature_name):    return (feature_name in self.DB["vars"][var_name])   # Search by source-name 



    #---#  Utilities for DB

    #---#  Build

    def _add_variable(self, var_origin, var_target, var_type):
        if var_target == "": var_target = var_origin
        # nVar scalar is automatically added in case of variables with index (vectors and collections)
        if self.type_with_index(var_type):
            self.DB["vars"]["n"+var_origin] = {"n"+var_origin:"n"+var_target, "TYPE":self.scalar_type}
        self.DB["vars"][var_origin] = {var_origin:var_target, "TYPE":var_type}
        

    def add_scalar(    self, var_origin, var_target=""): self._add_variable(var_origin, var_target, self.scalar_type) 
    def add_vector(    self, var_origin, var_target=""): self._add_variable(var_origin, var_target, self.vector_type) 
    def add_object(    self, var_origin, var_target=""): self._add_variable(var_origin, var_target, self.object_type) 
    def add_collection(self, var_origin, var_target=""): self._add_variable(var_origin, var_target, self.collection_type) 
 
    def add_feature(self, var_origin, feat_origin, feat_target=""):
        if not self.is_defined(var_origin):
            print(" ERROR  -  variable ", var_origin, "  not defined!")
            return
        else:
            if feat_target == "": feat_target = feat_origin
            self.DB["vars"][var_origin][feat_origin] = feat_target


    def set_format(self, f_type, f_string, side):
        if (side != "original" and side != "target"):                                      print("** WRONG side : ", side, "  ('original' or 'target')")
        if   not f_type in self.types:                                                     print("** WRONG format type set : ", f_type)
        elif not self.VARIABLE_label in f_string:                                          print("** "+side+" format(", f_string, ") - ERROR : missing ", self.VARIABLE_label, " keyword in the format string.")
        elif (self.type_with_index(f_type) and  not self.INDEX_label in f_string):         print("** "+side+" format(", f_string, ") - ERROR : missing ", self.INDEX_label,    " keyword in the format string.")
        elif (self.type_with_features(f_type) and  not self.FEATURE_label in f_string):    print("** "+side+" format(", f_string, ") - ERROR : missing ", self.FEATURE_label,  " keyword in the format string.")
        else:
            self.DB[side+"_formats"][f_type] = f_string

        print("** set  ", side.ljust(10), " format for ", f_type.ljust(12), " variables : ", self.DB[side+"_formats"][f_type])



    def set_original_format(self, f_type, f_string):    self.set_format(f_type, f_string, "original")
    def set_target_format(  self, f_type, f_string):    self.set_format(f_type, f_string, "target")



    def dictionary_for(self, _var):
        # Variable type requested
        if _var == "all":      return self.DB["vars"]

        if _var in self.types:
            _dict = {}
            for v in self.DB["vars"]:
                if (self.get_type(v) == _var):     _dict[v] = self.DB["vars"][v]
            return _dict
                    
        # Variable name requested
        if self.is_defined(_var):    return self.DB["vars"][_var]

        print(" ERROR  -  variable ", _var, "  not defined!")
        return {}



    def list_of_features_for(self, _var):
        fl = []
        d_var = self.dictionary_for(_var)
        for f in d_var:
            if (f != _var) and (f != "TYPE"): fl.append(f)

        return fl


    #---#  Save & Load

    def save_DB(self, dbFileName):
        with open(dbFileName, "w") as file:
            json.dump(self.DB, file)


    def load_DB(self, dbFileName):
        with open(dbFileName) as file:
            self.DB = json.load(file)
        print("** DB loaded from file ", dbFileName)
        self.print_summary()



    #---#  Print & Summary

    def print_interface_info(self):
        print("** Interface info")
        for ii in self.DB["interface_info"]:
            print(ii.ljust(20), "-->  ", self.DB["interface_info"][ii].ljust(20))


    def _source_format(self, vType):
        _source_format = self.VARIABLE_label
        if self.type_with_features(vType):     _source_format+='_'+self.FEATURE_label
        if self.type_with_index(vType):        _source_format+='['+self.INDEX_label+']'
        return _source_format


    def supported_formats(self):
        print("** Supported Formats")
        print(" Type                Source format              -->   Target Format ")
        for vType in self.types:
            print(vType.ljust(20), (self._source_format(vType)).ljust(24), "  -->  ", self.DB["target_formats"][vType])


    def print_target_formats(self):
        print("** Target Formats")
        for tf in self.DB["target_formats"]:
            print(tf.ljust(20), "-->  ", self.DB["target_formats"][tf].ljust(20))


    def list_variables(self, var_type="all"):
        for v in self.DB["vars"]:
            if (var_type == "all") or (self.get_type(v) == var_type):
                print(v.ljust(20), "-->  ", self.DB["vars"][v][v].ljust(20), " (", self.DB["vars"][v][self._TYPE_key], ")")


    def print_variables_summary(self):
        print("** Variables Summary")
        counter = {self.scalar_type:0, self.vector_type:0, self.object_type:0, self.collection_type:0, "NONE":0}
        for v in self.DB["vars"]:    counter[self.get_type(v)] += 1
        for t in counter:         print(t.ljust(20), "-->   entries: ", counter[t])


    def print_summary(self):
        self.print_interface_info()
        #        self.print_target_formats()
        self.supported_formats()
        self.print_variables_summary()


    def print_dictionary(self, _name = "all"):
        print(">> Dictionary for  ", _name)
        _d = self.dictionary_for(_name)
        for v in _d:     print(v.ljust(20), "-->", _d[v])




    ## Convertion from source to target format ###################################################################

    def convert(self, sVar, sFeat, sInd):

        typeVar = self.get_type(sVar)

        if not typeVar in self.types:    return "__TRANSLATION_TYPE_ERROR__"   # Probably this check can be removed ...

        tVar  = self.DB["vars"][sVar][sVar]
        tFeat = ""
        tInd  = ""


        # FEATURE

        if sFeat == "NONE":
            if   typeVar == self.object_type :        typeVar = self.scalar_type
            elif typeVar == self.collection_type :    typeVar = self.vector_type
        else:
            tFeat = self.DB["vars"][sVar][sFeat]


        # INDEX

        if (sInd  == "NONE") or (sInd  == "SKIP"):
            if   typeVar == self.vector_type :        typeVar = self.scalar_type
            elif typeVar == self.collection_type :    typeVar = self.object_type
        else:
            tInd  = sInd


        # Build translated string

        if   typeVar == self.scalar_type :        return (self.DB["target_formats"][typeVar].replace(self.VARIABLE_label, tVar))
        elif typeVar == self.vector_type :        return (self.DB["target_formats"][typeVar].replace(self.VARIABLE_label, tVar).replace(self.INDEX_label,   tInd))
        elif typeVar == self.object_type :        return (self.DB["target_formats"][typeVar].replace(self.VARIABLE_label, tVar).replace(self.FEATURE_label, tFeat))
        elif typeVar == self.collection_type :    return (self.DB["target_formats"][typeVar].replace(self.VARIABLE_label, tVar).replace(self.INDEX_label,   tInd).replace(self.FEATURE_label, tFeat))




        
        



# Built-in hash() function in Pyton is "salted" by a random mumber (unique per execution)
# (see: https://docs.python.org/3/reference/datamodel.html#object.__hash__ )
#    def hash_dict(self):
#        return hash(str(self.OBJs_dict))
