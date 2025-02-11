# Raspberry Pi 3 Kiosk

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

4. Nainštalovať chromium

    ```bash
    sudo apt install --no-install-recommends --yes chromium-browser
    ```

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

7. Vytvoriť súbor `/home/maker/.xsession` nasledovne:

   ```
   #!/usr/bin/env bash

   URL="https://www.root.cz"

   xset -dpms     # disable DPMS (Energy Star) features.
   xset s off     # disable screen saver
   xset s noblank # don't blank the video device

   # allow quitting the x-server with ctrl+alt+backspace
   setxkbmap -option terminate:ctrl_alt_bksp

   # Auto-detect resolution and store in variables
   resx=$(cut -d, -f1 /sys/class/graphics/fb0/virtual_size)
   resy=$(cut -d, -f2 /sys/class/graphics/fb0/virtual_size)

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
        --window-size=$resx,$resy --window-position=0,0 \
        "${URL}"
   ```


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

8. Reboot

## Change WiFi

```bash
$ sudo raspi-config
```

## Monitor Configuration

V subore `/boot/firmware/config.txt`

```
# Forces the Raspberry Pi to send an HDMI signal even if no display is detected.
hdmi_force_hotplug=1
```

## Resources

* https://fleetstack.io/blog/raspberry-pi-kiosk-tutorial
* https://gist.github.com/hrr/1a8d769255fdedc7f0b6a18e7fab2e2a
* https://forums.raspberrypi.com/viewtopic.php?t=294014
