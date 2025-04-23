#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "lib/logging.bash"


function main() {
    info "Setting up Additional Networking on eth"

    nmcli connection modify "Wired connection 1" \
      ipv4.addresses "${IP_ADDR:-10.0.0.1}/24" \
      ipv4.method manual
    nmcli connection up "Wired connection 1"
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
