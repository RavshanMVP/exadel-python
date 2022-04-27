import abc
class AbstractConverter(abc.ABC):
   @abc.abstractmethod
   def convert(self, input,output):
        pass

class jsonTOcsv(AbstractConverter):
    def convert(self, input, output):
        with open(input, 'r') as json_file:
            try:
                dictionary = eval(json_file.read())
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
                    with open(output, "w") as csv_file:
                        for i in final:
                            csv_file.write(",".join(i)+"\n")
            except:
                print("There is some error in json file")

class csvTOjson(AbstractConverter):
    def convert(self, input, output):
        with open(input,'r') as csv_file:
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

        with open(output,'w') as json_file:
            json_file.write(final_str)

c = csvTOjson()
c.convert("input.csv", "output.json")
j = jsonTOcsv()
j.convert("input.json", "output.csv")