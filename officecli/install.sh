#!/usr/bin/env bash
# Fetch the officecli binary into the image. Run at BUILD time, where the network is available —
# a task never has it. Pinned to an exact release and checksum-verified: an unpinned "latest" would
# make two builds of the same image tag behave differently, and a silent upstream change to a
# document tool is the kind of thing nobody notices until a customer's file comes out wrong.
set -euo pipefail

VERSION="v1.0.143"
case "$(uname -m)" in
  x86_64|amd64)  ASSET="officecli-linux-x64";   SHA="6a29c598a789b57c92c03e560907d3f131a4bd0a068785b1d338a86fc31a58a7" ;;
  aarch64|arm64) ASSET="officecli-linux-arm64"; SHA="c50298e4698fcd1b15fe1a0f096405ad260b5c84d4440882582d0bba1e57bd49" ;;
  *) echo "officecli: unsupported architecture $(uname -m)" >&2; exit 1 ;;
esac

URL="https://github.com/iOfficeAI/OfficeCLI/releases/download/${VERSION}/${ASSET}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "officecli: fetching ${VERSION} ${ASSET}"
curl -fsSL --retry 3 -o "$TMP/officecli" "$URL"
echo "${SHA}  $TMP/officecli" | sha256sum -c - >/dev/null

install -m 0755 "$TMP/officecli" /usr/local/bin/officecli
/usr/local/bin/officecli --version >/dev/null
echo "officecli: installed $(/usr/local/bin/officecli --version)"
