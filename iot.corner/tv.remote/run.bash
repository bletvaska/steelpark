#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


# the main function
function main(){
   # get path of current script
   local DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
   cd "${DIR}"

   # source virtual environment
   source ".venv/bin/activate"

   # run
   python3 -m remote.main
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi

