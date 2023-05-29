from machine import Pin, I2C
from time import sleep, ticks_ms
import onewire
import ssd1306
import neopixel

# Conexoes (minha montagem)
PWR_DS18B20 = Pin(26, Pin.OUT)
DQ_DS18B20 = Pin(27)
BOTAO_SW = Pin(15, Pin.IN, Pin.PULL_UP)
LED_PWR = Pin(14, Pin.OUT)
LED_WS2812 = Pin(16)
DISPLAY_I2C = 1
DISPLAY_SDA = Pin(6)
DISPLAY_SCL = Pin(7)

# Conexoes (montagem com Pi Pico)
#PWR_DS18B20 = Pin(26, Pin.OUT)
#DQ_DS18B20 = Pin(27)
#BOTAO_SW = Pin(16, Pin.IN, Pin.PULL_UP)
#LED_WS2812 = None
#LED_PWR = Pin(13, Pin.OUT) # Blue
#LED_OK = Pin(14, Pin.OUT)  # Green
#LED_BAD = Pin(15, Pin.OUT) # Red
#DISPLAY_I2C = 1
#DISPLAY_SDA = Pin(6)
#DISPLAY_SCL = Pin(7)

# Comandos DS18B20
CMD_READSPAD = 0xBE
CMD_WRITESPAD = 0x4E
CMD_CONVERT_T = 0x44
CMD_RECALL_E2 = 0xB8

# Display no endereco padrao 0x3C
i2c = I2C(DISPLAY_I2C, sda=DISPLAY_SDA, scl=DISPLAY_SCL)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# init RGB LED
if LED_WS2812 is None:
    ledRGB = None
    LED_PWR.off()
    LED_OK.off()
    LEC_BAD.off()
else:
    ledRGB = neopixel.NeoPixel(LED_WS2812, 1)
    ledRGB[0] = (0, 0, 0)
    ledRGB.write()

familia = ''

# Read scratchpad
def readspad(addr):
    ow.reset()
    ow.select_rom(sensor)
    ow.writebyte(CMD_READSPAD)
    spad = bytearray(9)
    for i in range(9):
        spad[i] = ow.readbyte()
    return spad

# Teste 1 - Endereço
def teste1(addr):
    print('Endereco: '+' '.join(hex(i)[2:4] for i in sensor))
    if sensor[0] != 0x28:
        print ('Nao parece ser DS18B20!')
    if (sensor[5] != 0) or (sensor[6] != 0):
        print('Endereco suspeito!')
        return True
    return False

# Teste 2 - Valor inicial do scratchpad
#  50/05/xx/xx/7F/FF/xx/10/xx
def teste2(spad):
    erro = False
    print('Scratchpad: '+' '.join(hex(i)[2:4] for i in spad))
    if (spad[0] != 0x50) or (spad[1] != 0x05):
        print ('Temperatura inicial incorreta')
        erro = True
    if spad[4] != 0x7F:
        print ('Configuracao diferente da default')
    if (spad[5] != 0xFF) or (spad[7] != 0x10):
        print ('Valores incorretos nos regs reservados')
        erro = True
    return erro

# Teste 3 - Mudanca da resolucao p/ 9 bits
def teste3(addr):
    erro = False
    ow.reset()
    ow.select_rom(addr)
    ow.writebyte(CMD_WRITESPAD)
    ow.writebyte(0xAA)
    ow.writebyte(0x55)
    ow.writebyte(0x00)
    spad = readspad(addr)
    if spad[4] != 0x1F:
        if spad[4] == 0x7F:
            print ('Resolucao fixa em 12 bits?')
        else:
            print ('Configuracao incorreta')
        erro = True
    if (spad[2] != 0xAA) or (spad[3] != 0x55):
        print ('Nao gravou user bytes')
    ow.reset()
    ow.select_rom(addr)
    ow.writebyte(CMD_RECALL_E2)  # restaura config
    sleep(0.1)
    return spad

# Teste 4 - Tempo de conversao
def teste4(addr):
    ow.reset()
    ow.select_rom(addr)
    ow.writebyte(CMD_CONVERT_T)
    inicio = ticks_ms()
    while ow.readbit() == 0:
        pass
    fim = ticks_ms()
    return fim - inicio

