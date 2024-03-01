##
##  Rewriting for NAIL/nanoAOD as baseline (source/description) format
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

        self.name            = interfaceName
        self.comment         = ""
        
        self.VARIABLE_label  = "VARIABLE"
        self.FEATURE_label   = "FEATURE"
        self.INDEX_label     = "INDEX"

        self.scalar_type     = "scalar"
        self.vector_type     = "vector"
        self.object_type     = "object"
        self.collection_type = "collection"

        self.types             = (self.scalar_type, self.vector_type, self.object_type, self.collection_type)
        self.typesWithIndex    = (                  self.vector_type,                   self.collection_type)
        self.typesWithFeature  = (                                    self.object_type, self.collection_type)

        self.info_dictionary = {}

        self.DB = {}

        self.DB["base_formats"]     = {}
        self.DB["target_formats"]   = {}
        self.DB["vars"]             = {}


        for t in self.types:
            self.DB["base_formats"][t]   = self.source_format(t)
            self.DB["target_formats"][t] = "NOT_SET"


        if db_file != "":      self.load_DB(db_file)


        if interfaceName != "":
            if interfaceName != self.name:
                print("Interface renamed :  ", self.name, "  ->  ", interfaceName)
            self.name = interfaceName


        self.update_info_dictionary()

        print("[",self.name,"] interfaceDictionary object created")


        
    def __str__(self):
        return "[ "+self.name+" ] Interface class for test format input files \n"+self.comment



    ##################################
    # Basic features

    def set_comment(self, comment_text):     self.comment = comment_text



    ##################################
    # Save & Load

    def update_info_dictionary(self):

        self.info_dictionary.clear()

        self.info_dictionary["info"]             = {}
        self.info_dictionary["info"]["name"]     = self.name
        self.info_dictionary["info"]["type"]     = str(type(self))
        self.info_dictionary["info"]["comment"]  = self.comment

        self.info_dictionary["VARIABLE_label"]   = self.VARIABLE_label
        self.info_dictionary["FEATURE_label"]    = self.FEATURE_label
        self.info_dictionary["INDEX_label"]      = self.INDEX_label

        self.info_dictionary["scalar_type"]      = self.scalar_type
        self.info_dictionary["vector_type"]      = self.vector_type
        self.info_dictionary["object_type"]      = self.object_type
        self.info_dictionary["collection_type"]  = self.collection_type

        self.info_dictionary["types"]            = self.types
        self.info_dictionary["typesWithIndex"]   = self.typesWithIndex
        self.info_dictionary["typesWithFeature"] = self.typesWithFeature

        self.info_dictionary["DB"]               = self.DB

        print("\n\n =========== info_dictionary =======================\n", self.info_dictionary, "\n=======================\n")

        return
            


    def configure_from_info_dictionary(self, infoDict = {}):

        id = infoDict if (len(infoDict) > 0) else self.info_dictionary

        self.name             = id["info"]["name"]
        self.comment          = id["info"]["comment"]

        self.VARIABLE_label   = id["VARIABLE_label"]
        self.FEATURE_label    = id["FEATURE_label"]
        self.INDEX_label      = id["INDEX_label"]

        self.scalar_type      = id["scalar_type"]
        self.vector_type      = id["vector_type"]
        self.object_type      = id["object_type"]
        self.collection_type  = id["collection_type"]

        self.types            = id["types"]
        self.typesWithIndex   = id["typesWithIndex"]
        self.typesWithFeature = id["typesWithFeature"]

        self.DB               = id["DB"]

        return
            


    def save_DB(self, dbFileName):
        self.update_info_dictionary()
        with open(dbFileName, "w") as file:
            json.dump(self.info_dictionary, file)
        return


    def load_DB(self, dbFileName):
        self.info_dictionary.clear()
        with open(dbFileName) as file:
            self.info_dictionary = json.load(file)
        print("** DB loaded from file ", dbFileName)

        self.configure_from_info_dictionary()
        
        self.print_summary()

        return
    


    ##################################
    # Placeholder for input-format-specific configurations

    def configureInterface(self):
        print("[",self.name,"] Placeholder for input-format-specific configurations")
        return



    ##################################
    #  Utilities for variables

    def is_defined(      self, var_name):                  return (var_name in self.DB["vars"])
    def has_this_feature(self, var_name, feature_name):    return (feature_name in self.DB["vars"][var_name])   # Search by source-name 


    def type_if(self, has_feature, has_index):
        if   not has_feature and not has_index :    return self.scalar_type
        elif not has_feature and     has_index :    return self.vector_type
        elif     has_feature and not has_index :    return self.object_type
        elif     has_feature and     has_index :    return self.collection_type
        return



    ##################################
    #  Utilities for DB building

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

        if var_target == "":    var_target = var_origin

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



    ##################################
    # Utilities for Format

    #    def source_format(self, vType):
    #        source_format = self.VARIABLE_label
    #        if self.type_with_features(vType):     source_format+='_'+self.FEATURE_label
    #        if self.type_with_index(vType):        source_format+='['+self.INDEX_label+']'
    #        return source_format

    def source_format(self, vType):
        source_format = self.VARIABLE_label
        if vType in self.typesWithFeature:      source_format+='_'+self.FEATURE_label
        if vType in self.typesWithIndex:        source_format+='['+self.INDEX_label+']'
        return source_format


    def set_format(self, f_type, f_string, side):
        if   (side != "base" and side != "target"):                                        print("** WRONG side : ", side, "  ('base' or 'target')")
        elif not f_type in self.types:                                                     print("** WRONG format type set : ", f_type)
        elif not self.VARIABLE_label in f_string:                                          print("** "+side+" format(", f_string, ") - ERROR : missing ", self.VARIABLE_label, " keyword in the format string.")
        elif (f_type in self.typesWithIndex   and  not self.INDEX_label   in f_string):    print("** "+side+" format(", f_string, ") - ERROR : missing ", self.INDEX_label,    " keyword in the format string.")
        elif (f_type in self.typesWithFeature and  not self.FEATURE_label in f_string):    print("** "+side+" format(", f_string, ") - ERROR : missing ", self.FEATURE_label,  " keyword in the format string.")
        else:
            self.DB[side+"_formats"][f_type] = f_string
            print("** set  ", side.ljust(10), " format for ", f_type.ljust(12), " variables : ", self.DB[side+"_formats"][f_type])
        return

    def set_base_format(  self, f_type, f_string):    self.set_format(f_type, f_string, "base")
    def set_target_format(self, f_type, f_string):    self.set_format(f_type, f_string, "target")


    
    ##################################
    # Utilities for dictionary extraction

    def dictionary_for(self, _var):
        # All variables requested
        if _var == "all":      return self.DB["vars"]

        # Variable name requested
        if self.is_defined(_var):    return self.DB["vars"][_var]

        print(" ERROR  -  variable ", _var, "  not defined!")
        return {}


    # Feature SOURCE name
    def list_of_features_for(self, _var):
        if not self.is_defined(_var):    return []
        d_var = self.dictionary_for(_var)
        return [f for f in d_var if f != _var]



    ##################################
    #  Print & Summary

    def print_interface_info(self):
        print("** Interface info")
        print("name             -->  ", self.name)
        print("comment          -->  ", self.comment)
        return


    def supported_formats(self):
        print("** Supported Formats")
        print(" Type                Source format              -->   Target Format ")
        for vType in self.types:
            print(vType.ljust(20), (self.DB["base_formats"][vType].ljust(24), "  -->  ", self.DB["target_formats"][vType]))
        return


    def print_target_formats(self):
        print("** Target Formats")
        for tf in self.DB["target_formats"]:
            print(tf.ljust(20), "-->  ", self.DB["target_formats"][tf].ljust(20))
        return


    def list_variables(self):
        for v in self.DB["vars"]:
            print(v.ljust(20), "-->  ", self.DB["vars"][v][v].ljust(20))
        return


    def print_summary(self):
        self.print_interface_info()
        self.supported_formats()
        return


    def print_dictionary(self, _name = "all"):
        print(">> Dictionary for  ", _name)
        _d = self.dictionary_for(_name)
        for v in _d:     print(v.ljust(20), "-->", _d[v])
        return


    ##################################
    # Build variable name according to specified format (base or target)

    def build_with_target_format(self, _Var, _Feat, _Ind):
        return self.build("target_formats", _Var, _Feat, _Ind)
        

    def build_with_base_format(self, _Var, _Feat, _Ind):
        return self.build("base_formats", _Var, _Feat, _Ind)



    def build(self, _format, _Var, _Feat, _Ind):

        tVar  = _Var
        tFeat = ""
        tInd  = ""

        _has_feature = False
        _has_index   = False

        # FEATURE
        if not _Feat == "NONE":
            tFeat        = _Feat
            _has_feature = True

        # INDEX
        if not ( (_Ind  == "NONE") or (_Ind  == "SKIP") ):
            tInd         = _Ind
            _has_index   = True

        typeVar = self.type_if(_has_feature, _has_index)
            
        return (self.DB[_format][typeVar].replace(self.VARIABLE_label, tVar).replace(self.INDEX_label, tInd).replace(self.FEATURE_label, tFeat))

        

    ##################################
    # Conversion from source to target format

    def convert(self, sVar, sFeat, sInd):

        if not self.is_defined(sVar):
            print("*** ERROR :  variable  ", sVar, "  is NOT defined")
            return "CONVERT_ERROR"

        tVar  = self.DB["vars"][sVar][sVar]
        tFeat = sFeat

        if (sFeat != "NONE"):
            if (not self.has_this_feature(sVar, sFeat)):
                print("*** ERROR :  variable  ", sVar, "  has NO feature  ", sFeat)
                return "CONVERT_ERROR"
            else:
                tFeat = self.DB["vars"][sVar][sFeat]

        tInd  = sInd

        return self.build_with_target_format(tVar, tFeat, tInd)





##################
# Notes:
#
# Built-in hash() function in Pyton is "salted" by a random mumber (unique per execution)
# (see: https://docs.python.org/3/reference/datamodel.html#object.__hash__ )
#    def hash_dict(self):
#        return hash(str(self.OBJs_dict))
