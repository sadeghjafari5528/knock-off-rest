from datatypes import DataType

class JsonSerializer:
    
    def serialize(self , text):
        datatype = DataType("json")
        from json import loads
        datatype.setData(loads(text))
        return datatype


    def deserialize(self , data):
        if data.getType() == "json":
            return str(data.getData())
        else:
            raise Exception("InvalidType error : type of data in JsonSerializer must be json")
