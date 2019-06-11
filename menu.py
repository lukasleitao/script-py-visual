import sys
import json

from pyfiglet import Figlet
f = Figlet(font='standard')
g = Figlet(font='standard')



class Menu:
    def __init__(self):
        

        with open('config.json') as config_file:
            self.config = json.load(config_file)
            if len(self.config['usuario']):
                self.parametros = self.config['usuario'].copy()
            else:
                self.parametros = self.config['default'].copy()

        print(f.renderText('Menu Principal'))
        self.toString()
        self.menu()
  

    def menu(self):              

        escolha = input('''
        [1] - Endereço da Câmera
        [2] - Quantidade de Quadros por segundo
        [3] - Codec de vídeo
        [4] - Tamanho do Buffer (tempo de vídeo)
        [5] - Resolução do vídeo
        [6] - Mostrar valor das variáveis
        [7] - Salvar configuração atual
        [8] - Retornar as configurações originais
        [9] - Começar a gravação
        [10] - Sair\n
        Escolha uma das opções acima: ''')

        if escolha == '1':
            self.change_camera() 
            self.change_configuracao()           
        elif escolha == '2':
            self.change_quadros()
            self.change_configuracao()  
        elif escolha == '3':
            self.change_codec() 
            self.change_configuracao()             
        elif escolha == '4':
            self.change_buffer() 
            self.change_configuracao()            
        elif escolha == '5':
            self.change_resolucao()
            self.change_configuracao()  
        elif escolha == '6':
            self.toString()
        elif escolha == '7':
            self.salvar_configuracao_atual()        
        elif escolha == '8':
            self.retornar_configuracao_default()
        elif escolha == '9':
            return
        elif escolha == '10':
            sys.exit()
        else:
            print('\n\t[INFO] Você digitou um valor incorreto')
            print('\n\t[INFO] Por favor, tente novamente')
            self.menu()

        self.menu()
    
    def change_quadros(self):
        try:                
            self.parametros['fps'] = int(input('\tDigite a quantidade de quadros por segundo: '))
        except:
            print("\n\t[INFO] Valor inválido, tente novamente")
            self.menu() 
    
    def change_buffer(self):
        try:                
            self.parametros['buffer'] = int(input('\tDigite o tamanho do buffer: '))
        except:
            print("\n\t[INFO] Valor inválido, tente novamente")
            self.menu() 
    
    def change_resolucao(self):
        try:
            self.parametros['resolucao_w'] = int(input("\tDigite a quantidade de pixels horizontais: "))
        except:
            print("\n\t[INFO] Valor inválido, tente novamente")
            self.menu()

    def change_camera(self):
        self.parametros['camera'] = input('\tDigite o endereço da câmera: ')

    def change_codec(self):
        self.parametros['codec'] = input('\tDigite o codec desejado: ')

    def change_configuracao(self):
        self.parametros['configuracao'] = 'usuario'

    def salvar_configuracao_atual(self):      
        self.config['usuario'].update(self.parametros)
        
        with open('config.json', 'w') as fp:
            json.dump(self.config, fp) 
        
        print("\n\t[INFO] Arquivo de configuração salvo")
        self.__init__()

    def retornar_configuracao_default(self):
        self.config['usuario'] = {}
        

        with open('config.json', 'w') as fp:
            json.dump(self.config, fp) 
        
        print("\n\t[INFO] Arquivo de configuração salvo, configurações default restauradas")
        self.__init__()



    def toString(self):
        print(g.renderText('Parametros'))
        print('\n')
        print('+--------------------------+----------------------------------------------------------------------+')
        print('|{:^26}|{:^70}|'.format("NOME DO PARÂMETRO","VALOR DO PARÂMETRO"))
        print('+--------------------------+----------------------------------------------------------------------+')
        for parametro,elemento in self.parametros.items():
            print('|{:^26}|{:^70}|'.format(parametro, elemento))            
        print('+--------------------------+----------------------------------------------------------------------+')
