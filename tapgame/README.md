# The Game Controller

## Building

```bash
$ export TAPGAME_VERSION=2025.1.5
$ docker buildx build \
    --platform linux/arm/v7 \
    --tag "bletvaska/gaussgame-core:${TAPGAME_VERSION}" \
    --tag "bletvaska/gaussgame-core:latest" \
    --file Dockerfile.arm32v7 \
    --push \
    --build-arg "VERSION=${TAPGAME_VERSION}" \
    .
```



# SPSE Presov

## Vianocny vianocny stromcek

* ESP32 ma zapojene piny 19 a GND (hned vedla)
    * 19 je datovy - pripojit na zeleny
    * GND je zem - pripojit na biely
* kod je napisany v micropython-e
    * je potrebne pripojit sa k mikrokontroleru a nastavit wifi
    * subor `config.py`
* rozprestriet QR kod


## Textovka

* pustit terminal a dostat sa do priecinku `~/Downloads/python-textovka/adventure/`
* spustit cez

    ```bash
    $ python main.py
    ```
* sutaz - ak sa dostanes z lietadla, dostanes nalepky z namakaneho dna


## Video/ prezentacia do pozadia


## Alien Breed

* na ploche je AlienBreed intro - staci na neho len kliknut