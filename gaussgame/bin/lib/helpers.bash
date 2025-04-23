function is_folder_empty() {
    local folder="${1:?Folder name is missing.}"

    if [[ -z $(ls -A "${folder}") ]]; then
        return 0
    else
        return 1
    fi
}


function die() {
    local message="${1}"

    error "${message}"
    exit 1
}


function get_ip() {
    curl --silent ifconfig.me
}


function get_hostname() {
    printf "%s-gw\n" "${IOTGW_ROOM}"
}


function get_dns_for_ip() {
    local ip="${1?IP address is missing.}"

    local result=$(dig -x "${ip}" +short)
    
    if [[ -n "${result}" ]]; then
        printf "%s\n" "${result::-1}"
    fi
}


function get_secret() {
    local filter="${1?Missing filter.}"

    jq --raw-output ".${filter}" /mnt/secrets/secrets.json
}


function get_part_of_uri() {
    # idea from: https://stackoverflow.com/a/1892107
    local part="${1?Missing the name of the part to extract.}"
    local uri="${2?Missing the URI.}"
    local regex="^(.*)://(.*):(.*)@(.*):([0-9]+)(/(.*))?$"
    local group

    # based on the part get regex
    case "${part}" in
        protocol | schema) 
            group=1;;
        user)
            group=2;;
        password)
            group=3;;
        host | broker | server)
            group=4;;
        port) 
            group=5;;
        path)
            group=6;;
        *) 
            die "Unknown part: ${part}"
            ;;
    esac
    
    # extract specified group
    if [[ $uri =~ $regex ]]; then
        printf "%s\n" "${BASH_REMATCH[$group]}"
    else
        die "URI is not in correct format: schema://user:password@host.com:port"
    fi    
}


function choice() {
    if [[ $# == 0 ]]; then
        die "Missing list of values."
    fi

    local list=($@)
    local index=$((RANDOM % ${#list[@]}))

    printf "%s\n" "${list[$index]}"
}


function get_random_string() {
    local length="${1:-15}"
    local alphabet="${2:-a-zA-Z0-9_.-}"

    cat /dev/urandom | tr -dc "${alphabet}" | head -c "${length}"
}


function get_ssid() {
    printf "%s-things" "${IOTGW_ROOM}"
}
