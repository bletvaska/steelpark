# Remote for VLC over MQTT and Telnet

## Install

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install -r requirements.txt
```


## Configuration

V priecinku `tv.remote/`, kde sa nachadza skript `run.bash`, treba vytvorit `.env` subor. Zacat staci so sablonou:

```bash
$ cp template.env .env
```


## Run

Spusta sa skriptom `run.bash`. Treba ho pridat do skriptu `~/.config/labwc/autostart`:

```bash
/usr/bin/lwrespawn "${HOME}/steelpark/iot.corner/tv.remote/run.bash" &
```

