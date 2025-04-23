#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "lib/logging.bash"
source "lib/helpers.bash"


function main() {
    info "Setting up RPi Connect"
    
    if [[ $(sudo --user "${USER}" rpi-connect status) -eq 1 ]]; then
        info "Enabling and Signing"
        sudo --user "${USER}" rpi-connect on
        sudo --user "${USER}" rpi-connect signin
    else
        info "RPi Connect Already Enabled"
    fi
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
