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
## Translation (i.e. dictionary) is relevant for variables and features *ONLY*
## - index information managed in the convert method only!

import json

class interfaceDictionary:
    def __init__(self, interfaceName = "", db_file = ""):

        self.VARIABLE_label = "VARIABLE"
        self.FEATURE_label  = "FEATURE"
        self.INDEX_label    = "INDEX"

        self.scalar_type     = "scalar"
        self.vector_type     = "vector"
        self.object_type     = "object"
        self.collection_type = "collection"

        self.types             = (self.scalar_type, self.vector_type, self.object_type, self.collection_type)
        self.typesWithIndex    = (                  self.vector_type,                   self.collection_type)
        self.typesWithFeature  = (                                    self.object_type, self.collection_type)


        self.DB = {}
        self.DB["interface_info"] = {}
        self.DB["base_formats"]   = {}
        self.DB["target_formats"] = {}
        self.DB["vars"]           = {}

        self.DB["interface_info"]["name"]     = ""
        self.DB["interface_info"]["comments"] = ""


        
        for t in self.types:
            self.DB["base_formats"][t]   = self._source_format(t)
            self.DB["target_formats"][t] = "NOT_SET"

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

    def has_this_feature(  self, var_name, feature_name):    return (feature_name in self.DB["vars"][var_name])   # Search by source-name 


    def type_if(self, has_feature, has_index):
        if   not has_feature and not has_index :    return self.scalar_type
        elif not has_feature and     has_index :    return self.vector_type
        elif     has_feature and not has_index :    return self.object_type
        elif     has_feature and     has_index :    return self.collection_type



    #---#  Utilities for DB

    #---#  Build

    #    def add_variable(self, var_origin, var_target, var_type):
    def add_variable(self, var_origin, var_target=""):

        if self.is_defined(var_origin):
            print("** ERROR trying to add a variable already defined in the dictionary : ", var_origin)
            return

        if "_" in var_origin:
            print("** ERROR trying to add a variable with an underscore in the base name : ", var_origin)
            return

        if "_" in var_target:
            print("** ERROR trying to add a variable with an underscore in the target name : ", var_target)
            return


        if var_target == "": var_target = var_origin

        self.DB["vars"][var_origin] = {var_origin:var_target}


    def add_feature(self, var_origin, feat_origin, feat_target=""):
        if not self.is_defined(var_origin):
            print("** ERROR  -  variable ", var_origin, "  not defined!")
            return
        if self.has_this_feature(var_origin, feat_origin):
            print("** ERROR  -  feature ", feat_origin, "  already defined for variable ", var_origin)
            return

        if feat_target == "": feat_target = feat_origin
        self.DB["vars"][var_origin][feat_origin] = feat_target
        return



    def _source_format(self, vType):
        _source_format = self.VARIABLE_label
        if self.type_with_features(vType):     _source_format+='_'+self.FEATURE_label
        if self.type_with_index(vType):        _source_format+='['+self.INDEX_label+']'
        return _source_format


    def set_format(self, f_type, f_string, side):
        if   (side != "base" and side != "target"):                                         print("** WRONG side : ", side, "  ('base' or 'target')")
        elif not f_type in self.types:                                                      print("** WRONG format type set : ", f_type)
        elif not self.VARIABLE_label in f_string:                                           print("** "+side+" format(", f_string, ") - ERROR : missing ", self.VARIABLE_label, " keyword in the format string.")
        elif (f_type in self.typesWithIndex   and  not self.INDEX_label   in f_string):    print("** "+side+" format(", f_string, ") - ERROR : missing ", self.INDEX_label,    " keyword in the format string.")
        elif (f_type in self.typesWithFeature and  not self.FEATURE_label in f_string):    print("** "+side+" format(", f_string, ") - ERROR : missing ", self.FEATURE_label,  " keyword in the format string.")
        else:
            self.DB[side+"_formats"][f_type] = f_string
            print("** set  ", side.ljust(10), " format for ", f_type.ljust(12), " variables : ", self.DB[side+"_formats"][f_type])


    def set_base_format(  self, f_type, f_string):    self.set_format(f_type, f_string, "base")
    def set_target_format(self, f_type, f_string):    self.set_format(f_type, f_string, "target")



    def dictionary_for(self, _var):
        # All variables requested
        if _var == "all":      return self.DB["vars"]

        # Variable name requested
        if self.is_defined(_var):    return self.DB["vars"][_var]

        print(" ERROR  -  variable ", _var, "  not defined!")
        return {}



    def list_of_features_for(self, _var):
        fl = []
        d_var = self.dictionary_for(_var)
        for f in d_var:
            if (f != _var):  fl.append(f)

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
        if vType in self.typesWithFeature:      _source_format+='_'+self.FEATURE_label
        if vType in self.typesWithIndex:        _source_format+='['+self.INDEX_label+']'
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


    def list_variables(self):
        for v in self.DB["vars"]:
            print(v.ljust(20), "-->  ", self.DB["vars"][v][v].ljust(20))


    def print_summary(self):
        self.print_interface_info()
        #        self.print_target_formats()
        self.supported_formats()


    def print_dictionary(self, _name = "all"):
        print(">> Dictionary for  ", _name)
        _d = self.dictionary_for(_name)
        for v in _d:     print(v.ljust(20), "-->", _d[v])




    ## Convertion from source to target format ###################################################################

    def convert(self, sVar, sFeat, sInd):

        tVar  = self.DB["vars"][sVar][sVar]
        tFeat = ""
        tInd  = ""

        _has_feature = False
        _has_index   = False


        # FEATURE

        if not sFeat == "NONE":
            tFeat = self.DB["vars"][sVar][sFeat]
            _has_feature = True

        # INDEX

        if not ( (sInd  == "NONE") or (sInd  == "SKIP") ):
            tInd  = sInd
            _has_index   = True


        typeVar = self.type_if(_has_feature, _has_index)
            
        return (self.DB["target_formats"][typeVar].replace(self.VARIABLE_label, tVar).replace(self.INDEX_label, tInd).replace(self.FEATURE_label, tFeat))


        
        

    ## Simple merge (according to target format) - no convertion from source to target format #######################

    def merge(self, sVar, sFeat, sInd):

        tVar  = sVar
        tFeat = ""
        tInd  = ""

        _has_feature = False
        _has_index   = False


        # FEATURE

        if not sFeat == "NONE":
            tFeat = sFeat
            _has_feature = True

        # INDEX

        if not ( (sInd  == "NONE") or (sInd  == "SKIP") ):
            tInd  = sInd
            _has_index   = True


        typeVar = self.type_if(_has_feature, _has_index)
            
        return (self.DB["target_formats"][typeVar].replace(self.VARIABLE_label, tVar).replace(self.INDEX_label, tInd).replace(self.FEATURE_label, tFeat))


        
        



# Built-in hash() function in Pyton is "salted" by a random mumber (unique per execution)
# (see: https://docs.python.org/3/reference/datamodel.html#object.__hash__ )
#    def hash_dict(self):
#        return hash(str(self.OBJs_dict))
