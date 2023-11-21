from interfaceDictionary import interfaceDictionary


class translator:
    def __init__(self, interfaceDictionaryFile = "NONE", name = "translator"):
        self.name = name
        if interfaceDictionaryFile == "NONE" :
            print("[",self.name,"] ERROR -", " Interface Dictionary File not set! ")
            return

        self.ID = interfaceDictionary("", interfaceDictionaryFile)
        print("[",self.name,"] translator object created, with interface ",self.ID.name())
        #print(self.ID)
        self.TRANSLATION_ERROR = "__TRANSLATION_ERROR__"

        

    #---#  Utility for error reporting

    def report_error(self, error_text, inputString = "NONE"):
        print("[",self.name,"] ERROR -", error_text)
        if inputString != "NONE" : print("[",self.name,"] +-->>  ", inputString)        
        return self.TRANSLATION_ERROR


    #---#  Utilities for variables fields identification
    
    def get_token(self, targetString):

        sToken = ""
        sToken_pos = 0

        for c in targetString:

            if ((c.isalnum()) or (c == '_')):
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

            t1, t1_pos = self.get_token(targetString[stringShift:])

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

        return result



    # This assumes string starting with "."
    # If a feature is found, its presence in the variable's dictionary will be checked in the main function
    def find_feature(self, targetString):
        result = "NONE"

        if (len(targetString) < 2) or (targetString[0] != "."):
            return result

        t1, t1_pos = self.get_token(targetString[1:])

        if t1_pos != 0:
            self.report_error("Wrong-formed feature filed  "+t1, targetString)

        if t1 != "":
            result = t1

        return result




    ##########  Methods for the string translation  ###############################

    def translate_string(self, inputString):

        if inputString == "":
            return inputString

        sHeader     = ""
        varName     = "NONE"
        varIndex    = "NONE"
        varFeature  = "NONE"
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



        ### Search for an index field

        tempIndex = self.find_index(inputString[string_shift:])

        if tempIndex == "NONE":
            if self.ID.type_with_index(varType):
                return self.report_error("Index field expected for "+varType+" variable  "+varName, inputString)
        else:
            if not self.ID.type_with_index(varType):
                return self.report_error("Index field found for "+varType+" variable  "+varName, inputString)

            string_shift += (len(tempIndex)+2)

            # Translate index field - Recursive application
            varIndex = self.translate_string(tempIndex)



        ### Search for a feature

        varFeature = self.find_feature(inputString[string_shift:])

        if varFeature == "NONE":

            if self.ID.type_with_features(varType):
                return self.report_error("Feature field expected for "+varType+" variable  "+varName, inputString)

        else:
            if self.ID.type_with_features(varType):

                ### Check if the feature found is present in the dictionary of the variable
                if not self.ID.has_this_feature(varName, varFeature):
                    return self.report_error("Feature   "+varFeature+"   not in the dictionary for "+varType+" variable  "+varName, inputString)

                string_shift += (len(varFeature)+1)

            else:
                # Feature present for wrong variable type (scalar or vector)
                return self.report_error("Feature   "+varFeature+"   not expected for "+varType+" variable  "+varName, inputString)
                


        ### Select the footer - Recursive application

        sFooter = self.translate_string(inputString[string_shift:])



        ###  Build the translated string using the method specific of the loaded interface

        outputString = sHeader+self.ID.convert(varName, varIndex, varFeature)+sFooter

        if self.TRANSLATION_ERROR in outputString:     outputString = self.TRANSLATION_ERROR


        return outputString
