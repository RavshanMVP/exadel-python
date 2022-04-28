from abstract import *

class CSVtoJSON(AbstractConverter):

    def read(self, input):
        try:
            f = open(input, "r")
            counter = os.path.getsize(input)
            if (counter ==0): raise Exception("File is empty")
            return f.read()

        except FileNotFoundError:
            print("This file probably does not exist")


    def writer(self, file, output):
        try:
            f= open(file, "w")
            f.write(output)
            if (os.path.exists(output)):
                raise Exception("The file with this name already exists")
        except FileExistsError:
            print("There's other file with the same name")
        finally:f.close()

    def convert(self, input):
        csv_file = input.split("\n")
        final = []
        keys_list = []
        counter = 0
        dictionary = dict()
        for line in csv_file:
            values = line.split(",")
            if counter ==0:
                for i in values:
                    keys_list.append(i)
            else:
                try:
                    for i in range(len(keys_list)):
                        key = keys_list[i]
                        dictionary[key] = values[i]
                    final.append(dict(dictionary))
                except:
                    print("Some error")
            counter+=1
        final_str = '{"data": '

        if (counter ==1):
            final_str += "{"
            for i in range(len(keys_list)):
                final_str +='"' + str(keys_list[i]) + '" : "",'
            final_str = (final_str[:len(final_str) - 1] + "}}").replace("'",'"')
        elif (counter ==2):
            final_str += str(final[0]).replace("'", '"')+"}"
        else:
            final_str+="["
            for i in final:
                final_str+=str(i) + ",\n"
            final_str = (final_str[:len(final_str) - 2] + "]}").replace("'",'"')

        return final_str




