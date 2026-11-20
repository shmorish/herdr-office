// 画面に出る言葉（日本語だけ）。

const T = {
  // The team board
  "board.working": "作業中",
  "board.done": "完了",
  "board.blocked": "困り中",
  "board.idle": "休憩中",
  "board.nap": "お昼寝",
  "board.interns": "インターン",
  "board.pizza": "お茶会!",
  // Speech bubbles
  help: "助けて!!",
  thanks: "できた～♡",
  pizzaHere: "ケーキ届いたよ 🍰",
  chat: ["今日もがんばろ～", "甘いもの食べたい…", "📱…", "ねむ～い", "いい天気 ☀️", "♡", "見た見た？", "もう一杯だけ～", "えへへ", "帰りにケーキ？🍰", "うちの子が一番かわいい", "✨"],
  sip: ["💧", "ごくごく", "ぷは～", "🥤", "つめたい！", "水分補給 ♡"],
  snack: ["🍪", "クッキーもう一枚…", "☕", "もぐもぐ", "マカロン ♡", "🍮", "ちょっとだけ"],
  pizzaChat: ["🍰", "おいしい！", "お茶おかわり？", "🫖", "最高のお茶会", "いちご ♡"],
  waterDone: "飲んだよ！",
  water: "💧 お水タイム！ひと口どうぞ～",
  months: ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
  weekdays: ["日", "月", "火", "水", "木", "金", "土"],
  // The room
  empty: "まだ誰も出社してないよ～ agent を開くと入ってくるよ。",
  thinking: "考え中…",
  remote: "リモート",
  // The settings panel
  "settings.title": "設定",
  "settings.debug": "デバッグモード",
  "debug.title": "Debug：ダミーの同僚",
  "debug.char": "キャラ",
  "debug.hair": "髪色",
  "debug.add": "＋ 追加",
  "debug.clear": "全部消す",
  "debug.kids": "子",
  "debug.remote": "リモート",
  "debug.party": "🍰 お茶会",
  "debug.partyEnd": "🍰 お茶会おわり",
  "debug.water": "💧 お水",
  "act.idle": "待機",
  "act.walk": "歩く",
  "act.typing": "タイピング",
  "act.blocked": "困り中",
  "act.alarm": "警報",
  "act.done": "完了",
  "act.sleep": "居眠り",
  "time.auto": "時間：自動",
  "time.12": "時間：昼",
  "time.18": "時間：夕方",
  "time.22": "時間：夜",
};

// `key` の言葉（文字列、または会話のように候補のリスト）。
export function t(key) {
  return T[key] ?? key;
}
