import time

btnLigar = True


def StandBy():
    while btnLigar == 0:
        #FAZER LED PISCAR VERMELHO
        print('pisca led')
        
        pass
    
    
def changePrograms():
    pass

# LAVAGEM LEVE
def Wash():
    #DETERMINAR LAVAGEM DEPOIS DE LER O POTENCIOMETRO
    #LAVAGEM LEVE, MODERADA E PESADA
    pass

# CENTRIFUGAÇÃO
def Centrifugation(): 
    pass

# ENXAGUE
def Enxague():
    pass

def waterLevel(level=2):
    #VERIFICA SENSOR E RETORNA O NIVEL
    if level == 1:
        print('NIVEL 1 WHILE ATE ENCHER NIVEL 1')
    elif level == 2:
        print('NIVEL 2 WHILE ATE ENCHER NIVEL 2')
    elif level == 3:
        print('NIVEL 3 WHILE ATE ENCHER NIVEL 3')
    Testando()   
    

def waterFill():
    #VERIFICA SE TEM AGUA ATRAVES DO SENSOR DE PRESSAO
    pass

def waterEmpty():
    pass

def Start():
    StandBy()
    
#teste
def Testando():
    teste = input('==>')
    waterLevel(int(teste))
    
Testando()