
function convert() {
    set -x
    local input=${1##*.}
    local output=${2##*.}

    if [[ $input == "srt" && $output == "vtt" ]]; then
      ffmpeg -i $1 $2
    fi

    set +x
}

convert input.srt output.vtt