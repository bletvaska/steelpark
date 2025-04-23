source "lib/colors.bash"

function log() {
    local level="${1?Log level is missing.}"
    shift
    local message="${*}"
    local now
    local color

    now=$(date +%H:%M:%S)
    level=$(echo "${level}" | tr a-z A-Z)

    # pick color for level
    case "${level}" in
        "ERROR" )
            color="${RED}"
            ;;
        "WARNING" | "WARN" )
            color="${YELLOW}"
            ;;
        "SUCCESS" )
            color="${GREEN}"
            ;;
        "DEBUG" )
            color="${BLUE}"
            ;;
        "CRITICAL" | "FATAL" )
            color="${BG_RED}"
            ;;
        *)
            color="${WHITE}"
            ;;
    esac

    # printf "${GREEN}%s${RESET} ${color}%-7s %s${RESET}\n" \
    #     "${now}" "${level}" "${message}"

    printf "${color}%-7s %s${RESET}\n" "${level}" "${message}"
}


function debug() {
    log DEBUG "${*}"
}


function info() {
    log INFO "${*}"
}


function warning() {
    log WARNING "${*}"
}


function error() {
    log ERROR "${*}"
}


function critical() {
    log CRITICAL "${*}"
}


function success() {
    log SUCCESS "${*}"
}
