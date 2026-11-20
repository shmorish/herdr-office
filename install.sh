#!/bin/sh
# mods/office を TypeScript から変換して Herdr の mods フォルダに置き（今あるものは置き換える）、確かめる。
# esbuild が要る（無ければ nix shell nixpkgs#esbuild か npx esbuild）。
set -e
cd "$(dirname "$0")"
DEST="$HOME/.config/herdr-app/mods/office"
./build.sh "$DEST"
herdr-app check "$DEST"
