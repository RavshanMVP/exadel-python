from abstract import *

class JSONtoCSV(AbstractConverter):

    def read(self, input):
        try:
            f = open(input, "r")
            counter = os.path.getsize(input)
            if (counter == 0): raise Exception("File is empty")
            return f.read()
        except FileNotFoundError:
            case = False


    def Write(self, file, output):
        try:
            f= open(file, "w")
            f.write(output)
            if (os.path.exists(output)):
                raise Exception("The file with this name already exists")
            f.close()
        except FileExistsError:
            print("There's other file with the same name")

    def convert(self, input):

        try:
            with open(input,"r") as file:
                dictionary = file.read()
            dictionary = eval(dictionary)
            keys_list = (dictionary.keys())
            for j in dictionary:
                lst = dictionary[j]
                counter = 0
                final = []
                for i in lst:
                    i = dict(i)
                    if (counter == 0):
                        final.append(i.keys())
                    final.append(i.values())
                    counter += 1
                str1 =""
                for i in final:
                    str1+=(",".join(i)+"\n")
                return str1
        except SyntaxError:
            print("There is some error in json file")

