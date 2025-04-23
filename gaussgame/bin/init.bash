#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "lib/logging.bash"
source "lib/helpers.bash"

# load environment variables from .env file
if [[ ! -f ".env" ]]; then
    die "No .env file found. Please create a .env file with the required variables."
fi

set -o allexport
source .env
set +o allexport


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

    if [[ $# -gt 0 ]]; then
        for script in "$@"; do
            if [[ ! -f "init.d/${script}" ]]; then
                die "Script '${script}' not found in init.d directory."
            else
                scripts="${scripts} init.d/${script}"
            fi
        done
    fi
    
    # run all the provisioning scripts
    for file in $scripts; do
        bash "${file}"
    done
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    trap on_sigint SIGINT
    main "$@"
fi
