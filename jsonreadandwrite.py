import json
def write_sample_json(data,filename):
  
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
        return filename
def read_sample_json(filename):
    with open(filename, "r") as f:
        loaded_data = json.load(f)
    return loaded_data
    
d={1:"One",2:"Two"}
write_sample_json(d,"mydata.json")
x=read_sample_json("test.json")
print(x)
    