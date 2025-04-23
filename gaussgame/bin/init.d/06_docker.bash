#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "lib/logging.bash"
source "lib/helpers.bash"


function main() {
    info "Installing docker"

    if [[ ! -f /usr/bin/docker ]]; then
        curl -sSL https://get.docker.com/ | bash
        usermod -aG docker "${USER:-pi}"
    else
        info "Docker already installed"
    fi
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
