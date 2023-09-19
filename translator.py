
class translator:
    def __init__(self, interface = "NONE", name = "translator"):
        self.name = name
        self.tI = interface
        print("[",self.name,"] translator object created, with interface ",self.tI.name)
#        print(self.tI)


#    def set_interface(self, interface):
#        self.tI = interface
#        print("> translator.set_interface called")
#        print(self.tI)


    def find_closed_sb(self, targetString):
        open_sb = 1
        closed_sb_pos = -1

        for i in range(0, len(targetString)):
            c = targetString[i]
            if c == "[":
                open_sb += 1
            elif c == "]":
                open_sb -= 1

            if open_sb == 0:
                closed_sb_pos = i
                break

        return closed_sb_pos



    def first_string_position(self, stringName, targetString):
        p_string = targetString.find(stringName)
        if p_string > 0:
            if targetString[(p_string-1):p_string] == '_':
                return -1
            if targetString[(p_string-1):p_string].isalnum():
                return -1
        return p_string



    def first_obj_position(self, objName, targetString):
        s_obj = objName + "["
        return self.first_string_position(s_obj, targetString)
    


    def find_first_obj(self, targetString):
        result = "NONE"
        for obj in self.tI.OBJs_dict:
            pObj = self.first_obj_position(obj, targetString)

            if pObj >= 0:
                result = obj
                break

        return result



    # This assumes string starting with "[" and looks for the corresponding "]"
    def find_first_index(self, targetString):
        result = "NONE"

        if not (targetString[0:1] == '['):
            return result

        index_begin = 1
        index_end   = index_begin + self.find_closed_sb(targetString[index_begin:])

        if (index_begin >= 0) and (index_end > index_begin):
            result = targetString[index_begin:index_end]

        return result



    # This assumes string starting with "." - if a feature is found,
    # its presence in the object's dictionary will be checked in the main function
    def find_first_feature(self, targetString):
        result = "NONE"

        if len(targetString) < 2:
            print("find_first_feature  -  string too short! ", "++"+targetString+"++")
            return result

        if targetString[0] != ".":
            print("find_first_feature  -  string not beginning with a dot! ", "++"+targetString+"++")
            return result

        featLen = 0
        for i in range(1, len(targetString)):
            c = targetString[i]
            if (not c.isalnum()) and (not c == "_") :
                break
            featLen += 1

        if featLen < 1:
            print("find_first_feature  -  no feature found after the dot! ", "++"+targetString+"++")
            return result

        result = targetString[1:(1+featLen)]

        return result





    #########################################

    def translate_string(self, inputString):

        print("[",self.name,"] translate_string called on  ", inputString)

        if inputString == "":
            return inputString

        ### Find first object and position (looping over Dictionary's objects)

        firstObj     = self.find_first_obj(inputString)

        if firstObj == "NONE":
            return inputString

        firstObj_pos = self.first_obj_position(firstObj, inputString)

        ### Extract the header

        sHeader = inputString[0:firstObj_pos]

        ### Locate the index field

        temp_Index   = self.find_first_index(inputString[(firstObj_pos+len(firstObj)):])

        if temp_Index == "NONE":
            print("Index field expected after  ", firstObj)
            return inputString

        ### Translate the index field (recursive application)

        firstIndex     = self.translate_string(temp_Index)
        firstIndex_pos = firstObj_pos + len(firstObj) + 1

        ### Locate the feature

        firstFeature     = self.find_first_feature(inputString[(firstIndex_pos + len(firstIndex) + 1):])
        firstFeature_pos = (firstIndex_pos + len(firstIndex) + 2)

        ### Check if the feature found is present in the dictionary

        if not firstFeature in self.tI.OBJs_dict[firstObj]:
            print("translate  -  Feature  ", firstFeature, "  not in the dictionary for object  ", firstObj)
            print(" -->  ++"+inputString+"++")        
            return "__TRANSLATE_ERROR__"

        ### Translate the footer (recursive application)

        sFooter = self.translate_string(inputString[(firstFeature_pos + len(firstFeature)):])


        ###  Build the translated string using the method specific of the loaded interface
    
        outputString = sHeader+self.tI.convert(firstObj, firstIndex, firstFeature)+sFooter

        return outputString

