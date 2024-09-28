
 Micropython Weather and Motion Detection System

Este projeto é uma demonstração de um sistema de monitoramento de condições climáticas e detecção de movimento, utilizando sensores conectados a um ESP32 e comunicando dados através de um broker MQTT. Ele integra um sensor DHT22 para medir temperatura e umidade, um sensor PIR para detecção de movimento, e publica as informações em um servidor MQTT. Um buzzer também é acionado quando a temperatura excede um determinado limite.

Funcionalidades

- **Medição de Temperatura e Umidade**: O sensor DHT22 coleta dados de temperatura e umidade.
- **Detecção de Movimento**: O sensor PIR detecta movimento e notifica o servidor MQTT.
- **Publicação via MQTT**: Os dados são publicados em um tópico MQTT (`smart-city`).
- **Alerta Sonoro**: Um buzzer é ativado quando a temperatura excede 25°C.

 Hardware Utilizado

- **ESP32**: Microcontrolador que conecta os sensores e o servidor MQTT.
- **DHT22**: Sensor de temperatura e umidade.
- **PIR Sensor**: Sensor de infravermelho para detectar movimento.
- **Buzzer**: Emite som quando a temperatura excede 25°C.
- **LED**: Indicador de status (conectado no pino 4).

 Conexões do Hardware

| Componente | Pino ESP32 |
|------------|------------|
| DHT22      | GPIO 15    |
| PIR        | GPIO 14    |
| Buzzer     | GPIO 2     |
| LED        | GPIO 4     |

 Configurações do MQTT

- **Broker**: `broker.mqttdashboard.com`
- **Tópico**: `smart-city`
- **ID do Cliente**: `micropython-weather-demo`

## Configuração do Wi-Fi

O código se conecta a uma rede Wi-Fi aberta chamada `Wokwi-GUEST`. Para usar uma rede diferente, ajuste os parâmetros na linha:

```python
sta_if.connect('Wokwi-GUEST', '')
```

## Instalação e Execução

### 1. Preparar o Ambiente

Você precisa configurar um ambiente de desenvolvimento MicroPython no ESP32. Siga estes passos:

- Instale o firmware MicroPython no seu ESP32.
- Use uma IDE compatível, como o [Thonny](https://thonny.org/), para carregar o código.

### 2. Carregar o Código

1. Copie o código para o seu ambiente de desenvolvimento.
2. Faça upload do código para o ESP32.
3. O ESP32 se conectará à rede Wi-Fi e começará a medir as condições climáticas e detectar movimento.

### 3. Testar via WebSocket

Você pode verificar os dados publicados no MQTT usando o cliente WebSocket MQTT no seguinte link:

- [MQTT WebSocket Client](http://www.hivemq.com/demos/websocket-client/)

Insira o broker `broker.mqttdashboard.com` e o tópico `smart-city` para visualizar as mensagens publicadas pelo ESP32.

### Simulação no Wokwi

Se você deseja simular o projeto antes de usar hardware físico, pode testar no [Wokwi](https://wokwi.com/arduino/projects/322577683855704658).

## Código

O código principal está abaixo:

```python
import network
import time
from machine import Pin
import dht
import ujson
from umqtt.simple import MQTTClient

# MQTT Server Parameters
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER    = "broker.mqttdashboard.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "smart-city"

sensor = dht.DHT22(Pin(15))
led_pin = Pin(4, Pin.OUT)
pir_pin = Pin(14, Pin.IN, Pin.PULL_UP)
buzzer_pin = Pin(2, Pin.OUT)

def play_buzzer(duration):
    buzzer_pin.on()
    time.sleep(duration)
    buzzer_pin.off()

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()

print("Connected!")

prev_weather = ""
prev_motion = 0
while True:
    print("Measuring weather conditions... ", end="")
    sensor.measure()
    message = ujson.dumps({
        "temp": sensor.temperature(),
        "humidity": sensor.humidity(),
    })
    if message != prev_weather:
        print("Weather updated!")
        print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, message))
        client.publish(MQTT_TOPIC, message)
        prev_weather = message
        
        temperature = sensor.temperature()
        if temperature > 25:
            play_buzzer(0.5)  # Toca o buzzer por 500 ms
        else:
            buzzer_pin.off()
        
    else:
        print("No change in weather")
    
    motion = pir_pin.value()
    if motion != prev_motion:
        print("Motion detected: {}".format(motion))
        print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, motion))
        client.publish(MQTT_TOPIC, str(motion))
        prev_motion = motion
    
    time.sleep(1)
```

## Referências

- [MQTT WebSocket Client](http://www.hivemq.com/demos/websocket-client/)
- [Wokwi Simulator](https://wokwi.com/arduino/projects/322577683855704658)

