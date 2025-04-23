#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "lib/logging.bash"
source "lib/helpers.bash"


function main() {
    info "Setting up RPi Connect"
    
    sudo --user "${USER}" rpi-connect status
    if [[ $? -ne 0 ]]; then
        info "Installing rpi-connect"
        sudo --user "${USER}" rpi-connect on
        sudo --user "${USER}" rpi-connect signin
    fi
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
