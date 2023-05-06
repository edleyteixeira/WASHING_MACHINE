from machine  import ADC, Pin
from utime import sleep

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

#RELays
buzzer = Pin(0, Pin.OUT)
engine_left = Pin(21, Pin.OUT)
engine_right = Pin(20, Pin.OUT)
bomb_water = Pin(19, Pin.OUT)
solenoid = Pin(18, Pin.OUT)




def standby():
    ledpower_red.value(1)
    while btn_power.value() == 0:
        sleep(0.1)
        print(pressure.read_u16())
    ledpower_red.value(0)
    ledpower_green.value(1)
    changePrograms()

def changePrograms():
    
    level, program = setPrograms()

    if program >= 1 and program <= 3:
        if program == 1:
            print('LAVAGEM LEVE')
            waterLevel()
            wash(4)
        if program == 2:
            print('LAVAGEM MODERADA')
            waterLevel(level)
            wash(8)
        if program == 3:
            print('LAVAGEM PESADA')
            waterLevel(level)
            wash(12)
    elif program == 4:
        enxague()
    elif program ==5:
        print('MODO CENTRIFUGAÇÃO')

def wash(cycles):
    leds('wash')
    for i in range(cycles):   
        for x in range(cycles+cycles):
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
            #VERIFICAR BOTAO POWER SE E TRUE
            waterLevel()
            print('PAUSA MOLHO')
            sleep(10)

def waterLevel(level=2):

    pressurevalue = pressure.read_u16()
    
    #LEVEL 1 WATER
    if level == 1:
        if pressurevalue < 16384:
            print('ENCHENDO PARA LEVEL 1')
            solenoid.value(1)
            while pressurevalue < 16384:
                sleep(0.5)
                pressurevalue = pressure.read_u16()
                print(pressurevalue)
            solenoid.value(0)
        elif pressurevalue > 16384:
            if pressurevalue - 16384 > 2000:
                bomb_water.value(1)
                while pressurevalue > 16384:
                    print('ESVAZIANDO PARA LEVEL 1')
                    sleep(0.5)
                    pressurevalue = pressure.read_u16()
                    print(pressurevalue)
                bomb_water.value(0)
    #LEVEL 2 WATER
    elif level == 2:
        if pressurevalue < 32768:
            print('ENCHENDO PARA LEVEL 2')
            solenoid.value(1)
            while pressurevalue < 32768:
                sleep(0.5)
                pressurevalue = pressure.read_u16()
                print(pressurevalue)
            solenoid.value(0)
        elif pressurevalue > 32768:
            if pressurevalue - 32768 > 2000:
                bomb_water.value(1)
                print('ESVAZIANDO PARA LEVEL 2')
                while pressurevalue > 32768:
                    sleep(0.5)
                    pressurevalue = pressure.read_u16()
                    print(pressurevalue)
                bomb_water.value(0)
    #LEVEL 3 WATER
    elif level == 3:
        if pressurevalue < 49151:
            print('ENCHENDO PARA LEVEL ')
            solenoid.value(1)
            while pressurevalue < 49151:
                sleep(0.5)
                pressurevalue = pressure.read_u16()
                print(pressurevalue)
            solenoid.value(0)
        elif pressurevalue > 49151:
            if pressurevalue - 49151 > 2000:
                bomb_water.value(1)
                while pressurevalue > 49151:
                    print('ESVAZIANDO PARA LEVEL 3')
                    sleep(0.5)
                    pressurevalue = pressure.read_u16()
                bomb_water.value(0)
    elif level == 4:
        if pressurevalue < 65535:
            print('ENCHENDO PARA LEVEL 4')
            solenoid.value(1)
            while pressurevalue < 65535:
                sleep(0.5)
                pressurevalue = pressure.read_u16()
                print(pressurevalue)
            solenoid.value(0)

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
    while True:
        print('ENXAGUANDO')
        sleep(0.5)

def centrifugation():
    pass

def leds(power):
    led_wash.value(0)
    led_enxague.value(0)
    led_centrifugation.value(0)
    if power == 'wash':
        led_wash.value(1)
    if power == 'enxague':
        led_enxague.value(1)
    if power == 'centrifugation':
        led_centrifugation.value(1)
standby()


