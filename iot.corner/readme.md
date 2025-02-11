# The IoT Corner Project

Projekt pre Borisa a hlavne pre Kulturpark.


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
