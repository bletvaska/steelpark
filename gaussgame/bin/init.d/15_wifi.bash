#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "lib/logging.bash"
source "lib/helpers.bash"


function main() {
    info "Setting up WiFi Connection"

    # delete existing WiFi network, if exist
    if [[ $(nmcli connection show) =~ "${WIFI_CONN_NAME} " ]]; then
        info "Deleting existing connection '${WIFI_CONN_NAME}'"
        nmcli connection delete "${WIFI_CONN_NAME}"
    fi

    # if nmcli connection delete "${CONN_NAME}" 2> /dev/null; then
    #     info "Deleting existing network '${CONN_NAME}'"
    # fi

    nmcli connection add type wifi \
        con-name "${WIFI_CONN_NAME:-conname}" \
        ifname wlan0 \
        ssid "${WIFI_SSID:-ssid}" \
        wifi-sec.key-mgmt wpa-psk \
        wifi-sec.psk "${WIFI_PASSWORD:-password}"

    # nmcli connection modify "preconfigured" connection.id "${WIFI_SSID:-ssid}"
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
