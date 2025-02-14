import os
import json
import shutil

class fileManager:
    def readJson(self, json_path: str) -> object:
        """
            Converte um arquivo Json para um objeto python.

            Parameters:
                json_path: Caminho do arquivo python

            Returns:
                Objeto com os dados do arquivo .json
        """
        data = open(json_path, encoding='utf-8')
        file = json.load(data,)
        
        return file    

    def nameDecoder(self, file_name: str) -> object:
        """
            Decodifica o nome do arquivo de acordo com o código GIMI

            Note:
                A codificação GIMI está armazenada no arquivo config/nomenclatura.json

            Parameters:
                file_name: Nome do arquivo a ser decodificado

            Returns:
                Objeto com as informações contidas no código -> {nome, produto, tensão, tipo, família, número sequencial, número da variável, material e bitola}

            Examples:
                >>> nameDecoder("NP.P.BA.001.01.BB")
                {
                    'name': 'NP.P.BA.001.01.BB',
                    'produto': New Piccolo'
                    'tensao': 'média',
                    'tipo': 'peça',
                    'familia': 'base',
                    'numero_sequencia': 001,
                    'numero_variavel': 01,
                    'material': 'NBR 7008 ZC',
                    'bitola': 14
                }
        """
        names_path = './config/nomenclaturas.json'
        name_meanings = self.readJson(names_path)
        name_properties = file_name.upper().split('.')
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
        #pprint(name_properties)
        return name_properties

    def fileRootPath(self, file) -> object:
        """
            Adiciona o caminho caminho da peça na pasta padrão de acordo com o nome do arquivo no objeto com as informações da peça.

            Parameters:
                file: Objeto do arquivo em que a propriedade será adicionada

            Returns:
                Objeto com as informações contidas no código -> {nome, produto, tensão, tipo, família, número sequencial, número da variável, material, bitola e caminho_padrao}

            Examples:
                >>> peça = {
                    'name': 'NP.P.BA.001.01.BB',
                    'produto': New Piccolo'
                    'tensao': 'média',
                    'tipo': 'peça',
                    'familia': 'base',
                    'numero_sequencia': 001,
                    'numero_variavel': 01,
                    'material': 'NBR 7008 ZC',
                    'bitola': 14
                }

                >>> FileRootPath(peça)
                {
                    'name': 'NP.P.BA.001.01.BB',
                    'produto': New Piccolo'
                    'tensao': 'média',
                    'tipo': 'peça',
                    'familia': 'base',
                    'numero_sequencia': 001,
                    'numero_variavel': 01,
                    'material': 'NBR 7008 ZC',
                    'bitola': 14
                    'caminho_padrão': 'PRODUTO/PADRONIZADO/MÉDIA TENSÃO/NEW PICCOLO/PEÇA/BASE'
                }
        """
        paths = self.readJson('./config/config.json')
        root_path = paths["CAMINHO_PADRAO"]

        file_path = f"{root_path}/{file['tensao']} TENSÃO/{file['produto']}/PEÇA/{file['familia']}"
        
        if file['produto'].lower() == 'caixa de medição':
            file_path = f"{root_path}/{file['tensao'].upper()} TENSÃO/{file['produto'].upper()}/PEÇAS"

        file["caminho_padrao"] = file_path.upper()

        return file

    def fileInfo(self, from_path: str) -> list[object]:
        """
            Adiciona a uma lista todas as peças encontradas no caminho passado com as informação importante sobre o arquivo.

            Parameters:
                from_path: Caminho da pasta com os DFTs

            Returns:
                Lista de objetos com as informações contidas no código para todas as peças da pasta passada.

            Examples:
                >>> filinfo("/caminho_dos_DFTS")
                {
                    'name': 'NP.P.BA.001.01.BB',
                    'produto': New Piccolo'
                    'tensao': 'média',
                    'tipo': 'peça',
                    'familia': 'base',
                    'numero_sequencia': 001,
                    'numero_variavel': 01,
                    'material': 'NBR 7008 ZC',
                    'bitola': 14
                },
                {
                    'name': 'NP.P.FE.001.01.CB',
                    'produto': New Piccolo'
                    'tensao': 'média',
                    'tipo': 'peça',
                    'familia': 'fechamento',
                    'numero_sequencia': 001,
                    'numero_variavel': 01,
                    'material': 'NBR 7008 ZC PRÉ PINTADO',
                    'bitola': 14
                },
                {...}
        """
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
       
    def copy(self, to_path: str, extension: str) -> list[str]:
        """
            Copia os arquivos com a extensão passada do caminho padrão para o caminho especificado.

            Parameters:
                to_path: Caminho da pasta onde os arquivos serão copiados.
                extension: Extensão dos arquivos a serem copiados.

            Returns:
                Uma lista de strings com o nome dos arquivos que não foram encontrados no caminho padrão.

            Examples:
                >>> filinfo("/caminho_dos_DFTS", ".dft")
                [NP.P.FE.001.01.CB, NP.P.BA.001.01.BB, ...]
                
        """
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
                defaut_path = f"{file['caminho_padrao'].upper()}/{file_name}"
                print(f"[Copiando]: {defaut_path}")

                shutil.copy2(defaut_path, f"{to_path.upper()}/{file_name}")

                found.append(file['name'])

                #if file['produto'].lower() == 'new piccolo' or file['produto'].lower() == 'invólucro':
                    #defaut_path = f"{file['caminho_padrao'].upper()}/DFTS NOVOS/{file_name}"
                #    defaut_path = f"{file['caminho_padrao'].upper()}/{file_name}"


                    # Copy2 presrve the original file metadata -> https://docs.python.org/3.3/library/shutil.html#shutil.copy2
                    
                #    shutil.copy2(defaut_path, f"{to_path.upper()}/{file_name}")

                #    found.append(file['name'])
                #    continue # Check if needed

                shutil.copy2(f"{file['caminho_padrao'].upper()}/PEÇAS/{file_name}", f"{to_path.upper()}/{file_name.upper()}")

            except:
                not_found.append(file['name'])
                continue
            
        self.logFiles(to_path, {"found": found, "not_found": not_found})

        return not_found

    def extensionToLower(self, file, from_path: str) -> None:
        """
            Altera a extensão do arquivo para letras minúsculas

            Parameters:
                file: Arquivo que terá a extensão alterada para minpuscula.
                from_path: Caminho do arquivo que terá a extensão alterada para minúscula.
            
            Examples:
                >>> extensionToLower("NP.P.FE.001.01.CB.DFT", "/caminho_dos_DFTS")
                >>> /caminho_dos_DFTS/NP.P.FE.001.01.CB.dft
        """

        #filename, extension = os.path.splitext(file) #Extension with dot
        filename, extension = file['name'], file['extension']

        file_name = f"{filename}.{extension}"
        new_name = f"{filename}.{extension.lower()}"


        os.rename(f'{from_path}\{file_name}', f'{from_path}\{new_name}')
        return

