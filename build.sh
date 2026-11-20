#!/bin/sh
# mods/office を $1 に置く。*.ts は esbuild で *.js に変換する（Herdr が読むのは .js だけ）。
# import はそのまま残す（gpui-kit や herdr は Herdr が実行時に渡す）。
set -eu
out=$1
rm -rf "$out"
mkdir -p "$out"
(cd mods/office && find . -type f ! -name '*.ts' ! -name '*.d.ts' ! -name jsconfig.json) | while read -r f; do
  mkdir -p "$out/$(dirname "$f")"
  cp "mods/office/$f" "$out/$f"
done
for f in mods/office/*.ts; do
  esbuild "$f" --outfile="$out/$(basename "${f%.ts}").js" --format=esm --target=es2022 --charset=utf8 --log-level=warning
done
