#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "lib/logging.bash"
source "lib/helpers.bash"


function main() {
    info "Configuring zram"

    sed --in-place 's/ALGO=.*/ALGO=zstd/g' /etc/default/zramswap
    sed --in-place 's/PERCENT=.*/PERCENT=75/g' /etc/default/zramswap
    
    systemctl restart zramswap
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
