from machine  import ADC, Pin
from utime import sleep, localtime, time

import uos

#CONFIG LEDS
ledpower_red = Pin(1, Pin.OUT)
ledpower_green = Pin(2, Pin.OUT)
led_wash = Pin(3, Pin.OUT)
led_enxague = Pin(4, Pin.OUT)
led_centrifugation = Pin(5, Pin.OUT) 

#POTENTIOMETERS
pt_level = ADC(0)
pt_program = ADC(1)

#SENSOR DE PRESSAO
pressure = ADC(2)

#BUTTONS
btn_power = Pin(17, Pin.IN, Pin.PULL_DOWN)
btn_turbo = Pin(22, Pin.IN, Pin.PULL_DOWN)

#BIP
buzzer = Pin(0, Pin.OUT)

#RELays
engine_left = Pin(21, Pin.OUT)
engine_right = Pin(20, Pin.OUT)
bomb_water = Pin(19, Pin.OUT)
solenoid = Pin(18, Pin.OUT)


def standby():
    log('MODO STANDBY - ESPERANDO APERTAR BOTAO POWER')
    ledpower_green.value(0)
    ledpower_red.value(1)
    while btn_power.value() == 0:
        sleep(0.1)
        log(f'VALOR DO SENSOR DE PRESSAO: {pressure.read_u16()}')
    ledpower_red.value(0)
    ledpower_green.value(1)
    changePrograms()

def changePrograms():
    
    level, program = setPrograms()

    if program >= 1 and program <= 3:
        if program == 1:
            leds('wash')
            log('LAVAGEM LEVE')
            waterLevel(level)
            log(f'NIVEL DE ÁGUA ATINGIDO')
            wash(1) #definir 4
            leds('enxague')
            enxague()
            leds('centrifugation')
            centrifugation()
            shutdown()
        if program == 2:
            leds('wash')
            log('LAVAGEM MODERADA')
            waterLevel(level)
            log(f'NIVEL DE ÁGUA ATINGIDO')
            wash(1) #definir 8
            leds('enxague')
            enxague()
            leds('centrifugation')
            centrifugation()
            shutdown()
        if program == 3:
            leds('wash')
            log('LAVAGEM PESADA')
            waterLevel(level)
            log(f'NIVEL DE ÁGUA ATINGIDO')
            wash(1) #definir 12
            leds('enxague')
            enxague()
            leds('centrifugation')
            centrifugation()
            shutdown()
    elif program == 4:
        leds('enxague')
        log('ENXAGUE')
        enxague()
        leds('centrifugation')
        centrifugation()
        shutdown()
    elif program == 5:
        log('CENTRIFUGAÇÃO')
        leds('centrifugation')
        centrifugation()
        shutdown()

def wash(cycles):
    level, program = setPrograms()
    for i in range(cycles):   
        for x in range(cycles+cycles):
            for c in range(5):
                engine_left.value(1)
                if btn_turbo.value() == 1:
                    seconds = 0.4
                else:
                    seconds = 0.7
                sleep(seconds)
                engine_left.value(0)
                sleep(0.05)
                engine_right.value(1)
                sleep(seconds)
                engine_right.value(0)
                log(f'CICLO: {c+1}')
            #VERIFICAR BOTAO POWER SE E TRUE
                programChanged(level, program)
            log('PAUSA MOLHO')
            sleep(10) #definir 30s

def waterLevel(level=2):
    
    def fill(pressurevalue, top):
        solenoid.value(1)
        while pressurevalue < top:
            sleep(0.5)
            pressurevalue = pressure.read_u16()
            log(f'ENCHENDO => {pressurevalue}')
        solenoid.value(0)
        
                
    def clear(pressurevalue, top):
            if pressurevalue - top > 2000:
                bomb_water.value(1)
                while pressurevalue > top:
                    sleep(0.5)
                    pressurevalue = pressure.read_u16()
                    log(f'DESCARTANDO ÁGUA | PRESSURE => {pressurevalue}')
                bomb_water.value(0)
    #LEVEL 1 WATER 16328
    if level == 1:
        pressurevalue = pressure.read_u16()
        
        if pressurevalue < 16328:
            fill(pressurevalue, 16328)
        elif pressurevalue > 16328:
            clear(pressurevalue, 16328)
    #LEVEL 2 WATER 32768
    elif level == 2:
        pressurevalue = pressure.read_u16()
        if pressurevalue < 32768:
            fill(pressurevalue, 32768)
        elif pressurevalue > 32768:
            clear(pressurevalue, 32768)
    #LEVEL 3 WATER 49151
    elif level == 3:
        pressurevalue = pressure.read_u16()
        if pressurevalue < 49151:
            fill(pressurevalue, 49151)
        elif pressurevalue > 49151:
            clear(pressurevalue, 49151)
    #LEVEL 4 WATER 65535
    elif level == 4:
        pressurevalue = pressure.read_u16()
        
        if pressurevalue < 65535:
            fill(pressure, 65535)
        elif pressurevalue > 65535:
            clear(pressurevalue, 16328)
    

