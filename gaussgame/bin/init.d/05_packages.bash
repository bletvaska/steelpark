#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "lib/logging.bash"
source "lib/helpers.bash"

function main() {
    info "Update system and Install Additional Packages"

    # update system
    apt update && sudo apt upgrade --yes

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
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
