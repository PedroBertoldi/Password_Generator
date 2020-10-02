import os
import multiprocessing

DEBUG = False

class Dicionario:
    def __init__(self,path,isfolder=False):
        if path == "" or path == None:
            raise ValueError("folder_path must be a valid file path",1)
        if isfolder:
            if not os.path.exists(path):
                raise ValueError("path [{}] does not exist".format(path))
        else:
            if not os.path.isfile(path):
                raise ValueError("File [{}] not found".format(path))
        if DEBUG:
            print("Arquivo encontrado, atribuindo a dicionario")
        self._path = path
        self._is_folder = isfolder
        self.data = {}
        self.ext = ["txt"] #Arrumar isso daqui
    def load_dictionair(self):
        if self._is_folder:
            array_files = os.listdir(self._path)
            valid_file_name = []
            for file_name in array_files:
                extencion = file_name.split(".")
                if extencion[-1] in self.ext:
                    valid_file_name.append(self._path + "/" + file_name)
            if len(valid_file_name) == 0:
                raise ValueError("File path [{}] dos not contain any valid files".format(self._path))
            if DEBUG:
                print("Valid file names: {}".format(valid_file_name))
            with multiprocessing.Pool() as pool:
                result = pool.map(Dicionario.load_single_file, valid_file_name)
            if len(result) > 2:
                self.data = result[0]
                for single_dict in result[1:]:
                    self.merge(single_dict)
            elif len(result) == 1:
                self.data = result[0]
            else:
                raise Exception("Nenhum dicionario foi retornado")
        else:
            self.data = Dicionario.load_single_file(self._path)
    @staticmethod
    def load_single_file(path):
        data = {}
        with open(path) as file:
                for file_line in file:
                    line = file_line.strip()
                    line_len = len(line)
                    if line_len in data:
                        data[line_len].append(line.lower())
                    else:
                        temp_dict = {line_len:[line]}
                        data.update(temp_dict)                        
        return data
    @staticmethod
    def is_valid_path(path,isfolder):
        if isfolder:
            return os.path.isdir(path)
        else:
            return os.path.isfile(path)
    def merge(self, dict2):
        keys = list(dict2)
        for key in keys:
            if key in self.data:
                self.data[key] += dict2[key]
            else:
                temp_dict = {key:dict2[key]}
                self.data.update(temp_dict)