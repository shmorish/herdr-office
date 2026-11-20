#!/bin/sh
# Copies mods/office/ into Herdr's mods folder (replacing what's there) and checks it.
set -e
cd "$(dirname "$0")"
DEST="$HOME/.config/herdr-app/mods/office"
rm -rf "$DEST"
cp -R mods/office "$DEST"
herdr-app check "$DEST"
