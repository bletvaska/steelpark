# The Game Controller

## Issue

* problem pri baleni obrazu pre ovladanie a pristup ku GPIO pinom
* toto funguje ako tak: https://github.com/gpiozero/gpiozero/discussions/1117


## Development

### Priprava prostredia

konfiguracny subor pre projekt je `pyproject.toml`, ktory vie byt konfiguraciou aj pre `poetry` aj pre `uv`. aktualne pouzivam `uv`

postup na vytvorenie devel prostredia moze vyzerat nasledovne:

```bash
# najprv vytvorime .venv/ priecinok
$ uv venv

# prostredie aktivujeme
$ source .venv/bin/activate

# nainstalujeme vsetky zavislosti
$ uv sync
```


### Samotny vyvoj





## Building Package

distribucne balicky sa vytvoria pomocou nasledovnych prikazov v priecinku `dist/`:

```bash
$ uv build
$ poetry build
```


## Building Docker Image

```bash
$ export GAUSSGAME_VERSION=2025.7.1
$ docker buildx build \
    --platform linux/arm/v7 \
    --tag "bletvaska/gaussgame-core:latest" \
    --tag "bletvaska/gaussgame-core:2025" \
    --tag "bletvaska/gaussgame-core:2025.7" \
    --tag "bletvaska/gaussgame-core:${GAUSSGAME_VERSION}" \
    --file Dockerfile.arm32v7 \
    --push \
    --build-arg "VERSION=${GAUSSGAME_VERSION}" \
    .
$ docker image tag bletvaska/gaussgame-core:${GAUSSGAME_VERSION} bletvaska/gaussgame-core:2025 
$ docker image tag bletvaska/gaussgame-core:${GAUSSGAME_VERSION} bletvaska/gaussgame-core:2025.7
```




## Testing with MQTT

subscribe for all events

```bash
$ mosquitto_sub -h localhost -t steelpark/gauss/# -F "%t: %p"
```

send tap event

```bash
$ mosquitto_pub -h localhost -t steelpark/gauss/keyboard/event -m '{"name": "tap"}'
```

periodically send taps:

```bash
export MQTT_URI="mqtt://localhost:1883/steelpark/gauss/keyboard/event"

while true; do 
    # rules
    for _ in 1 2 3; do
        mosquitto_pub -L $MQTT_URI -m '{"name": "tap"}'
        sleep 1
    done

    # delay
    sleep 4

    # game
    for _ in {1..60}; do
        mosquitto_pub -L $MQTT_URI -m '{"name": "tap"}'
        sleep 1
    done

    # delay
    sleep 10
done
```

change screen

```bash
$ mosquitto_pub -h localhost -t steelpark/gauss/screen -m '{"name": "START"}'
$ mosquitto_pub -h localhost -t steelpark/gauss/screen -m '{
    "name": "RESULTS", 
    "player": {"dt": "2025-06-17T16:41:21Z", "id": 1209, "score": 74, "name": "Srandovná Slaninka", "rank": 990}, 
    "table": [
        {"id": 578, "name": "Chichotavý Klokaník", "score": 211}, {"id": 566, "name": "Hopsavý Myšiak", "score": 199}, {"id": 572, "name": "Bublinková Myška", "score": 196}, {"id": 791, "name": "Srandovná Veverička", "score": 194}, {"id": 795, "name": "Bystrý Krtko", "score": 192}, {"id": 1137, "name": "Skákajúci Oceánik", "score": 192}, {"id": 793, "name": "Prskajúca Medvedica", "score": 189}, {"id": 965, "name": "Hopsavý Tuleň", "score": 188}, {"id": 567, "name": "Hopsavý Veveričiak", "score": 187}, {"id": 576, "name": "Hopsavá Konvalinka", "score": 186}, {"id": 606, "name": "Srandovný Slimáčik", "score": 186}, {"id": 740, "name": "Lenivá Konvalinka", "score": 186}
    ], 
    "chart": {
        "labels": ["9 - 31", "32 - 53", "54 - 76", "77 - 98", "99 - 121", "122 - 143", "144 - 166", "167 - 188", "189 - 211"], 
        "data": [22, 65, 146, 140, 197, 291, 253, 83, 6], 
        "gauss": [],
        "playerScoreBin": 2
    }    
}'
```

list of screens

* `START` - 
* `GAUSS` -
* `RULES-1` - 
* `RULES-2` - 
* `RULES-3` - 
* `GET_READY` -
* `PLAY` -
* `GAME_OVER` -
* `RESULTS` -


zobrazenie vysledkov


```bash
$ mosquitto_pub -h localhost -t kulturpark/gauss/screen -m '{
    "name": "RESULTS", 
    "player": {"dt": "2025-06-17T16:41:21Z", "id": 1209, "score": 74, "name": "Srandovná Slaninka", "rank": 990}, 
    "table": [
        {"id": 578, "name": "Chichotavý Klokaník", "score": 211}, 
        {"id": 566, "name": "Hopsavý Myšiak", "score": 199}, 
        {"id": 572, "name": "Bublinková Myška", "score": 196}, 
        {"id": 791, "name": "Srandovná Veverička", "score": 194}, 
        {"id": 795, "name": "Bystrý Krtko", "score": 192}, 
        {"id": 1137, "name": "Skákajúci Oceánik", "score": 192}, 
        {"id": 793, "name": "Prskajúca Medvedica", "score": 189}, 
        {"id": 965, "name": "Hopsavý Tuleň", "score": 188}, 
        {"id": 567, "name": "Hopsavý Veveričiak", "score": 187}, 
        {"id": 576, "name": "Hopsavá Konvalinka", "score": 186}, 
        {"id": 606, "name": "Srandovný Slimáčik", "score": 186}, 
        {"id": 740, "name": "Lenivá Konvalinka", "score": 186}
    ], 
    "chart": {
        "labels": [
            "1 - 23",
            "24 - 46",
            "47 - 70",
            "71 - 93",
            "94 - 116",
            "117 - 139",
            "140 - 163",
            "164 - 186",
            "187 - 209",
            "210 - 233"
        ],
        "data": [
            12,
            36,
            59,
            82,
            106,
            129,
            152,
            175,
            199,
            222
        ],
        "playerScoreBin": 4
    },
    "gauss": {
        "x", [],
        "y", []
    }    
}'









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
