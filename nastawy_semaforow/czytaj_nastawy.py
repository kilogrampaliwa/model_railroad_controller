

class nastawy:

    def __init__(self):

       self.__dict_creator(self.__load_lines("nastawy_semaforow/nastawa_semafory.txt"))


    def __load_lines(self, address):
        lines = []
        with open(address, 'r',encoding='utf-8') as file:
            all_lines = file.readlines()
            for x in all_lines:
                x = self.__remove_whitespace(x)
                if x[0] == '@': lines.append(x[1:])
        return lines

    def __remove_whitespace(self, text):
        return ''.join(text.split())

    def __dict_creator(self, lines):

        self.__dict_out = {}

        for x in lines:
            dict_semafor = {}
            x_spt = x.split('|')
            for n in x_spt[1:]:
                dict_komora = {
                    "sygnal":False,
                    "mruganie": False
                }
                if len(n)==3: dict_komora['mruganie'] = True
                dict_komora['sygnal'] = n[1]
                dict_semafor[n[0]] = dict_komora.copy()
            self.__dict_out[x_spt[0]] = dict_semafor.copy()


    def __call__(self): return self.__dict_out

