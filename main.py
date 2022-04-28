from json_to_csv import *
from csv_to_json import *
name = input("Enter the name of the file ")
ext = input("Enter the extension .json or .csv ")

if (ext == ".csv"):
    try:
        c = CSVtoJSON()
        input = c.read(name+ext)
        if (input):
            result = c.convert(input)
            c.Write("output.json",result)
            print("csv has been converted to json")
        else: print("File probably does not exist")
    except:
        print("File is empty")

elif (ext ==".json"):
    try:
        j = JSONtoCSV()
        input = j.read(name + ext)
        input = eval(input)
        if (input):
            result = j.convert(name + ext)
            j.Write("output.csv", result)
            print("json has been converted to csv")
        else: print("File probably does not exist")
    except:
        print("File is empty")