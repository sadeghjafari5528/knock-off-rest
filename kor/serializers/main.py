from serializer import JsonSerializer
from datatypes import DataType

if __name__ == "__main__":
    j = DataType(type="json")
    j.setData(["1" , "sfda"])
    serializer = JsonSerializer()
    x = serializer.deserialize(j)
    print(x , type)