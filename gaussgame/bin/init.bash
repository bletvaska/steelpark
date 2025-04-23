#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "lib/logging.bash"
source "lib/helpers.bash"

# TODO: check handling of SIGINT
function on_sigint() {
    fatal "SIGINT received. Quit."
    exit 1
}

function main() {
    # Check if the script is run as root
    if [ "$EUID" -ne 0 ]; then
        die "This script must be run as root"
    fi

    local scripts=$(ls init.d/*.bash 2> /dev/null)

    # check if config file exists as parameter
    if [[ $# -gt 0 ]]; then
        scripts="${@}"
    fi
    
    # run all the provisioning scripts
    for file in $scripts; do
        bash "init.d/${file}"
    done
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    trap on_sigint SIGINT
    main "$@"
fi
