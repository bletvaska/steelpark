#!/usr/bin/env bash

global URL="http://localhost"


function main(){
    # move mouse cursor out of the screen
    evemu-event /dev/input/event0 --type EV_REL --code REL_X --value 9999 --sync
    evemu-event /dev/input/event0 --type EV_REL --code REL_Y --value 9999 --sync

    # close other services
    # turns off pcmanfm for desktop management
    pcmanfm --desktop-off
    # watchdog for running apps
    killall -9 lwrespawn
    killall -9 wf-panel-pi

    # wait for service
    printf "Waiting for service to start...\n"
    lxterminal --command '(figlet -c -f slant "Gauss Game"; printf "Loading services for game to run. Please wait...\n") | lolcat --animate -d 30; sleep 5'

    status_code=0
    while [[ "${status_code}" != 200 ]]; do
        # status_code=$(curl --silent --output /dev/null -w "%{http_code}" "${URL}")
        status_code=$(timeout 1 curl --fail --silent --output /dev/null "${URL}")
        printf "...still waiting...\n"
        sleep 4
    done

    # Auto-detect resolution and store in variables
    width=$(cut -d, -f1 /sys/class/graphics/fb0/virtual_size)
    height=$(cut -d, -f2 /sys/class/graphics/fb0/virtual_size)

    # cleanup chromium
    sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' "${HOME}/.config/chromium/Local State"
    sed -i 's/"exited_cleanly":false/"exited_cleanly":true/; s/"exit_type":"[^"]\+"/"exit_type":"Normal"/' "${HOME}/.config/chromium/Default/Preferences"


    # start chromium in kiosk mode
    chromium-browser \
        --no-first-run \
        --start-maximized \
        --noerrdialogs \
        --disable-infobars \
        --incognito \
        --window-size="${width},${height}" --window-position=0,0 \
        --kiosk \
        --hide-scrollbars \
        "${URL}"
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi