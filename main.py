from machine  import ADC, Pin
from utime import sleep, localtime, time
import uos

#CONFIG LEDS
ledpower_machine = Pin(25, Pin.OUT, value=1)
ledpower_green = Pin(0, Pin.OUT, value=0)
ledpower_red = Pin(1, Pin.OUT, value=0)
led_wash = Pin(3, Pin.OUT, value=0)
led_enxague = Pin(4, Pin.OUT, value=0)
led_centrifugation = Pin(2, Pin.OUT, value=0) 

#POTENTIOMETERS
#pt_level = ADC(0)
pt_program = ADC(1)

#SENSOR DE PRESSAO
pressure = Pin(12, Pin.IN, Pin.PULL_DOWN) 

#BUTTONS
btn_power = Pin(14, Pin.IN, Pin.PULL_DOWN)
btn_turbo = Pin(15, Pin.IN, Pin.PULL_DOWN)

#BIP
buzzer = Pin(13, Pin.OUT)

#RELays
softner = Pin(5, Pin.IN)
engine_left = Pin(6, Pin.OUT, value=0)
engine_right = Pin(7, Pin.OUT, value=0)
bomb_water = Pin(8, Pin.OUT, value=0)
solenoid = Pin(9, Pin.OUT, value=0)

#VARIAVEIS
normal = 0.7
turbo = 0.35
agitar = 3

def standby():
    log('STANDBY')
    ledpower_green.value(0)
    ledpower_red.value(1)
    while btn_power.value() == 0:
        sleep(.1)
    log('BOTAO POWER ACIONADO')
    log('INICIANDO PROGRAMAÇÃO KING WASH')
    ledpower_red.value(0)
    ledpower_green.value(1)
    changePrograms()

def changePrograms():
    
    program = setPrograms()

    if program >= 1 and program <= 3:
        if program == 3:
            leds('wash')
            log('LAVAGEM LEVE')
            solenoid.on()
            log('ENCHENDO...')
            while pressure.value() == 0:
                sleep(1)
                while btn_power.value() == 0:
                    off()
                    ledpower_green.off()
                    ledpower_red.on()
                    sleep(1)
                ledpower_red.off()
                ledpower_green.on()
                solenoid.on()
            log('NIVEL DE ÁGUA ATINGIDO')
            solenoid.off()
            off()
            wash(8)
            leds('enxague')
            enxague()
            leds('centrifugation')
            centrifugation()
            shutdown()
        if program == 2:
            leds('wash')
            log('LAVAGEM MODERADA')
            solenoid.on()
            log('ENCHENDO...')
            while pressure.value() == 0:
                sleep(1)
                while btn_power.value() == 0:
                    off()
                    ledpower_green.off()
                    ledpower_red.on()
                    sleep(1)
                ledpower_red.off()
                ledpower_green.on()
                solenoid.on()
            log('NIVEL DE ÁGUA ATINGIDO')
            solenoid.off()
            wash(16) 
            leds('enxague')
            enxague()
            leds('centrifugation')
            centrifugation()
            shutdown()
        if program == 1:
            leds('wash')
            log('LAVAGEM PESADA')
            solenoid.on()
            log('ENCHENDO...')
            while pressure.value() == 0:
                sleep(1)
                while btn_power.value() == 0:
                    off()
                    ledpower_green.off()
                    ledpower_red.on()
                    sleep(1)
                ledpower_red.off()
                ledpower_green.on()
                solenoid.on()
            log('NIVEL DE ÁGUA ATINGIDO')
            solenoid.off()
            wash(24) 
            leds('enxague')
            enxague()
            leds('centrifugation')
            centrifugation()
            shutdown()
    elif program == 4:
        leds('enxague')
        log('ENXAGUE')
        enxague()
        off()
        leds('centrifugation')
        centrifugation()
        shutdown()
    elif program == 5:
        log('CENTRIFUGAÇÃO')
        leds('centrifugation')
        centrifugation()
        shutdown()

def wash(cycles):
    log('INICIANDO AGITAÇÃO')
    program = setPrograms()
    for i in range(cycles):
        log(f'WASH CICLO GERAL {i+1}/{cycles}')
            for c in range(100):
                log(f'WASH AGITAÇÃO {c+1}/{100}')
                if btn_turbo.value() == 1:
                    wait = turbo
                    log('TURBO ON')
                else:
                    wait = normal
                engine_left.value(1)
                sleep(agitar)
                engine_left.value(0)
                sleep(wait)
                engine_right.value(1)
                sleep(agitar)
                engine_right.value(0)
                sleep(agitar)
                fill()
                log(f'CICLO: {c+1}')
                programChanged(program)
                while btn_power.value() == 0:
                    sleep(1)
            log('PAUSA MOLHO')
            sleep(60)



