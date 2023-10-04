
class translator:
    def __init__(self, interface = "NONE", name = "translator"):
        self.name = name
        self.tI = interface
        print("[",self.name,"] translator object created, with interface ",self.tI.name)
        print(self.tI)


    #    def set_interface(self, interface):
    #        self.tI = interface
    #        print("> translator.set_interface called")
    #        print(self.tI)


    #---#  Utility for error reporting

    def report_error(self, inputString, error_text):
        print("[",self.name,"] ERROR -", error_text)
        print("[",self.name,"] +-->>  ", inputString)        
        return "__TRANSLATION_ERROR__"


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

            if self.tI.is_defined(t1):
                return t1, self.tI.get_type(t1), (stringShift+t1_pos)
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
            self.report_error(targetString, "Wrong-formed feature filed  "+t1)

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
            if self.tI.type_with_index(varType):
                return self.report_error(inputString, "Index field expected after  "+varName)
        else:
            string_shift += (len(tempIndex)+2)

            # Translate index field - Recursive application
            varIndex = self.translate_string(tempIndex)



        ### Search for a feature

        varFeature = self.find_feature(inputString[string_shift:])

        if varFeature == "NONE":

            if self.tI.type_with_features(varType):
                return self.report_error(inputString, "Feature missing in the input string for variable  "+varName)

        else:
            if self.tI.type_with_features(varType):

                ### Check if the feature found is present in the dictionary of the variable
                if not self.tI.has_this_feature(varName, varFeature):
                    return self.report_error(inputString, "Feature   "+varFeature+"   not in the dictionary for variable   "+varName)

                string_shift += (len(varFeature)+1)

            else:
                # Feature present for wrong variable type (scalar or vector)
                return self.report_error(inputString, "Feature   "+varFeature+"   not expected for variable   "+varName)
                

        ### Select the footer - Recursive application

        sFooter = self.translate_string(inputString[string_shift:])


        ###  Build the translated string using the method specific of the loaded interface

        outputString = sHeader+self.tI.convert(varName, varIndex, varFeature)+sFooter


        return outputString
