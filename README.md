# herdr-office

[Herdr](https://herdr.dev) のウィンドウ上部に置くオフィスの mod。agent ひとりにつき 1 人の女の子がデスクを持ち、作業中・困り中・完了・待機中が絵で一目でわかる。

[kamikuo/herdr-moe-office](https://github.com/kamikuo/herdr-moe-office) を個人用に fork したもの。

## 元の repo との違い

- 表示は日本語だけ。英語・繁体字中国語の文言と、⚙️ の言語切り替えを外した。
- 部屋はナチュラルな部屋だけ。オフホワイトの壁、木の床と腰壁、白とグレーの家具、観葉植物の緑で、ハート・星・リボン・飾り旗・壁紙の柄は描かない。パステル・地雷系・ゴスロリのシーンと ⚙️ のシーン切り替えは外した。
- mod のフォルダ名は `office`（元は `moe-office`）。
- 不具合の修正
  - 親が生きているサブ agent が、デスクの子とインターンの二重に出ていた。
  - 帰る子や配達の子が、歩かずにドアや目的地へワープしていた。
  - レイアウトの `props` を `init` の引数から読んでいて、Herdr から渡らず効いていなかった（今は `props()` から読む）。

## オフィスで起きること

agent の状態ごとに、その子の動きが変わる。

| 状態 | 動き |
|---|---|
| 作業中 | デスクでタイピング。画面のコードが一行ずつ流れる |
| 困り中 | 立ち上がって手を挙げる。5 分たつと泣き出し、画面がピンクに点滅して名札も光る |
| 完了 | バンザイして、画面にごきげんな顔文字。そのターミナルを見に行くまで続く |
| 待機中 | ウォーターサーバーのそばでおしゃべり。10 分たつと、ソファでお昼寝・おしゃべり・お水・おやつを順に回る |

ほかに起きること:

- 新しい agent はドアから入ってきて、閉じた agent は箱を抱えて帰っていく。
- サブ agent はインターンとして、親のデスクのそばにいる。
- 5 分以内に 3 人が作業を終えると、ケーキが届いてお茶会になる。
- 毎時はじめの 3 分間、ウォーターサーバーの上に「お水タイム」の吹き出しが出る。これは使っている人への声かけで、「飲んだよ！」を押すと消える。
- 壁のカレンダーは今日の日付、時計は今の時刻。窓の外は時間帯に合わせて変わり、夜は部屋が暗くなる。
- 猫が 1 匹いる。床を歩き、空いたデスクや本棚の上、壁の猫用の棚で昼寝する。
- キャラクターは 7 人、髪の色は 16 色。agent が初めて出てきたときに決まり、Herdr を再起動しても変わらない。

## 操作

- 女の子にマウスを乗せると、今していることと git のブランチが出る。
- 女の子かデスクをクリックすると、その agent のターミナルへ移る。
- 右上の ⚙️ で「デバッグモード」を入れると、ダミーの同僚を足して、動き・キャラ・髪色・サブ agent・リモート勤務・時間帯を切り替えられる。お茶会とお水タイムもすぐ出せる。

## 入れ方

1. mod を `~/.config/herdr-app/mods/office` に入れる。

   ```sh
   git clone https://github.com/shmorish/herdr-office.git && cd herdr-office && ./install.sh   # esbuild が要る
   ```

   自分の環境では [dotfiles](https://github.com/shmorish/dotfiles) の Home Manager がコミット固定で取ってきて、同じ場所にコピーしている。

2. レイアウト（`~/.config/herdr-app/layouts/<名前>.json`）にブロックを足す。例えばタブバーの下に高さ 250 px で置くなら、次のようにする。

   ```json
   { "id": "office", "type": "block", "content": { "mod": "office" }, "size": { "px": 250 }, "min": 170, "max": 520 }
   ```

   高さは、オフィスと下のペインの境目をドラッグして変えられる。`min` と `max` がその範囲で、中の絵は高さに合わせて拡大・縮小する。親の row や column に `"resizable": false` があるとドラッグできない。

プログラムの実行やネットワークへの接続はしない。

## 開発

コードは `mods/office/*.ts` に TypeScript で書く。`strict` で null チェックも有効。Herdr が読むのは `.js` だけなので、`build.sh` が esbuild で変換する（キャラクターの `chars/*/char.js` はツールが作るファイルなので JS のまま）。

```sh
tsc -p .                 # 型チェック（nix shell nixpkgs#typescript か npx -p typescript tsc）
./build.sh dist/office   # 変換して dist/office に置く
./install.sh             # 変換して ~/.config/herdr-app/mods/office に置く
```

PR と main への push で、CI が型チェックと変換を確かめる。Herdr の型定義（Apache-2.0）は `types/` に写してある。

- 部屋の絵（`mods/office/scene/natural/`）は `tools/scene_art.py` で作る。手で編集しない。

  ```sh
  rm -rf mods/office/scene && python3 -I tools/scene_art.py mods/office/scene
  ```

- 画面の文言は `mods/office/i18n.ts` にまとめてある。
- 作りの詳細とキャラクターの追加方法は [AGENTS.md](AGENTS.md)（英語）にある。