def setPrograms():

    if pt_program.read_u16() >= 0 and pt_program.read_u16() <= 18000:
        program = 1
    elif pt_program.read_u16() > 18000 and pt_program.read_u16() <= 30000:
        program = 2
    elif pt_program.read_u16() > 3000 and pt_program.read_u16() <= 44000:
        program = 3
    elif pt_program.read_u16() > 44000 and pt_program.read_u16() <= 55053:
        program = 4
    elif pt_program.read_u16() > 55043:
        program = 5
    else:
        program = 2

    return program  

def enxague():
    bomb_water.value(1)
    sleep(120)#120
    log('INICIANDO MINI CENTRIFUGAÇÃO DO ENXAGUE')
    for e in range(4):
        engine_right.value(1)
        sleep(7)#7
        engine_right.value(0)
        sleep(12)#12
        log(f'{e+1}/4')
    log('CENTRIFUGAÇÃO DE 2 MINUTOS')
    engine_right.value(1)
    sleep(120)#mudar 120
    engine_right.value(0)
    sleep(20)#20
    bomb_water.value(0)
    program  = setPrograms()
    solenoid.on()
    log('LIBERANDO AMACIANTE')
    softner.init(Pin.OUT)
    log('ECHENDO RESERVATORIO')
    while pressure.value() == 0:
        sleep(3)
    log(f'NIVEL DE AGUA ATINGIDO')
    solenoid.off()
    softner.init(Pin.IN)
    wash(8)
            
    
def centrifugation():
    leds('centrifugation')
    log('MODO CENTRIFUGAÇÃO')
    bomb_water.value(1)
    log('BOMBA DE VACUO LIGADA')
    sleep(120)
    for i in range(5):
        engine_right.value(1)
        sleep(7)
        engine_right.value(0)
        sleep(12)
        log(f'{i+1}/5')
    log('1/3 CENTRIFUGAÇÃO CONCLUIDA')
    for i in range(4):
        engine_right.value(1)
        sleep(60)
        engine_right.value(0)
        sleep(15)
        log(f'{i+1}/4')
    log('2/3 CENTRIFUGAÇÃO CONCLUIDA')
    for i in range(2):
        engine_right.value(1)
        sleep(120)
        engine_right.value(0)
        sleep(15)
    log('3/3 CENTRIFUGAÇÃO CONCLUIDA')
    bomb_water.value(0)
    log('BOMBA DE VACUO DESLIGADA')
        
def leds(power=''):
    led_wash.value(0)
    led_enxague.value(0)
    led_centrifugation.value(0)
    if power == 'wash':
        led_wash.value(1)
    elif power == 'enxague':
        led_enxague.value(1)
    elif power == 'centrifugation':
        led_centrifugation.value(1)
    else:
        pass

def shutdown():
    off()
    leds()
    while btn_power.value() == 1:
        buzzer.on()
        ledpower_green.value(1)
        sleep(.25)
        buzzer.off()
        ledpower_green.value(0)
        sleep(.25)
        log('ESPERANDO DESLIGAR BOTAO')
    ledpower_green.value(0)
    sleep(1)
    standby()

def programChanged(program):
    programbefore = program
    program_now = setPrograms()
    if programbefore != program_now:
        programbefore = program_now
        log('FUNÇÃO ALTERADA, REPROGRAMANDO.')
        changePrograms()
        shutdown()

def log(msg):
    times = localtime(time())
    timenow = f"[{times[2]}/{times[1]}/{times[0]} as {times[3]}:{times[4]}:{times[5]}] => "
    msg = timenow +msg
    with open('log.txt', 'a') as f:
        f.write(msg + '\n')
    print(msg) # opcional: também exibir o log no console

def off():
    softner.init(Pin.IN)
    engine_left.off()
    engine_right.off()
    bomb_water.off()
    solenoid.off()

def fill():
    if pressuree.value() == 0:
        solenoid.on()
        while pressure.value == 0:
            sleep(3)
        solenoid.off()            

log('=================================  INIT ===========================================')           

off()
standby()
#enxague()