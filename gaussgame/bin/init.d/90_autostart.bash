#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "lib/logging.bash"


function main() {
    info "Creating autostart Script for labwc"

    cp templates/autostart.bash /home/maker/.config/labwc/autostart
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
