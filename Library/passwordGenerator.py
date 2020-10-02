import Library.dictionairs as lib_dict
from random import randint
import math

DEBUG = False

class PasswordGenerator:
    def __init__(self):
        self.dicionario : lib_dict.Dicionario
        self.is_missing_dictonair = True
        self.uper = 0.00
        self.sybols = 0.00
        self.numbers = 0.10
        self.size = 8
        self.allow_filling_with_numbers = True

    def load_dictionairs(self,data):
        lista = False
        if type(data) is list:
            if type(data[0]) is lib_dict.Dicionario:
                self.dicionario = data[0]
            if len(data) > 1:
                for dicto in data[1:]:
                    if not (type(dicto) is lib_dict.Dicionario):
                        raise ValueError("Data type must be a Dictionair class or a list of Dictionairs class elements")
                    self.dicionario.merge(dicto)
        elif type(data) is lib_dict.Dicionario:
            self.dicionario = data
        else:
            raise ValueError("Invalid data type")
        self.is_missing_dictonair = False
    def generate_password(self,n =1):
        result = []
        if self.is_missing_dictonair:
            raise Exception("No dictionair was loaded")
        if n < 1:
            raise ValueError("Invalid value for n")
        for _ in range(n):
            password = -1
            while password == -1:
                password = self.generate_single_password()
            result.append(password)
        return result
    @staticmethod
    def generate_number(nneeded):
        if nneeded <= 0:
            raise ValueError("Numero Invalido")
        maximo = (10**nneeded)-1
        return str(randint(0,maximo))

    def generate_single_password(self):
        if self.is_missing_dictonair:
            raise Exception("No dictionare was loaded")
        dont_care = False
        if self.numbers < 0:
            number_needed = 0
            dont_care = True
        elif self.numbers == 0:
            number_needed = 0
        elif self.numbers <= 1:
            number_needed = round(self.size * self.numbers)
            if DEBUG:
                print("Numeros necessarios:{}".format(number_needed))
        else:
            raise ValueError("Number param must be a value betwen -inf and 1")
        numbers_in = 0
        password_size = 0
        raw_password = []
        if DEBUG:
            print("Iniciando geração")
        while password_size < self.size:
            if (number_needed - numbers_in) > 0:
                temp = PasswordGenerator.generate_number(number_needed - numbers_in)
                numbers_in += len(temp)
            else:
                options = list(self.dicionario.data)
                avaliable = []
                for o in options:
                    if o < (self.size - password_size):
                        avaliable.append(o)
                if len(avaliable) == 0 and self.allow_filling_with_numbers:
                    index1 = 0
                elif dont_care:
                    index1 = randint(0,len(avaliable))
                else:
                    index1 = randint(0,len(avaliable)-1)

                if index1 == len(avaliable):
                    tamanho = 0
                    if self.size - password_size > 2:
                        tamanho = randint(1,self.size-password_size)
                    else:
                        tamanho = self.size - password_size
                    temp = PasswordGenerator.generate_number(tamanho)
                else:
                    temp_list = self.dicionario.data[avaliable[index1]]
                    temp = temp_list[randint(0,len(temp_list)-1)]
            raw_password.append(temp)
            password_size += len(temp)
        final_password = ""
        while len(raw_password) > 0:
            element = raw_password[randint(0,len(raw_password)-1)]
            final_password += element
            raw_password.remove(element)
        return final_password