def setPrograms():

    if pt_program.read_u16() > 0 and pt_program.read_u16() <= 13107:
        program = 1
    elif pt_program.read_u16() > 13107 and pt_program.read_u16() <= 26214:
        program = 2
    elif pt_program.read_u16() > 26214 and pt_program.read_u16() <= 39321:
        program = 3
    elif pt_program.read_u16() > 39231 and pt_program.read_u16() <= 52428:
        program = 4
    elif pt_program.read_u16() > 52428 and pt_program.read_u16() <= 65535:
        program = 5
    else:
        program = 2

    if pt_level.read_u16() > 0 and pt_level.read_u16() <= 16384:
        level = 1
    elif pt_level.read_u16() > 16384 and pt_level.read_u16() <= 32768:
        level = 2
    elif pt_level.read_u16() > 32768 and pt_level.read_u16() <= 49151:
        level = 3
    elif pt_level.read_u16() > 49151 and pt_level.read_u16() <= 65535:
        level = 4
    else:
        level = 2

    return level, program  

def enxague():
    bomb_water.value(1)
    while pressure.read_u16() > 0:
        log('DESCARTANDO ÁGUA')
        sleep(.2)
    log('INICIANDO MINI CENTRIFUGAÇÃO DO ENXAGUE')
    sleep(1) #definir 60 segundos
    for e in range(4):
        engine_right.value(1)
        sleep(5)
        engine_right.value(0)
        sleep(5)
    log('CENTRIFUGAÇÃO DE 2 MINUTOS')
    engine_right.value(1)
    sleep(120)
    bomb_water.value(0)
    level, program  = setPrograms()
    waterLevel(level)
    log(f'NIVEL DE AGUA ATINGIDO')
    for i in range(2):   
        for x in range(4):
            for c in range(5):
                print(c)
                engine_left.value(1)
                if btn_turbo.value() == 1:
                    seconds = 0.4
                else:
                    seconds = 0.7
                sleep(seconds)
                engine_left.value(0)
                sleep(0.05)
                engine_right.value(1)
                sleep(seconds)
                engine_right.value(0)
                waterLevel()
            #VERIFICAR BOTAO POWER SE E TRUE
            log('PAUSA MOLHO')
            sleep(10)
    
def centrifugation():
    leds('centrifugation')
    log('MODO CENTRIFUGAÇÃO')
    bomb_water.value(1)
    log('BOMBA DE VACUO LIGADA')
    while pressure.read_u16() > 0:
        sleep(1) #definir 5 em produção
        log(f'CENTRIFUGAÇÃO => SENSOR DE PRESSÃO {pressure.read_u16()}')
    for i in range(5):
        engine_right.value(1)
        sleep(5)
        engine_right.value(0)
        sleep(5)
    for i in range(4):
        engine_right.value(1)
        sleep(60)
        engine_right.value(0)
        sleep(30)
    engine_right.value(1)
    sleep(120)
    engine_right.value(0)
    
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
    leds()
    buzzer.value(1)
    sleep(.25)
    buzzer.value(0)
    sleep(.25)
    buzzer.value(1)
    sleep(.25)
    buzzer.value(0)
    sleep(.25)
    buzzer.value(1)
    sleep(1)
    buzzer.value(0)
    while btn_power.value() == 0:
        ledpower_green.value(1)
        sleep(.25)
        ledpower_green.value(0)
        sleep(.25)
        log('ESPERANDO DESLIGAR BOTAO')
    ledpower_green.value(0)
    sleep(1)
    standby()

def programChanged(level, program):
    levelbefore, programbefore = level , program
    level_now , program_now = setPrograms()
    if programbefore != program_now:
        programbefore = program_now
        log('FUNÇÃO ALTERADA, REPROGRAMANDO.')
        changePrograms()
        shutdown()
    if levelbefore != level_now:
        levelbefore = level_now
        log('NIVEL DE AGUA ALTERADO, AJUSTANDO.')
        waterLevel()
        log(f'NIVEL DE ÁGUA ATINGIDO')

def log(msg):
    times = localtime(time())
    timenow = f"{times[2]}/{times[1]}/{times[0]} as {times[3]}:{times[4]}:{times[5]} => "
    msg = timenow +msg
    with open('/log.txt', 'a') as f:
        f.write(msg + '\n')
    print(msg) # opcional: também exibir o log no console


    
log('============================================================================')           
standby()


