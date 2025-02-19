# Raspberry Pi 3 Kiosk


## System Setup

1. Nainštalovať [Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/) - základný, nie Lite

    * zapnúť ssh
    * pripojiť sa na WiFi


2. Aktualizovať

    ```bash
    $ sudo apt update && sudo apt upgrade --yes
    $ sudo apt install --no-install-recommends --yes \
        xserver-xorg x11-xserver-utils xinit \
        lightdm
    ```


3. Nainštalovať docker

    ```bash
    $ curl -sSL https://get.docker.com/ | sudo sh
    ```

    a pridat pouzivatela do skupiny docker:

    ```bash
    $ sudo usermod -aG docker $USER
    ```


4. V prípade potreby nainštalovať chýbajúce balíky pre riešenie

    ```bash
    $ sudo apt install --no-install-recommends --yes chromium-browser
    ```


5. Zabezpečiť, aby sa monitor, resp. HDMI výstup zapínal vždy (aj keď monitor nebude pripojený):

   V subore `/boot/firmware/config.txt`

   ```
   # Forces the Raspberry Pi to send an HDMI signal even if no display is detected.
   hdmi_force_hotplug=1
   ```


## Spustenie prehravaca


1. vytvorit skript na prehravanie v `/usr/local/bin/kiosk.bash`:

    ```bash
    #!/usr/bin/env bash

    URL="http://localhost"

    # wait for service
    printf "Waiting for service to start...\n"
    status_code=0
    while [[ "${status_code}" != 200 ]]; do
        status_code=$(curl --silent --output /dev/null -w "%{http_code}" "${URL}")
        printf "...still waiting...\n"
        sleep 1
    done

    killall -9 lwrespawn
    killall -9 pcmanfm
    killall -9 wf-panel-pi

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
        --kiosk \
        --incognito \
        --hide-scrollbars \
        --window-size="${width},${height}" --window-position=0,0 \
        "${URL}"
    ```

    nastavit prava na spustanie:

    ```bash
    $ chmod +x /usr/local/bin/kiosk.bash
    ```

2. vytovrit autostart subor  `~/.config/autostart/kiosk.desktop`:

    ```desktop
    [Desktop Entry]
    Type=Application
    Name=Kiosk Mode
    Exec=/usr/local/bin/kiosk.bash
    X-GNOME-Autostart-enabled=true
    ```


## Vychytávky

1. Start htop na konzole 2

   Ulozit do suboru `/etc/systemd/system/htop.service`

   ```
   [Unit]
   Description=htop on tty2

   [Service]
   Type=simple
   ExecStart=/usr/bin/htop
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


## Resources

* https://fleetstack.io/blog/raspberry-pi-kiosk-tutorial
* https://gist.github.com/hrr/1a8d769255fdedc7f0b6a18e7fab2e2a
* https://forums.raspberrypi.com/viewtopic.php?t=294014
