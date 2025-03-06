# Raspberry Pi 3 Kiosk


## System Setup

1. Nainštalovať [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/)

   * pouzit zakladny obraz - nie full ani lite
   * na instalaciu pouzit RPi Imager a v nom
      * zapnúť ssh
      * nastavit pripojenie do WiFi
      * rozlozenie klavesnice na us


2. zabezpecit vzdialeny pristup cez sluzbu [Raspberry Pi Connect](https://connect.raspberrypi.com/devices)

   Najprv treba connect zapnut na zariadeni:

   ```bash
   $ rpi-connect on
   ```

   Potom treba zariadenie pridat do sluzby pomocou nasledujuceho prikazu:

   ```bash
   $ rpi-connect signin
   ```

   Po kliknuti na vygenerovany odkaz alebo prekopirovani vygenerovaneho odkazu do prehliadaca, v ktorom ste prihlaseni do sluzby RPi Connect, sa zariadenie prida do zoznamu vasich zariadeni.

   Odteraz je mozne vsetko robit cez rozhranie sluzby RPi Connect.


3. Aktualizovať

    ```bash
    # nie je uplne nutne urobit aj cely upgrade
    $ sudo apt update && sudo apt upgrade --yes
    ```


4. Nainštalovať docker

    ```bash
    $ curl -sSL https://get.docker.com/ | sudo bash
    ```

    a pridat pouzivatela do skupiny docker:

    ```bash
    $ sudo usermod -aG docker $USER
    ```

    restartovat

    ```bash
    $ sudo reboot
    ```


5. V prípade potreby nainštalovať chýbajúce balíky pre riešenie:

   * `vim` - pre upravu konfiguracie
   * `figlet` a `lolcat` - pre spustenie fancy zdrziavaca pri startovani GUI
   * `curl` - pre skript cakajuci na spustenie potrebnych kontajnerov (je uz nainstalovany)

    ```bash
    $ sudo apt install --no-install-recommends --yes \
        curl \
        vim \
        figlet lolcat
    ```


6. Zabezpečiť, aby sa monitor, resp. HDMI výstup zapínal vždy (aj keď monitor nebude pripojený):

   V subore `/boot/firmware/config.txt`

   ```
   # Forces the Raspberry Pi to send an HDMI signal even if no display is detected.
   hdmi_force_hotplug=1
   ```


7. Vypnut neziaduce sluzby:

   ```bash
   $ sudo systemctl disable cups
   ```


8. Audio cez HDMI

   Ak je RPi pripojene k obrazovke cez HDMI a je mozne v cielovom zariadeni prehravat zvuk, tak staci pri zapnutom GUI v nastaveni hlasitosti prepnut na audio cez HDMI.

   Inac napriklad cez `raspi-config` a menu `System Options > Audio` vybrat polozku HDMI.


9. Externe tlacitko na vypnutie/zapnutie RPi

   RPi ma zabudovanu podporu pre power tlacitko. Na jeho reprezentaciu treba mat momentary switch a pripojit ho na GPIO pin 3. Ak sa pripoji na iny, da sa sice prekonfigurovat a predvolene bude fungovat vypinanie, ale zapinanie fungovat nebude :-(

   Pre pridanie podpory treba pridat do suboru `/boot/firmware/config.txt` na konci tento riadok:

   ```
   dtoverlay=gpio-shutdown
   ```


10. zvysenie vykonu pomocou ZRAM

   nainstalovat balik zram-tools

   ```bash
   $ sudo apt install --yes zram-tools
   ```

   nastavit subor `/ect/default/zramswap` a upravit/pridat tieto riadky:

   ```
   ALGO=zstd
   PERCENT=75
   ```

   restartovat sluzbu

   ```bash
   $ sudo systemctl restart zramswap
   ```

   a overit:

   ```bash
   $ zramctl
   $ free -h
   ```


11. skrytie kurzoru mysi

   kedze vo waylande nefunguje nejak specialne schovavanie kurzoru mysi, tak to urobime tak, ze mysou pohneme mimo obrazovku (vpravo dolu). na to, aby sa to udialo, nainstalujeme nastroje evemu z balika `evemu-tools`:

   ```bash
   $ sudo apt install --yes evemu-tools
   ```

   a nasledne zavolame:

   ```bash
   # kliknutie lavym tlacidlom mysi
   $ evemu-event /dev/input/event3 --type EV_KEY --code BTN_LEFT --value 1 --sync
   # uvolnenie laveho tlacidla mysi
   $ evemu-event /dev/input/event3 --type EV_KEY --code BTN_LEFT --value 0 --sync
   # posun doprava
   $ evemu-event /dev/input/event3 --type EV_REL --code REL_X --value 9999 --sync
   # posun dolu
   $ evemu-event /dev/input/event3 --type EV_REL --code REL_Y --value 9999 --sync
   ```


12. nastavenie pevnej ip adresy na ethernetovy port v pripade, ak bude problem

   najprv sa nastavi ip adresa na 10.20.30.1

   ```bash
   $ sudo nmcli connection modify Wired\ connection\ 1 \
      ipv4.addresses 10.20.30.1/24 \
      ipv4.method manual
   ```

   nasledne sa rozhranie zapne

   ```bash
   $ sudo nmcli connection up Wired\ connection\ 1
   ```


## Autostart

Kedze novy Raspberry Pi OS pouziva labwc, staci upravit subor `autostart` pre pouzivatela v subore `~/.config/labwc/autostart`. Tento subor bude reprezentovat skript, ktory sa spusti.

Konfiguracia pre vsetkych je ulozena v subore `/etc/xdg/labwc/autostart` a vyzera, ze sa pusti vzdy pred pouzivatelskou konfiguraciou. Takze tu pouzivatelsku treba adekvatne upravit a pripadne kill-nut nepotrebne procesy.

V nasledujucich podkapitolach budu teda uvedene riesenia pre spustenie prehliadaca a pre spustenie video prehravaca.


### Spustenie prehliadaca


1. vytvorit autostart skript v `~/.config/labwc/autostart`:

    ```bash
    #!/usr/bin/env bash

    URL="http://localhost"

    # close other services
    pcmanfm --desktop-off
    # killall -9 pcmanfm
    killall -9 lwrespawn
    killall -9 wf-panel-pi

    # wait for service
    printf "Waiting for service to start...\n"
    lxterminal --command '( figlet -c -f slant "Gauss Game"; printf "Loading services for game to run. Please wait...\n") | lolcat --animate -d 30; sleep 5'

    status_code=0
    while [[ "${status_code}" != 200 ]]; do
        # status_code=$(curl --silent --output /dev/null -w "%{http_code}" "${URL}")
        status_code=$(timeout 1 curl --fail --silent --output /dev/null "${URL}")
        printf "...still waiting...\n"
        sleep 4
    done

    # Auto-detect resolution and store in variables
    width=$(cut -d, -f1 /sys/class/graphics/fb0/virtual_size)
    height=$(cut -d, -f2 /sys/class/graphics/fb0/virtual_size)

    # cleanup chromium
    sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' "${HOME}/.config/chromium/Local State"
    sed -i 's/"exited_cleanly":false/"exited_cleanly":true/; s/"exit_type":"[^"]\+"/"exit_type":"Normal"/' "${HOME}/.config/chromium/Default/Preferences"


    # start chromium in kiosk mode
    chromium-browser \
        --no-first-run \
        --start-maximized \
        --noerrdialogs \
        --disable-infobars \
        --incognito \
        --window-size="${width},${height}" --window-position=0,0 \
        --kiosk \
        --hide-scrollbars \
        "${URL}"



### Spustenie video prehravaca



## Vychytávky

### Monitor cez tmux

1. najprv vyvorime skript, ktory budeme chciet spustat. `/usr/local/bin/monitor.bash`

   ```bash
   #!/usr/bin/env bash

   # variables
   CMD1="docker compose --file /home/maker/kulturpark/tapgame/docker-compose/docker-compose.yaml logs --follow --tail 10"
   #CMD2="dry"
   CMD2="htop"
   CMD3='sleep 30; mosquitto_sub -h localhost -t kulturpark/tapgame/# -F "%t: %p"'


   # run monitor with tmux
   tmux new-session -d -s monitor \; \
   	send-keys "${CMD1}" C-m \; \
   	new-window \; \
   	send-keys "${CMD2}" C-m  \; \
       new-window \; \
       send-keys "${CMD3}" C-m \; \
   	attach
   ```

2. Start monitor na konzole 2

   Ulozit do suboru `/etc/systemd/system/monitor.service`

   ```
   [Unit]
   Description=monitor on tty2

   [Service]
   Type=simple
   ExecStart=/usr/local/bin/monitor.bash
   StandardInput=tty
   StandardOutput=tty
   TTYPath=/dev/tty2

   [Install]
   WantedBy=multi-user.target
   ```

   A zapnut:

   ```bash
   $ sudo systemctl enable htop.service
   ```

   **Poznámka:** Podľa https://unix.stackexchange.com/questions/224992/where-do-i-put-my-systemd-unit-file treba `unit` uložiť do súboru `/usr/local/lib/systemd/system/htop.service`


2. Start `mosquitto_sub` na konzole 3

   Ulozit do suboru `/etc/systemd/system/mqtt_sub.service`

   ```
   [Unit]
   Description=mosquitto_sub on tty3

   [Service]
   Type=simple
   #ExecStartPre=/usr/bin/sleep 30
   ExecStart=/usr/local/bin/mqtt_monitor.bash
   Restart=on-failure
   RestartSec=7s
   StandardInput=tty
   StandardOutput=tty
   TTYPath=/dev/tty3

   [Install]
   WantedBy=multi-user.target
   ```

   A zapnut:

   ```bash
   $ sudo systemctl enable mqtt_sub.service
   ```



## Riešenie pre X

1. Vytvoriť súbor `/home/maker/.xinitrc` nasledovne:

   ```
   #!/usr/bin/env bash

   URL="https://localhost"

   # wait for service
   printf "Waiting for service to start...\n"
   status_code=0
   while [[ "${status_code}" != 200 ]]; do
       status_code=$(curl --silent --output /dev/null -w "%{http_code}" "${URL}")
       print "...still waiting...\n"
       sleep 1
   done

   xset -dpms     # disable DPMS (Energy Star) features.
   xset s off     # disable screen saver
   xset s noblank # don't blank the video device

   # allow quitting the x-server with ctrl+alt+backspace
   setxkbmap -option terminate:ctrl_alt_bksp

   # Auto-detect resolution and store in variables
   width=$(cut -d, -f1 /sys/class/graphics/fb0/virtual_size)
   height=$(cut -d, -f2 /sys/class/graphics/fb0/virtual_size)

   # cleanup chromium
   sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' "${HOME}/.config/chromium/Local State"
   sed -i 's/"exited_cleanly":false/"exited_cleanly":true/; s/"exit_type":"[^"]\+"/"exit_type":"Normal"/' "${HOME}/.config/chromium/Default/Preferences"

   # start chromium
   chromium-browser \
        --no-first-run \
        --start-maximized \
        --noerrdialogs \
        --disable-infobars \
        --kiosk \
        --incognito \
        --hide-scrollbars \
        --window-size="${width},${height}" --window-position=0,0 \
        "${URL}"
   ```


## Misc a Cache


1. Zmena wifi

   ```bash
   $ sudo raspi-config
   ```

2. aktivovanie existujuceho wifi pripojenia

   ak nahodou uz existuje wifi connection:

   ```bash
   $ nmcli conn show
   ```

   a treba ho len aktivovat/zmenit, tak z prikazoveho riadku:

   ```bash
   $ nmcli conn up CONN_NAME
   ```



6. Zabezpečiť autologin:

Autologin:

Bud manualne pomocou

```bash
$ sudo raspi-config
```

Alebo spustit prikaz:

```bash
$ sudo systemctl edit getty@tty1
```

A vlozit toto:

```
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin maker --noclear %I $TERM
```




Graficky boot po starte

```bash
$ systemctl --quiet set-default graphical.target
```


konzolovy start:

```bash
$ systemctl --quiet set-default multi-user.target
```














## Cache

6. Upraviť súbor `/etc/default/nodm` nasledovne:

   ```
   # Set NODM_ENABLED to something different than 'false' to enable nodm
   NODM_ENABLED=true

   # User to autologin for
   NODM_USER=maker

   # The Xserver executable and the display name can be omitted, but should
   # be placed in front, if nodm's defaults shall be overridden.
   # with no cursor option
   NODM_X_OPTIONS='-nolisten tcp -nocursor
   ```



## Monitor cez tmux

```bash
#!/usr/bin/env bash

# variables
CMD1="docker compose --file /home/maker/kulturpark/tapgame/docker-compose/docker-compose.yaml logs --follow --tail 10"
CMD2="dry"
CMD3="htop"


# run monitor with tmux
tmux new-session -d -s monitor \; \
	send-keys "${CMD1}" C-m \; \
	new-window \; \
	send-keys "${CMD2}" C-m  \; \
    new-window \; \
    send-keys "${CMD3}" C-m \; \
	attach
```

## Resources

* https://fleetstack.io/blog/raspberry-pi-kiosk-tutorial
* https://gist.github.com/hrr/1a8d769255fdedc7f0b6a18e7fab2e2a
* https://forums.raspberrypi.com/viewtopic.php?t=294014
* navod ako spravit kiosk s wayfire - https://www.raspberrypi.com/tutorials/how-to-use-a-raspberry-pi-in-kiosk-mode/
* navod ako spravit autostart s labwc (v prilozenom pdf na github-e sa nachadzaju navody pre dalsie moznosti) - https://forums.raspberrypi.com/viewtopic.php?t=379321
  * pdf na github-e: https://github.com/thagrol/Guides/tree/main

* zram navod (zrejme starsi) - https://pimylifeup.com/raspberry-pi-zram/
  * dnes bude zrejme stacit nainstalovat balik `zram-tools` a nasledne upravit konfiguraciu

