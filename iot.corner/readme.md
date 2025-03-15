# The IoT Corner Project



## Pristup na RPi

ssh maker:kulturpark@ip

## Spustenie

```bash
$ docker compose up --detach
```


## Build & Devel

```bash
$ docker compose build && docker compose up && docker compose down
```

## Baliky na RPi

```
$ sudo apt install btop vim
```

```
$ curl -sSL https://get.docker.com/ | sh
```


## How it works

Je to trojkompozicia:

* mosquitto
* zigbee2mqtt
* nginx + vlastna appka

Na stranke je niekolko elementov, ktore patria do skupiny `socket` a maju jedinecne identifikatory `socket-X`, kde `X` je ciselny identifikator zasuvky. Pridat dalsie zariadenie znamena pridat dalsi element do HTML kodu, pomocou CSS ho spravne umiestnit a pridat ho so zodpovedajucim nazvom (`socket-X`) do Zigbee2MQTT.

Kedze je ale nasadenie cez externy web a externe mqtt, tym padom sa spusta len Zigbee2MQTT.



## Spustenie prehravaca

vytvorit skript na prehravanie v `~/runner.bash`:

```bash
#!/usr/bin/env bash

killall -9 lwrespawn
killall -9 pcmanfm
killall -9 wf-panel-pi

cvlc "${HOME}/Videos/"* \
    --fullscreen \
    --loop \
    --no-osd \
    --no-audio \
    --no-mouse-events
```

vytovrit autostart subor  `~/.config/autostart/vlc.desktop`:

```desktop
[Desktop Entry]
Type=Application
Name=Video Player
Exec=/home/maker/runner.bash
X-GNOME-Autostart-enabled=true
```


## Zariadenia na MQTT

* blind - https://www.zigbee2mqtt.io/devices/E2102.html#ikea-e2102
* repeater - https://www.zigbee2mqtt.io/devices/E1746.html#ikea-e1746
* light-1 - https://www.zigbee2mqtt.io/devices/LED1836G9.html#ikea-led1836g9
* remote - https://www.zigbee2mqtt.io/devices/ZS06.html#tuya-zs06
* socket-X - https://www.zigbee2mqtt.io/devices/E2204.html#ikea-e2204


zapnutie wifi na rpi:

```bash
$ nmcli connection up hello-world
```