# Tenta identificar chip falso pelo endereco
def idchip1(addr):
    global familia
    if addr[0] == 0x28:
        if (addr[1] == 0xFF) and (addr[2] == 0x64):
            familia = 'C'
        elif (addr[1] == 0x61) and (addr[2] == 0x64):
            familia = 'C'
        elif (addr[1] == 0x00) and (addr[4] == 0x59) and (addr[5] == 0x43):
            familia = 'E'

# Tenta identificar chip falso pelo valor do scratchpad
def idchip2(spad):
    global familia
    if (spad[7] == 0x66) and (spad[6] != 0x0C) and (spad[5] != 0xFF):
        familia = 'D2:XSEC SE18B20'

# Tenta identificar chip pelo comportamento da gravacao
def idchip3(spaddef, spadgrv, addr):
    global familia
    if spaddef[6] != spadgrv[6]:
        print('Configuracao mudou byte reservado')
        if (spaddef[6] == 0x0C) and (spadgrv[6] == 0x00):
            if addr[1] == 0xAA:
                familia = 'B1:GXCAS 18B20'
            elif addr[1] == 0xFF:
                familia = 'B2:7QTek QT18B20'
            else:
                familia = 'B1:UMW 18B20'

# Tenta identificar chip pelo tempo de leitura
def idchip4(tconv):
    global familia
    print ('Conversao em {} ms'.format(tconv))
    if tconv < 20:
        familia = 'D1'
        return True
    elif tconv < 50:
        familia = 'C'
        return True
    elif (familia == '') and (tconv > 300) and (tconv < 550):
        familia = 'A2'
    return False

ow = onewire.OneWire(DQ_DS18B20)

while True:
    display.fill(0)
    display.text('TESTE DS18B20', 0, 0, 1)
    display.text('Aperte o botao', 0, 56, 1)
    display.show()
    while BOTAO_SW.value() == 1:
        sleep(0.1)
    while BOTAO_SW.value() == 0:
        sleep(0.1)
    display.fill(0)
    display.text('TESTANDO', 0, 0, 1)
    display.show()

    if not ledRGB is None:
        ledRGB[0] = (32, 16, 0)
        ledRGB.write()
    LED_PWR.on()
    PWR_DS18B20.on()
    sleep(0.1)
    sensors = ow.scan()
    PWR_DS18B20.off()
    LED_PWR.off()
    if not ledRGB is None:
        ledRGB[0] = (0, 0, 0)
        ledRGB.write()
    if len(sensors) == 0:
        display.text("Sem sensor!", 0, 16, 1)
        display.show()
        while BOTAO_SW.value() == 1:
            sleep(0.1)
        while BOTAO_SW.value() == 0:
            sleep(0.1)
    else:
        LED_PWR.on()
        PWR_DS18B20.on()
        sensor = sensors[0]
        if not ledRGB is None:
            ledRGB[0] = (64, 32, 0)
            ledRGB.write()
        legitimo = True
        addr=''
        for x in sensor:
            addr = addr+'{:02X}'.format(x)
        display.text(addr, 0, 16, 1)
        display.show()
        if teste1(sensor):
            if ledRGB is None:
                LED_BAD.on()
            else:
                ledRGB[0] = (64, 0, 0)
                ledRGB.write()
            display.text('***SUSPEITO***', 0, 24, 1)
            display.show()
            legitimo = False
            idchip1(sensor)
        print()
        spad = readspad(sensor)
        if teste2(spad):
            legitimo = False
            idchip2(spad)
        print()
        spad2 = teste3(sensor)
        if idchip3(spad, spad2, sensor):
            legitimo = False
        tconv = teste4(sensor)
        if idchip4(tconv):
            legitimo = False
        print()
        if legitimo and (tconv > 550) and (tconv < 750):
            if ledRGB is None:
                LED_OK.on()
            else:
                ledRGB[0] = (0, 64, 0)
                ledRGB.write()
            display.text('Parece legitimo', 0, 32, 1)
            display.show()
            print('Parece legitimo')
            familia = 'A1:Maxim DS18B20'
        print ('Familia: ' + familia)
        display.text(familia, 0, 40, 1)
        display.text('Aperte o botao', 0, 56, 1)
        display.show()
        PWR_DS18B20.off()
        LED_PWR.off()
        while BOTAO_SW.value() == 1:
            sleep(0.1)
        while BOTAO_SW.value() == 0:
            sleep(0.1)
        if ledRGB is None:
            LED_OK.off()
            LED_BAD.off()
        else:
            ledRGB[0] = (0, 0, 0)
            ledRGB.write()
