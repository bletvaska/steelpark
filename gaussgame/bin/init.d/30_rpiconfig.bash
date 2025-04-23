#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

source "lib/logging.bash"
source "lib/helpers.bash"


function main() {
    info "Modifying Raspberry Pi Config"

    # delete existing lines first
    sed --in-place '/^#\?hdmi_force_hotplug=1/d' /boot/firmware/config.txt
    sed --in-place '/^#\?dtoverlay=gpio-shutdown/d' /boot/firmware/config.txt

    # append options as new lines at the end
    printf "hdmi_force_hotplug=1\n" >> /boot/firmware/config.txt
    printf "dtoverlay=gpio-shutdown\n" >> /boot/firmware/config.txt
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
