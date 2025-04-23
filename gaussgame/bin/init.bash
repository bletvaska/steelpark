#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "/app/lib/logging.bash"

# TODO: check handling of SIGINT
function on_sigint() {
    fatal "SIGINT received. Quit."
    exit 1
}

function main() {
    # check if config file exists as parameter
    if [[ $# -eq 0 ]]; then
        fatal "No config file provided. Exiting."
        exit 1
    fi
    
    local config_file="${1}"
    if [[ ! -f "${config_file}" ]]; then
        fatal "Config file does not exist. Exiting."
        exit 1
    fi
    
    # check if config file is empty


    # run all the provisioning scripts
    for file in init.d/*.bash; do
        bash "${file}"
    done
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    trap on_sigint SIGINT
    main "$@"
fi
