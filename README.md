# TestadorDS18B20

Identifica se um sensor de temperatura "DS18B20" é original.

Tests if a "DS18B20" temperature sensor is original.

## Sobre / About

Este projeto foi inspirado pela biblioteca CheckDS18B20 de Koen DV.  O meu código foi escrito diretamente a partir das informações acumuladas por Chris Petrich em https://github.com/cpetrich/counterfeit_DS18B20. No meu projeto, optei por não enviar ao sensor comandos não documentados.

This project was inspired by the CheckDS18B20 library, written by Koen DV. My code was written directly from the information gathered by Chris Petrich at https://github.com/cpetrich/counterfeit_DS18B20.  In my project, I opted for not sending undocumented commands to the sensor.

## Uso / Use

Coloque o sensor a ser testado no conector (tomando cuidado com a orientação) e aperte o botão. Um LED acende enquanto o sensor está alimentado e sendo testado. Ao final dos testes, o resultado é apresentado no display e uma LED verde ou vermelho acende para indicar se o sensor é original ou uma cópia. Um segundo aperto do botão limpa o resultado e volta à condição inicial.

Consulte https://github.com/cpetrich/counterfeit_DS18B20 para interpretar o resultado do teste. De forma resumida:

A1: Legítimo
A2: Clone com desempenho ruim
B1:GXCAS 18B20 - clone com bugs menores
B2: 7Q-Tek QT18B20 - clone com bugs menores
C: Clone com problemas sérios
D1: Clone com problemas sérios
D2: XSEC SE18B20 - clone com problemas sérios
E: NOVOSENSE NS18B20 - clone com bom desempenho

Put the sensor to test in the connector (paying attention to the pinout) and press the button. A LED lights up while the sensor is powered up and tested. At the end of the tests, a report is shown in the display and a LED green or red lights to signal a original sensor or a copy. A second press of the button clears the report and returns to the initial condition.

To interpret the result, see https://github.com/cpetrich/counterfeit_DS18B20. TL/DR:

A1: Authentic
A2: Clone with bad performance
B1:GXCAS 18B20 - clone with minor bugs
B2: 7Q-Tek QT18B20 - clone with minor bugs
C: Clone with serious problems
D1: Clone with serious problems
D2: XSEC SE18B20 - clone with serious problems
E: NOVOSENSE NS18B20 - clone with good performance


## Hardware

Eu decidi montar o meu testador em uma latinha de bala (Altoids); para ficar pequeno eu usei uma [placa RP2040 Zero da Waveshare ](https://www.waveshare.com/rp2040-zero.htm). Esta placa inclui um LED RGB WS2812 que é usada para mostrar o resultado. Eu também usei um botão que possui um LED interno, este LED é usado para indicar quando o sensor está alimentado.

Eu inclui neste repositório uma versão usando componentes mais comuns: uma Raspberry Pi Pico e um LED RGB de catodo comum (vermelho e verde para o resultado e azul para indicar a alimentação do sensor).

As duas versões usam um display OLED I2C gráfico monocromático com 128x64 pontos, com controlador SSD1306.

Não deve ser difícil adaptar o software para outras placas que suportadas pelo MicroPython e outros displays.

I decided to mount my assembly in a Altoids can; to keep it small I used a [Waveshare RP2040 Zero board](https://www.waveshare.com/rp2040-zero.htm). This board includes a WS2812 RGB LED that is used to signal the good/bad result. I also used a pushbutton with a built-in LED, this LED is used to signal when the sensor is powered.

I included in this repository a version using more common parts: a Raspberry Pi Pico, a plain pushbutton and a common-cathode RGB LED (red and green for the result, blue for powered).

Both versions use a monochrome OLED I2C 128x64 dot display with an SSD1306 controller.

It should not be too hard to adapt the software for other boards that support MicroPython and other displays.


## Software

O software foi escrito em MicroPython. As bibliotes usadas são onewire, neopixel and ssd1306. As primeiras duas estão incluídas no port do MicroPython para o RP2040, a biblioteca ssd1306 library pode ser baixada de https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/display/ssd1306.

Mude o bloco "Conexoes" conforme a sua montagem.

Salve o programa na placa com o nome "main.py" para ele ser executado automaticamente quando a placa for alimentada.
 
The software is written in MicroPython. The libraries used are onewire, neopixel and ssd1306. The first two are included in the RP2040 port MicroPython, ssd1306 library can be download from https://github.com/micropython/micropython-lib/tree/master/micropython/drivers/display/ssd1306.

Change the block "Conexoes" to reflect your hardware connections.

Save the program on the board as "main.py" to have it run when power is applied.


## Agradecimentos / Thanks

Agradecimento especial a Chris Petrich pelo trabalho de pesquisa e pela excelente documentação dos resultados.

A special thank you to Chris Petrich for his research and for the excellent documentation of the results.


## Aviso / Disclaimer

*Este projeto se baseia nos resultados empíricos observados por Chris Petrich. Nenhuma garantia, implícita ou explícita, é dada.*

*This project is based on empirical results observed by Chris Petrich. No guarantees given or implied.* 
