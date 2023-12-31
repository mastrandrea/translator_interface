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
        vType  = "NONE"
        vPos   = -1

        stringShift = 0

        while stringShift < len(targetString):

            t1, t1_pos = self.get_token(targetString[stringShift:], underscore_allowed=False)

            if self.ID.is_defined(t1):
                return t1, self.ID.get_type(t1), (stringShift+t1_pos)
            else:
                stringShift += (t1_pos + len(t1))

        return result, vType, vPos



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
    # If a feature is found, its presence in the variable's dictionary will be checked in the main function
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




    ##########  Methods for the string translation  ###############################
    #
    # Note: index field is usually not present in case of automatic internal index loop - it is used only for explicit picking (re-definition) of one element of vector/collection
    #
    def translate_string(self, inputString):

        if not self.do_translate:
            return inputString
        
        if inputString == "":
            return inputString

        sHeader     = ""
        varName     = "NONE"
        varFeature  = "NONE"
        varIndex    = "NONE"
        sFooter     = ""

        varType     = ""


        ### Find first variable (looping over dictionaries' keys)

        varName, varType, string_shift = self.find_first_var(inputString)


        ### Exit condition

        if varName == "NONE":
            return inputString



        ### Extract the header

        sHeader = inputString[0:string_shift]

        string_shift += len(varName)



        ### Search for a feature

        varFeature = self.find_feature(inputString[string_shift:])

        #        if varFeature == "NONE":
        #
        #            if self.ID.type_with_features(varType):
        #                return self.report_error("Feature field expected for "+varType+" variable  "+varName, inputString)
        #
        #        else:
        if varFeature != "NONE":

            if self.ID.type_with_features(varType):

                ### Check if the feature found is present in the dictionary of the variable
                if not self.ID.has_this_feature(varName, varFeature):
                    return self.report_error("Feature   "+varFeature+"   not in the dictionary for "+varType+" variable  "+varName, inputString)

                string_shift += (len(varFeature)+1)

            else:
                # Feature present for wrong variable type (scalar or vector)
                return self.report_error("Feature   "+varFeature+"   not expected for "+varType+" variable  "+varName, inputString)
                


        ### Search for an index field

        tempIndex = self.find_index(inputString[string_shift:])

        #        if tempIndex == "NONE":
        #            if self.ID.type_with_index(varType):
        #                return self.report_error("Index field expected for "+varType+" variable  "+varName, inputString)
        #        else:
        if tempIndex != "NONE":
            if not self.ID.type_with_index(varType):
                return self.report_error("Index field found for "+varType+" variable  "+varName, inputString)

            if tempIndex == "SKIP":
                string_shift += 2
            else:
                string_shift += (len(tempIndex)+2)

            # Translate index field - Recursive application
            varIndex = self.translate_string(tempIndex)



        ### Select the footer - Recursive application

        sFooter = self.translate_string(inputString[string_shift:])



        ###  Build the translated string using the method specific of the loaded interface

        outputString = sHeader+self.ID.convert(varName, varFeature, varIndex)+sFooter

        if self.TRANSLATION_ERROR in outputString:     outputString = self.TRANSLATION_ERROR


        return outputString





    ##########  Adding new variables and/or features to the db  ###################
    #
    # TBC: collection and scalar are assumed as baseline for the variables to be added ... index identified, but not used ...
    #
    
    def add_to_dictionary(self, inputString, hasIndex = True, featuresFrom = ""):

        ## If no dictionary is set then skip

        if not self.do_translate:
            return

        ## Check featuresFrom in db
        ## Check varFeature and featuresFrom simultaneously != 0 -> issue

        ### Single identifier (VARIABLE_FEATURE[INDEX]) is assumed - eventual recursive translation of the INDEX to be evaluated

        if inputString == "":
            self.report_error("Trying to add empty identifier to the dictionary! ")
            return
            
        varName     = "NONE"
        #        varIndex    = "NONE"
        varFeature  = "NONE"
        varType     = ""


        ### The first token is the variable name

        varName, varName_pos = self.get_token(inputString, False)


        #        ### Search for an index field
        #
        #        string_shift = (varName_pos+len(varName))
        #
        #        tempIndex = self.find_index(inputString[string_shift:])
        #
        #        if tempIndex != "NONE":
        #            if tempIndex == "SKIP":
        #                string_shift += 2
        #            else:
        #                string_shift += (len(tempIndex)+2)
        #                varIndex = tempIndex


        ### Search for a feature

        string_shift = (varName_pos+len(varName))

        varFeature = self.find_feature(inputString[string_shift:])


        print("Adding to the dictionary  variable "+varName+" , feature "+varFeature)



        ### Check and update the existing db

        # Variable already present in the db
        if self.ID.is_defined(varName):

            varType = self.ID.get_type(varName)

            # Trying to add a feature to the db
            if varFeature != "NONE":

                if not self.ID.type_with_features(varType):
                    self.report_error("Trying to add a feature to the "+varName+" variable already defined in the dictionary as of  "+varType+"  type", inputString)
                    return

                if self.ID.has_this_feature(varName, varFeature):
                    self.report_error("Feature "+varFeature+" already defined in the dictionary for variable  "+varName+" !  NO CHANGES to the dictionary! ", inputString)
                    return

                # New feature for an existing variable
                self.ID.add_feature(varName, varFeature)

            # Trying to add a variable with no feature to the db, with the variable already defined in the db -> wrong
            else:
                self.report_error("Trying to add the "+varName+" variable already defined in the dictionary  ("+varType+")", inputString)
                return


        # New Variable (i.e. not defined yet in the db)
        else:

            # With features
            if varFeature != "NONE":
                if hasIndex:    self.ID.add_collection(varName)
                else:           self.ID.add_object(varName)
                self.ID.add_feature(varName, varFeature)

            elif featuresFrom != "":
                if hasIndex:    self.ID.add_collection(varName)
                else:           self.ID.add_object(varName)
                for f in self.ID.list_of_features_for(featuresFrom):
                    self.ID.add_feature(varName, f)

            # No features
            else:
                if hasIndex:    self.ID.add_vector(varName)
                else:           self.ID.add_scalar(varName)

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
