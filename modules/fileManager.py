import os, json, shutil

class fileManager:
    def readJson(self, json_path):
        data = open(json_path, encoding="utf-8")
        file = json.load(data,)
        
        return file    

    def nameDecoder(self, file_name):
        names_path = './config/nomenclaturas.json'
        name_meanings = self.readJson(names_path)
        name_properties = file_name.upper().split(".")

        produto, tipo, familia = name_properties[0], name_properties[1], name_properties[2]
        numero_sequencia, numero_variavel = name_properties[3], name_properties[4]
        bitola, material = name_properties[5][0], name_properties[5][1]

        name_properties = {
            "name": file_name,
            "produto": name_meanings["produtos"][produto]["nome"].capitalize(),
            "tensao": name_meanings["produtos"][produto]["tensao"].capitalize(),
            "tipo": name_meanings["tipos"][tipo].capitalize(),
            "familia": name_meanings["familias"][familia].capitalize(),
            "numero_sequencia": numero_sequencia,
            "numero_variavel": numero_variavel,
            "material": name_meanings["materiais"][material].upper(),
            "bitola": name_meanings["bitolas"][bitola].upper()
        }
        return name_properties

    def fileRootPath(self, file):
        paths = self.readJson('./config/config.json')
        root_path = paths["CAMINHO_PADRAO"]

        file_path = f"{root_path}/{file['tensao']} TENSÃO/{file['produto']}/PEÇA/{file['familia']}"
            
        file["caminho_padrao"] = file_path.upper()

        return file

    def fileInfo(self, from_path):
        files_on_path = os.listdir(from_path)
        files = []
        failed = []

        for file in files_on_path[2:]:
            try:
                filename, extension = os.path.splitext(file)
                extension = extension[1:]
                name_info = self.nameDecoder(filename)
                name_info = self.fileRootPath(name_info)

                if extension == "": extension = 'folder'

                name_info["extension"] = extension

                files.append(name_info)
            except:
                failed.append(file)
                continue
            
        return files
    
    def copy(self, to_path, extension):
        files_info = []
        found = []
        not_found = []

        valid_extensions = [extension] #Redundante -> Substituir por extension
        files_info = self.fileInfo(to_path)

        for file in files_info:      
            file_name = f"{file['name']}.{file['extension']}"

            if file['extension'].lower() not in valid_extensions: continue
            if file['extension'].isupper(): self.extensionToLower(file, to_path) # If the file extesion is in uppper case calls the function to rename the extesion to lower case

            try:
                print(f"[Copiando]: {file_name}")

                if file['produto'].lower() == 'new piccolo' or file['produto'].lower() == 'invólucro':
                    defaut_path = f"{file['caminho_padrao'].upper()}/DFTS NOVOS/{file_name}"

                    # Copy2 presrve the original file metadata -> https://docs.python.org/3.3/library/shutil.html#shutil.copy2
                    
                    shutil.copy2(defaut_path, f"{to_path.upper()}/{file_name}")

                    found.append(file['name'])
                    continue # Check if needed

                shutil.copy2(f"{file['caminho_padrao'].upper()}/PEÇAS/{file_name}", f"{to_path.upper()}/{file_name.upper()}")

            except:
                not_found.append(file['name'])
                continue
            
        self.logFiles(to_path, {"found": found, "not_found": not_found})

        return not_found

    def extensionToLower(self, file, from_path):
        #filename, extension = os.path.splitext(file) #Extension with dot
        filename, extension = file['name'], file['extension']

        file_name = f"{filename}.{extension}"
        new_name = f"{filename}.{extension.lower()}"

        os.rename(f'{from_path}\{file_name}', f'{from_path}\{new_name}')
        return

    def logFiles(self, to_path, file_status):
        f = open(f"{to_path}\Copy DFT log.txt", "w")

        f.write(f"not_found: {str(file_status['not_found'])} \n\n found: {str(file_status['found'])}")
        f.close()

    def sendToMachines(from_path):
        pass

    def rename(self, from_path):
        files = self.fileInfo(from_path)
        for file in files:
            try:
                new_filename = f'{from_path}/{file.name}.DFT'

                if file.extension == "dft":
                    os.rename(f'{from_path}/{file.name}.{file.extension}', new_filename)
            except:
                continue