#!/usr/bin/env bash
# vim: set ft=sh ts=4 sw=4 et:

set -o errexit
set -o pipefail
set -o nounset

source lib/logging.bash
source lib/helpers.bash

# load environment variables from .env file
if [[ ! -f ".env" ]]; then
    die "No .env file found. Please create a .env file with the required variables."
fi

set -o allexport
source .env
set +o allexport

function main(){
    printf "${WIFI_SSID}"
    exit 0

    # Check if the script is run as root
    if [ "$EUID" -ne 0 ]; then
        die "This script must be run as root"
    fi

    # update system
    info "Updating system"
    sudo apt update && sudo apt upgrade --yes

    # install additional packages
    info "Installing packages"
    apt install --yes \
        btop \
        curl \
        evemu-tools \
        figlet \
        lolcat \
        tmux \
        vim \
        zram-tools

    # disabling not needed services
    info "Disabling cups"
    sudo systemctl disable cups

    # turn on rpi-connect
    info "Turning on rpi-connect"
    sudo --user "${USER}" rpi-connect on
    sudo --user "${USER}" rpi-connect signin

    # install docker
    info "Installing docker"
    curl -sSL https://get.docker.com/ | bash
    usermod -aG docker "${USER:-pi}"

    # modify raspberry
    info "Modifying Raspberry Pi"
    printf "# Forces the Raspberry Pi to send an HDMI signal even if no display is detected.\nhdmi_force_hotplug=1\n" >> /boot/firmware/config.txt
    printf "# Enable shutdown button on GPIO pin 3\ndtoverlay=gpio-shutdown\n" >> /boot/firmware/config.txt

    # configure zram
    info "Configuring zram"
    sed --in-place 's/ALGO=.*/ALGO=zstd/g' /etc/default/zramswap
    sed --in-place 's/PERCENT=.*/PERCENT=75/g' /etc/default/zramswap
    systemctl restart zramswap

    # set networking
    info "Setting up additional networking"
    nmcli connection modify "Wired connection 1" \
      ipv4.addresses "${IP_ADDR:-10.0.0.1}/24" \
      ipv4.method manual
    nmcli connection up "Wired connection 1"

    nmcli connection add type wifi \
        con-name "${WIFI_CONN_NAME:-conname}" \
        ifname wlan0 \
        ssid "${WIFI_SSID:-ssid}" \
        wifi-sec.key-mgmt wpa-psk \
        wifi-sec.psk "${WIFI_PASSWORD:-password}"
    nmcli connection modify "preconfigured" connection.id "${WIFI_SSID:-ssid}"

    hostnamectl hostname "${HOSTNAME:-pikiosk}"

    # set autostart script
    cp autostart.bash /home/maker/.config/labwc/autostart

    # reboot
    info "Rebooting system in 10s"
    sleep 10
    reboot
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
