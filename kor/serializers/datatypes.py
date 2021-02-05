

class DataType :
    def __init__(self , type ,data=None):
        self.__avalibleType = {"json" : [list , dict]}
        self.__data = data
        if type in self.__avalibleType.keys():
            self.__type = type
        else:
            raise Exception("TypeNotSupported error : this serializer can not support " + str(type))
        

    def setData(self , data):
        if self.__isValidType(type(data)):
            self.__data = data
        else:
            raise Exception("InvalidType error: type must be " + self.__getStrOfAvalibleType())

    def getData(self):
        return self.__data

    def getType(self):
        return self.__type
        
    def __isValidType(self , type):
        return type in self.__avalibleType[self.__type]

    def __getStrOfAvalibleType(self):
        types = ""
        for i in range(len(self.__avalibleType[self.__type]) - 1):
            types += str(self.__avalibleType[self.__type][i]) + " or "
        types += str(self.__avalibleType[self.__type][-1])
        return types