# ToDo
# Exemples
    def logFiles(self, to_path: str, file_status) -> None :
        """
            Gera um arquivo de texto no diretório passado com as peças encontradas 
            e não encontradas no diretório padrão 

            Parameters:
                to_path: Caminho do diretório os arquivos serão verificada.
                file_status: Status da peça encontrada ou não.
                
            Examples:
                >>> 
        """

        file = open(f'{to_path}\Copy DFT log.txt', 'w')

        file.write(f"not_found: {str(file_status['not_found'])} \n\n found: {str(file_status['found'])}")
        file.close()

    def rename(self, from_path: str) -> None:
        """
            Lista os arquivos do diretório passado e verifica se o arquivo tem a 
            extensão em letras minúscula, senão renoia a extensão para letras maiúsculas.  

            Parameters:
                to_path: Caminho do diretório dos arquivos que serão verificados.
                
            Examples:
                >>> rename("PRODUTO/PADRONIZADO/MÉDIA TENSÃO/NEW PICCOLO/PEÇA/BASE")
        """
        files = self.fileInfo(from_path)
        for file in files:
            try:
                new_filename = f'{from_path}/{file.name}.DFT'

                if file.extension == "dft":
                    os.rename(f'{from_path}/{file.name}.{file.extension}', new_filename)
            except:
                continue

