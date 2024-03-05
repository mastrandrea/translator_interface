##
##  Translation  FROM  NAIL/nanoAOD format  TO  target format (e.g. PHYSLITE)
##
##

from interfaceDictionary import interfaceDictionary


class translator:
    def __init__(self, interfaceDictionaryFile = "NONE", name = "translator"):
        self.name = name
        self.do_translate = True
        self.TRANSLATION_ERROR = "__TRANSLATION_ERROR__"

        if interfaceDictionaryFile == "NONE" :
            print("[",self.name,"] ERROR -", " Interface Dictionary File not set! ")
            return

        if interfaceDictionaryFile == "NO_TRANSLATION" :
            self.do_translate = False
        else:
            self.ID = interfaceDictionary("", interfaceDictionaryFile)

        print("[",self.name,"] translator object  ",self.name,"  created, with interface dictionary  ",interfaceDictionaryFile)
        #print(self.ID)

        

    #---#  Utility for error reporting

    def report_error(self, error_text, inputString = "NONE"):
        print("[",self.name,"] ERROR -", error_text)
        if inputString != "NONE" : print("[",self.name,"] +-->>  ", inputString)        
        return self.TRANSLATION_ERROR


    def addition_error(self, error_text, inputString = "NONE"):
        print("[",self.name,"] SKIP ADDITION -", error_text)
        if inputString != "NONE" : print("[",self.name,"] +-->>  ", inputString)        
        return


    #---#  Utilities for variables fields identification

    def get_token(self, targetString, underscore_allowed = True):

        sToken     = ""
        sToken_pos = 0

        for c in targetString:

            if ((c.isalnum()) or (underscore_allowed and (c == '_'))):
                sToken += c
            else:
                if sToken == "":
                    sToken_pos += 1
                else:
                    break

        return sToken, sToken_pos


    def find_closed_sb(self, targetString):
        open_sb       = 1
        closed_sb_pos = -1

        for i in range(0, len(targetString)):
            c = targetString[i]
            if   c == "[":  open_sb += 1
            elif c == "]":  open_sb -= 1

            if open_sb == 0:
                closed_sb_pos = i
                break

        return closed_sb_pos


    # Finding the first token which corresponds to one of the variables in the dictionary
    def find_first_var(self, targetString):
        result = "NONE"
        vPos   = -1

        stringShift = 0

        while stringShift < len(targetString):

            t1, t1_pos = self.get_token(targetString[stringShift:], underscore_allowed=False)

            if self.ID.is_defined(t1):
                return t1, (stringShift+t1_pos)
            else:
                stringShift += (t1_pos + len(t1))

        return result, vPos



    # This assumes string starting with "[" and looks for the corresponding "]"
    def find_index(self, targetString):
        result = "NONE"

        if not (targetString[0:1] == '['):
            return result

        index_begin = 1
        index_end   = index_begin + self.find_closed_sb(targetString[index_begin:])

        if (index_end > index_begin):
            result = targetString[index_begin:index_end]
        elif (index_end == index_begin):
            result = "SKIP"

        return result



    # This assumes string starting with "_" (NAIL/nanoAOD specific)
    # Not searched in the dictionary: if a feature is found, its presence in the variable's dictionary will be checked in the main function
    def find_feature(self, targetString):
        result = "NONE"

        if (len(targetString) < 2) or (targetString[0] != "_"):
            return result

        t1, t1_pos = self.get_token(targetString[1:], underscore_allowed=True)

        if t1_pos != 0:
            self.report_error("Wrong-formed feature filed  "+t1, targetString)

        # Protection against functions!
        l = len(t1)
        if (t1 != "") and (targetString[l+1:l+2] != "("):
            result = t1

        return result




    # This works only for variables (or constants) groups already defined in the dictionary
    def split_var_feat(self, varString):
        varName    = "NONE"
        varFeature = "NONE"

        ### Find first variable (looping over dictionaries' keys)
        varName, string_shift = self.find_first_var(varString)

        if varName == "NONE":
            return varString, varFeature

        string_shift += len(varName)

        ### Search for a feature
        varFeature = self.find_feature(varString[string_shift:])

        if varFeature != "NONE":

            ### Check if the feature found is present in the dictionary of the variable
            if not self.ID.has_this_feature(varName, varFeature):
                print("Feature   "+varFeature+"   not in the dictionary for variable  "+varName, varString)


        print("Found  ", varName, "  ++", varFeature, "++")


        return varName, varFeature




    def _isDefined(self, varName, varFeature):

        if not self.ID.is_defined(varName):
            return False

        if ((not varFeature == 'NONE') and (not self.ID.has_this_feature(varName, varFeature))):
            return False

        return True



    def isDefined(self, varString):

        varName, varFeature = self.split_var_feat(varString)

        return self._isDefined(varName, varFeature)




    def listOfFeaturesFor(self, var_name):
        return self.ID.list_of_features_for(var_name)



    ##########  Methods for the string translation  ###############################
    #
    # Note: index field is usually not present in case of automatic internal index loop - it is used only for explicit picking (re-definition) of one element of vector/collection
    #
    def translate_string(self, inputString):

        #        print("tttttttttttttttt < ", inputString)

        if not self.do_translate:
            #            print("tttttttttttttttt > ", inputString)
            return inputString
        
        if inputString == "":
            #            print("tttttttttttttttt > ", inputString)
            return inputString

        sHeader     = ""
        varName     = "NONE"
        varFeature  = "NONE"
        varIndex    = "NONE"
        sFooter     = ""

        doConvert = True

        ### Find first variable (looping over dictionaries' keys)

        varName, string_shift = self.find_first_var(inputString)


        ### Exit condition

        if varName == "NONE":
            #            print("tttttttttttttttt > ", inputString)
            return inputString



        ### Extract the header

        sHeader = inputString[0:string_shift]

        string_shift += len(varName)



        ### Search for a feature

        varFeature = self.find_feature(inputString[string_shift:])

        if varFeature != "NONE":

            ### Check if the feature found is present in the dictionary of the variable
            if not self.ID.has_this_feature(varName, varFeature):
                #                return self.report_error("Feature   "+varFeature+"   not in the dictionary for variable  "+varName, inputString)
                print("Feature   "+varFeature+"   not in the dictionary for variable  "+varName, inputString)
                doConvert = False

            string_shift += (len(varFeature)+1)



        ### Search for an index field

        tempIndex = self.find_index(inputString[string_shift:])

        if tempIndex != "NONE":

            if tempIndex == "SKIP":
                string_shift += 2
            else:
                string_shift += (len(tempIndex)+2)

            # Translate index field - Recursive application
            varIndex = self.translate_string(tempIndex)



        ### Select the footer - Recursive application

        sFooter = self.translate_string(inputString[string_shift:])



        ###  Build the translated string using the method specific of the loaded interface
        if doConvert:
            outputString = sHeader+self.ID.convert(varName, varFeature, varIndex)+sFooter
        else:
            outputString = sHeader+self.ID.build_with_base_format(varName, varFeature, varIndex)+sFooter

        if self.TRANSLATION_ERROR in outputString:     outputString = self.TRANSLATION_ERROR


        #        print("tttttttttttttttt > ", outputString)


        return outputString





    ##########  Methods for the extraction of the list of variables (inputs)  ###############################
    #
    # 
    #
    def get_var_list(self, inputString):

        varList = []
        
        if inputString == "":
            return varList

        sHeader     = ""
        varName     = "NONE"
        varFeature  = "NONE"
        varIndex    = "NONE"
        sFooter     = ""


        ### Find first variable (looping over dictionaries' keys)

        varName, string_shift = self.find_first_var(inputString)


        ### Exit condition

        if varName == "NONE":
            return varList



        ### Extract the header

        sHeader       = inputString[0:string_shift]
        string_shift += len(varName)


        ### Search for a feature

        varFeature = self.find_feature(inputString[string_shift:])

        if varFeature != "NONE":

            ### Check if the feature found is present in the dictionary of the variable
            if not self.ID.has_this_feature(varName, varFeature):
                print("Feature   "+varFeature+"   not in the dictionary for variable  "+varName, inputString)

            string_shift += (len(varFeature)+1)


        ### Add found variable to the list

        #        #        varList = [self.ID.build_with_target_format(varName, varFeature, "NONE")]
        #        varList = [self.ID.convert(varName, varFeature, "NONE")]

        varList = [self.ID.build_with_base_format(varName, varFeature, "NONE")]


        ### Search for an index field

        tempIndex = self.find_index(inputString[string_shift:])

        if tempIndex != "NONE":

            if tempIndex == "SKIP":
                string_shift += 2
            else:
                string_shift += (len(tempIndex)+2)

            # Add variables names found in the index field - Recursive application
            varList += self.get_var_list(tempIndex)



        ### Select the footer - Recursive application

        varList += self.get_var_list(inputString[string_shift:])



        ### Remove duplicates

        varList = list(dict.fromkeys(varList))


        return varList





    ##########  Adding new variables and/or features to the db  ###################
    #
    # Baseline idea: addition to the analysis interface (dictionary) of variables defined during the data manipulation (e.g. event loop).
    # The name used will be just the one defined, since - by definition - this variable should not be present in the target data ntuple.
    # (Otherwise this should have been added to the interface definition upstream!)
    #
    # Index not searched for!
    #

    def add_to_dictionary(self, inputString):

        #        print("[", self.name,"] add_to_dictionary(", inputString, " )")
        #print("@@@@@@@@@@@@@@@ add_to_dictionary(", inputString, " )")


        ## If no dictionary is set then skip

        if not self.do_translate:
            return

        ### Single identifier (VARIABLE or VARIABLE_FEATURE) is assumed - INDEX should not be part of the interface definition

        if inputString == "":
            self.addition_error("Trying to add empty identifier to the dictionary! ")
            return
            
        varName     = "NONE"
        varFeature  = "NONE"


        ### The first token is the variable name

        varName, varName_pos = self.get_token(inputString, False)


        ### Search for a feature

        string_shift = (varName_pos+len(varName))

        varFeature = self.find_feature(inputString[string_shift:])


        #print("Adding to the dictionary  variable "+varName+" , feature "+varFeature)


        ### Check and update the existing db

        # Variable already present in the db
        if self.ID.is_defined(varName):

            # Trying to add a feature to the db
            if varFeature != "NONE":

                if self.ID.has_this_feature(varName, varFeature):
                    self.addition_error("Feature "+varFeature+" already defined in the dictionary for variable  "+varName+" !  NO CHANGES to the dictionary! ", inputString)
                    return

                # New feature for an existing variable
                self.ID.add_feature(varName, varFeature)

            # Trying to add a variable with no feature to the db, with the variable already defined in the db -> wrong
            else:
                self.addition_error("Trying to add the "+varName+" variable already defined in the dictionary !  NO CHANGES!", inputString)
                return


        # New Variable (i.e. not defined yet in the db)
        else:

            self.ID.add_variable(varName)
            
            # With features
            if varFeature != "NONE":
                self.ID.add_feature(varName, varFeature)

        return





    def add_features_from(self, targetVar, sourceVar = ""):

        print("@@@@@@@@@@@@@@@ add_features_from(", targetVar, " , ", sourceVar, " )")

        ## If no dictionary is set then skip
        if not self.do_translate:
            return

        # If target variable is not present in the db -> error
        if not self.ID.is_defined(targetVar):
            print("ERROR: trying to copy features FOR  a variable not defined in the db : ", targetVar)
            return
            
        # If source variable is not present in the db -> error
        if not self.ID.is_defined(sourceVar):
            print("ERROR: trying to copy features FROM a variable not defined in the db : ", sourceVar)
            return
            
        for f in self.ID.list_of_features_for(sourceVar):
            print("add ", targetVar, "  ", f)
            self.ID.add_feature(targetVar, f)

        return







    def add_constant(self, inputString, constValue):

        ## If no dictionary is set then skip
        if not self.do_translate:
            return

        if inputString == "":
            self.addition_error("Trying to add empty identifier to the dictionary! ")
            return
 
        constPrefix = "NONE"
        constName   = "NONE"


        ### The first token is the constant prefix (same format of a variable name)

        constPrefix, constPrefix_pos = self.get_token(inputString, False)


        ### Search for a constName (same format of a var_feature

        string_shift = (constPrefix_pos+len(constPrefix))

        constName = self.find_feature(inputString[string_shift:])


        if constPrefix != self.ID.CONSTANT_label:
            self.addition_error("Trying to add an not-well defined constant to the dictionary !  NO CHANGES to the dictionary! ", inputString)
            return

        # Trying to add an undefined constant to the db
        if constName == "NONE":
            self.addition_error("Trying to add an undefined constant to the dictionary !  NO CHANGES to the dictionary! ", inputString)
            return



        ### Check and update the existing db

        # Const group not yet present in the db
        if not self.ID.is_defined(constPrefix):      self.ID.add_variable(constPrefix)

        self.ID.add_constant(constPrefix, constName, constValue)


        return



#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
