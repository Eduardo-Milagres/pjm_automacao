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
            'name': file_name,
            'produto': name_meanings['produtos'][produto]['nome'].capitalize(),
            'tensao': name_meanings['produtos'][produto]['tensao'].capitalize(),
            'tipo': name_meanings['tipos'][tipo].capitalize(),
            'familia': name_meanings['familias'][familia].capitalize(),
            'numero_sequencia': numero_sequencia,
            'numero_variavel': numero_variavel,
            'material': name_meanings['materiais'][material].upper(),
            'bitola': name_meanings['bitolas'][bitola].upper()
        }
        return name_properties

    def fileRootPath(self, file: object) -> object:
        """
            Adiciona a propriedade 'CAMINHO_PADRÃO' ao objeto da peça a partir da pasta base de biblioteca de projetos (CAMINHO_PADRÃO) contida no arquivo /config/config.json.

            Parameters:
                file: Objeto com as informações da peça

            Returns:
                Acrescenta o parâmetro "caminho_padrao" ao objeto da peça.
                
            Examples:
                >>> file = {
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
                >>> fileRootPath(file)
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
                    'caminho_padrao': Z:/PRODUTO/PADRONIZADO/MÉDIA TENSÃO/NEW PICCOLO/PEÇA/BASE
                }
                
        """
                
        paths = self.readJson('./config/config.json')
        root_path = paths['CAMINHO_PADRAO']

        file_path = f"{root_path}/{file['tensao']} TENSÃO/{file['produto']}/PEÇA/{file['familia']}"
            
        file['caminho_padrao'] = file_path.upper()

        return file

# ToDo
# Exemples: passar o argumento da função
    def fileInfo(self, from_path: str) -> list[object]: # Verificar função
        """
            Cria uma lista com todas as informações das peças de um diretório. 

            Parameters:
                from_path: Caminho do diretório com os arquivos que se deseja obter as informações.

            Returns:
                Uma lista de objetos com as informações das peças do diretório passado.
                
            Examples:
                >>> fileInfo('')
                [
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
                        'caminho_padrao': 'Z:/PRODUTO/PADRONIZADO/MÉDIA TENSÃO/NEW PICCOLO/PEÇA/BASE'
                        'extension': '.DFT'
                    },
                    ...
                ]
                
        """
        files_on_path = os.listdir(from_path)
        files = []
        failed = []
        
        print(f'[files on path]: {files_on_path}')

        for file in files_on_path[2:]:
            try:
                filename, extension = os.path.splitext(file)
                extension = extension[1:]
                name_info = self.nameDecoder(filename)
                name_info = self.fileRootPath(name_info)

                if extension == '': extension = 'folder'

                name_info['extension'] = extension

                files.append(name_info)
                print(name_info['name'])
            except:
                failed.append(file)
                continue
        return files

# ToDo
# Exemplos: adiconar diretório destino  
    def copy(self, to_path: str, extension: list[str]) -> list[str]:
        """
            Copia os arquivos com a extensão passada do diretório padrão para o diretório passado. 

            Parameters:
                to_path: Caminho do diretório para onde os arquivos serão copiados.
                extension: Lista com as extensões dos arquivos que deseja copiar.

            Returns:
                Uma lista de strings com os nomes dos arquivos não encontrados no diretório padrão.
                
            Examples:
                Arquivos no diretório destino ():
                    NP.P.BA.001.01.BA.DFT
                    NP.P.SU.008.03.BB.DFT
                    NP.P.FE.005.07.CB-XXXX.DFT
                >>> copy('', 'DFT')
                [
                    ['NP.P.FE.005.07.CB-XXXX']
                ]     
        """
        files_info = []
        found = []
        not_found = []
        new_piccolo = 'new piccolo'
        involucro = 'involucro'

        valid_extensions = [extension] #Redundante -> Substituir por extension
        files_info = self.fileInfo(to_path)

        for file in files_info:      
            file_name = f"{file['name']}.{file['extension']}"

            if file['extension'].lower() not in valid_extensions: continue
            if file['extension'].isupper(): self.extensionToLower(file, to_path)

            try:
                if file['produto'].lower() == new_piccolo or file['produto'].lower() == involucro:
                    defaut_path = f"{file['caminho_padrao'].upper()}/DFTS NOVOS/{file_name}"
                else:
                    defaut_path = f"{file['caminho_padrao'].upper()}/{file_name}"

                # Copy2 presrve the original file metadata -> https://docs.python.org/3.3/library/shutil.html#shutil.copy2
                shutil.copy2(defaut_path, f"{to_path.upper()}/{file_name}")

                found.append(file['name'])
                continue # Check if needed

            except:
                print(f'[Não encontrado]: {file_name}')
                not_found.append(file['name'])
                continue
            
        self.logFiles(to_path, {'found': found, 'not_found': not_found})

        return not_found

# ToDo
# Exemples: Incluir caminho
    def extensionToLower(self, file: str, from_path: str):
        """
            Muda a extensão do arquivo para minúscula (lower case). 

            Parameters:
                file: Arquivo com a extensão em maiúscula.
                from_path: Caminho do diretório onde a extensão dos arquivos será verificada.
                
            Examples:
                >>> extensionToLower('NP.P.BA.001.01.BB.DFT', '')
                NP.P.BA.001.01.BB.dft
        """
        filename, extension = file['name'], file['extension']

        file_name = f'{filename}.{extension}'
        new_name = f'{filename}.{extension.lower()}'

        os.rename(f'{from_path}\{file_name}', f'{from_path}\{new_name}')
        return

# ToDo
# Exemples
    def logFiles(self, to_path: str, file_status: object[str]):
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

    def sendToMachines(from_path):
        pass

    def rename(self, from_path): # Igual a extensionToLower?
        files = self.fileInfo(from_path)
        for file in files:
            try:
                new_filename = f'{from_path}/{file.name}.DFT'

                if file.extension == 'dft':
                    os.rename(f'{from_path}/{file.name}.{file.extension}', new_filename)
            except:
                continue
