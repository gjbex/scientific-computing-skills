#!/usr/bin/env bash

set -euo pipefail

VERSION='1.19.0'
PREFIX='./tools/hyperfine'
METHOD='auto'

usage() {
    cat <<'EOF'
Usage:
  install_hyperfine.sh [--prefix DIR] [--version VERSION]
                       [--method auto|cargo|download]

Install hyperfine into a user-controlled directory without root access.

Options:
  --prefix DIR       Installation prefix. Default: ./tools/hyperfine
  --version VERSION  Hyperfine version. Default: 1.19.0
  --method METHOD    Installation method. Default: auto
  --help             Show this help message
EOF
}

have_command() {
    command -v "$1" >/dev/null 2>&1
}

detect_archive_name() {
    local os arch

    os="$(uname -s)"
    arch="$(uname -m)"

    case "${os}" in
        Linux) ;;
        *)
            echo "Unsupported operating system: ${os}" >&2
            return 1
            ;;
    esac

    case "${arch}" in
        x86_64)
            printf 'hyperfine-v%s-x86_64-unknown-linux-gnu.tar.gz\n' \
                "${VERSION}"
            ;;
        aarch64|arm64)
            printf 'hyperfine-v%s-aarch64-unknown-linux-gnu.tar.gz\n' \
                "${VERSION}"
            ;;
        *)
            echo "Unsupported architecture: ${arch}" >&2
            return 1
            ;;
    esac
}

download_file() {
    local url output

    url="$1"
    output="$2"

    if have_command curl; then
        curl -L --fail --output "${output}" "${url}"
        return 0
    fi

    if have_command wget; then
        wget -O "${output}" "${url}"
        return 0
    fi

    echo 'Need curl or wget to download hyperfine.' >&2
    return 1
}

install_with_cargo() {
    local prefix_abs

    if ! have_command cargo; then
        echo 'cargo not found.' >&2
        return 1
    fi

    prefix_abs="$(realpath -m "${PREFIX}")"
    mkdir -p "${prefix_abs}"
    cargo install \
        --root "${prefix_abs}" \
        --version "${VERSION}" \
        hyperfine
}

install_from_archive() {
    local archive_name url prefix_abs temp_dir archive_path extract_dir

    archive_name="$(detect_archive_name)"
    url="https://github.com/sharkdp/hyperfine/releases/download/\
v${VERSION}/${archive_name}"
    prefix_abs="$(realpath -m "${PREFIX}")"
    temp_dir="$(mktemp -d)"
    archive_path="${temp_dir}/${archive_name}"
    extract_dir="${temp_dir}/extract"

    mkdir -p "${extract_dir}" "${prefix_abs}/bin"
    download_file "${url}" "${archive_path}"

    tar -xzf "${archive_path}" -C "${extract_dir}"
    cp "${extract_dir}"/hyperfine-v"${VERSION}"-*/hyperfine \
        "${prefix_abs}/bin/"
    chmod +x "${prefix_abs}/bin/hyperfine"
    rm -rf "${temp_dir}"
}

while (($# > 0)); do
    case "$1" in
        --prefix)
            PREFIX="$2"
            shift 2
            ;;
        --version)
            VERSION="$2"
            shift 2
            ;;
        --method)
            METHOD="$2"
            shift 2
            ;;
        --help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown argument: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
done

case "${METHOD}" in
    auto)
        if have_command cargo; then
            install_with_cargo
        else
            install_from_archive
        fi
        ;;
    cargo)
        install_with_cargo
        ;;
    download)
        install_from_archive
        ;;
    *)
        echo "Unknown install method: ${METHOD}" >&2
        exit 2
        ;;
esac

cat <<EOF
hyperfine installed under: $(realpath -m "${PREFIX}")
Add it to PATH with:
  export PATH="$(realpath -m "${PREFIX}")/bin:\$PATH"
EOF
