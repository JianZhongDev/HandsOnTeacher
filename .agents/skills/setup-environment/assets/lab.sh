#!/usr/bin/env bash
# Course lab launcher (Linux, macOS, WSL). Run it from the course folder.
#
#   ./lab.sh list                      your labs
#   ./lab.sh 03/L01                    run module 03, lesson L01 with default settings
#   ./lab.sh 03/L01 help               the settings this lab lets you change
#   ./lab.sh 03/L01 size=5000          change one setting (results are kept per setting)
#   ./lab.sh run <script> [args]       run any script with the course runtime
#   ./lab.sh check                     check that the runtime works
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export COURSE_DIR="$HERE"

# ---- set by setup-environment (see course.json) ---------------------------
RUN=("$HERE/.env/bin/python" -B)          # command that runs a lab file
LAB_FILE="lab.py"                         # lab file name inside each lesson folder
CHECK=("${RUN[@]}" -c "import handson; print('runtime OK')")
export PYTHONPATH="$HERE/_shared${PYTHONPATH:+:$PYTHONPATH}"
# ---------------------------------------------------------------------------

cmd="${1:-list}"
case "$cmd" in
  list)
    echo "Labs (run with: lab <module>/<lesson> [key=value ...]):"
    found=0
    for f in "$HERE"/[0-9][0-9]-*/lessons/L*/"$LAB_FILE"; do
      [[ -e "$f" ]] || continue
      d=$(dirname "$f"); m=$(basename "$(dirname "$(dirname "$d")")"); l=$(basename "$d")
      echo "  ${m%%-*}/${l%%-*}   $m / $l"
      found=1
    done
    [[ $found -eq 1 ]] || echo "  (none yet: the teaching agent creates labs as lessons are prepared)"
    ;;
  check)
    exec "${CHECK[@]}"
    ;;
  run|py)
    shift
    [[ $# -ge 1 ]] || { echo "usage: lab run <script> [args]" >&2; exit 1; }
    [[ -f "$1" ]] || { echo "No such script: $1" >&2; exit 1; }
    script_dir="$(cd "$(dirname "$1")" && pwd)"; script="$script_dir/$(basename "$1")"; shift
    cd "$script_dir"
    exec "${RUN[@]}" "$script" "$@"
    ;;
  -h|--help|help)
    sed -n '2,10p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
    ;;
  */*)
    module="${cmd%%/*}"; lesson="${cmd#*/}"; shift
    matches=( "$HERE"/"$module"-*/lessons/"$lesson"*/"$LAB_FILE" )
    if [[ ! -e "${matches[0]}" ]]; then
      echo "No lab found for $module/$lesson. Try: lab list" >&2
      exit 1
    fi
    cd "$(dirname "${matches[0]}")"
    exec "${RUN[@]}" "$LAB_FILE" "$@"
    ;;
  *)
    echo "Unknown command '$cmd'. Try: lab help" >&2
    exit 1
    ;;
esac
