// The room and everything in it. Art is listed in ART: each entry is a file and its size in
// scene units (1 unit = U px). They're vector placeholders from tools/scene_art.py;
// to use a drawn image instead, save it with the same aspect ratio and change its `src`.
// Boards, screens and signs whose content changes are drawn here with divs.
import { div, svg, image } from "gpui-kit";
import type { Color, NativeElement } from "gpui-kit";
import { run } from "herdr";
import { dollSprite, BOX, PERSON } from "./doll.js";
import { t } from "./i18n.js";

// One art file and its size in units. A `mask` piece is drawn in one colour (art()'s `tint`).
interface ArtPiece { src: string; w: number; h: number; mask?: boolean }
// The sky out of the windows (main.js picks it by the hour).
export interface Sky { top: Color; bottom: Color; stars?: boolean }
// A team board row: colour, label, count, and whether to show it (shown unless false).
type BoardRow = [color: Color, label: string, n: number | string, show?: boolean];
// A remote agent's tile on the video call.
export interface Remote { address: string; pane?: string | null; machine: string; name: string; status: string | null; title: string }

// The room's colours drawn as divs (the art is in scene/natural/, made by scene_art.py).
export const INK: Color = "#4a4038"; // outlines and text
const WALL: Color = "#f1ede6";
export const FLOOR: Color = "#d9b98f";
const WAIN: Color = "#d8cbb8", WAIN_STRIPE: Color = "#d0c2ad", RAIL: Color = "#b89a78", BASE: Color = "#a88560";
const PINS: [Color, Color] = ["#4f6b8a", "#6f8f69"];
const CALENDAR = { head: "#ffffff", day: INK, week: "#4f6b8a" } satisfies Record<string, Color>;
const BOARD = { bg: "#fbf8f2", border: RAIL, text: INK } satisfies Record<string, Color>;
const DIR = "mods/office/scene/natural/";
export const ART: Record<string, ArtPiece> = {
  desk: { src: "desk.svg", w: 32, h: 14 },
  lamp: { src: "lamp.svg", w: 5, h: 9 },
  monitor: { src: "monitor.svg", w: 14, h: 13 },
  chair: { src: "chair.svg", w: 12, h: 20 },
  couch: { src: "couch.svg", w: 36, h: 17 },
  cooler: { src: "cooler.svg", w: 11, h: 25 },
  counter: { src: "counter.svg", w: 36, h: 21 },
  cake: { src: "cake.svg", w: 10, h: 5 },
  cakeCarry: { src: "cake_carry.svg", w: 9, h: 3 },
  bookshelf: { src: "bookshelf.svg", w: 14, h: 26 },
  catshelf: { src: "catshelf.svg", w: 14, h: 5 },
  calendar: { src: "calendar.svg", w: 13, h: 16 },
  // Desk things, one set per character (doll.js CHARACTERS), from slot x 31 on the desk top.
  "set_jirai": { src: "set_jirai.svg", w: 8, h: 10 },
  "set_intern": { src: "set_intern.svg", w: 8, h: 10 },
  "set_designer-cute": { src: "set_designer-cute.svg", w: 8, h: 10 },
  "set_engineer-hoodie": { src: "set_engineer-hoodie.svg", w: 8, h: 10 },
  "set_wavy-blouse": { src: "set_wavy-blouse.svg", w: 8, h: 10 },
  "set_twintail-blazer": { src: "set_twintail-blazer.svg", w: 8, h: 10 },
  "set_bob-jacket": { src: "set_bob-jacket.svg", w: 8, h: 10 },
  box: { src: "box.svg", w: 7, h: 6 },
  plant: { src: "plant.svg", w: 10, h: 20 },
  door: { src: "door.svg", w: 17, h: 29 },
  doorOpen: { src: "door_open.svg", w: 17, h: 29 },
  doorSign: { src: "door_sign.svg", w: 12, h: 4 },
  window: { src: "window.svg", w: 30, h: 26 },
  clock: { src: "clock.svg", w: 14, h: 16 },
  floor: { src: "floor.svg", w: 32, h: 8 },
  rug: { src: "rug.svg", w: 40, h: 5 },
  catSit: { src: "cat_sit.svg", w: 14, h: 11 },
  catSleep: { src: "cat_sleep.svg", w: 14, h: 11 },
  catWalk0: { src: "cat_walk_0.svg", w: 14, h: 11 },
  catWalk1: { src: "cat_walk_1.svg", w: 14, h: 11 },
  stool: { src: "stool.svg", w: 9, h: 7 },
  laptop: { src: "laptop.svg", w: 6, h: 4 },
};

// Where things sit, in units. Desk slot: SLOT wide; the chair, the seated doll's box and the
// desk front are placed from the slot's left edge. Seats and the desk top match the dolls'
// typing and sleeping poses (seat at 7 units, hands at 12).
export const SLOT = 38;
export const DESK = { x: 10, top: 12, chair: 2, monitor: 21, lamp: 34, set: 31,
  screen: [21 + 1.6, 1.6, 10.8, 7.4] /* x, y from the monitor's top, w, h */ };
export const COUNTER_TOP = 11;
export const CAT_W = 14;


// An art piece with its bottom-left corner at (x, bottom), in px. `flip`: the mirrored file
// (<name>_l.<ext>), for things that turn around. A `mask` piece is one colour, `tint`.
export function art(id: string, x: number, bottom: number, U: number, tint?: Color, flip = false): NativeElement {
  const a = ART[id];
  const src = DIR + (flip ? a.src.replace(/(\.\w+)$/, "_l$1") : a.src);
  const el = a.mask ? svg(src).text_color(tint ?? INK) : image(src);
  return el.absolute().left(x).top(bottom - a.h * U).w(a.w * U).h(a.h * U);
}
export const artW = (id: string, U: number): number => ART[id].w * U;

// Plain wall, wainscot and floor, filling the whole view.
export function room(W: number, H: number, wallBottom: number, U: number): NativeElement[] {
  const els = [div().absolute().left(0).top(0).w(W).h(wallBottom).bg(WALL)];
  const wain = 9 * U;
  els.push(div().absolute().left(0).top(wallBottom - wain).w(W).h(wain).bg(WAIN));
  for (let x = U * 2; x < W; x += U * 4) els.push(div().absolute().left(x).top(wallBottom - wain + U).w(U * 1.4).h(wain - 2 * U).rounded(U).bg(WAIN_STRIPE));
  els.push(div().absolute().left(0).top(wallBottom - wain - U * 0.8).w(W).h(U * 1.2).rounded(U).bg(RAIL));
  els.push(div().absolute().left(0).top(wallBottom).w(W).h(Math.max(0, H - wallBottom)).bg(FLOOR));
  const ft = ART.floor.h * U, fw = ART.floor.w * U;
  for (let y = wallBottom, r = 0; y < H; y += ft, r++)
    for (let x = (r % 2) * -fw / 2; x < W; x += fw) els.push(art("floor", x, y + ft, U));
  els.push(div().absolute().left(0).top(wallBottom - U * 0.6).w(W).h(U * 1.2).bg(BASE));
  return els;
}

// The view out of the windows is one landscape across the room: the sky, one sun or moon
// (at `sunX`, room px, so it shows in one window only), clouds drifting across, and a
// skyline along the bottom. Each window shows its own stretch of it.
const SKYLINE = (() => {
  const out = [];
  for (let x = 0, k = 1; x < 4000; k++) { // in units; 4000 is wider than any room
    const w = 5 + (k * 37) % 7, h = 3 + (k * 53) % 8;
    out.push({ x, w, h, lit: (k * 29) % 5 });
    x += w + (k % 3 === 0 ? 2 : 0.4);
  }
  return out;
})();

export function window_(x: number, y: number, U: number, sky: Sky, sunX: number): NativeElement {
  const [gx, gy, gw, gh] = [3 * U, 3 * U, 24 * U, 20 * U];
  const ox = x + gx; // where this glass sits in the room
  const night = Boolean(sky.stars);
  const city = night ? "#4b4878" : sky.top === "#ffd6a8" ? "#d9a0a8" : "#b9d3ea";
  const glass = div().absolute().left(gx).top(gy).w(gw).h(gh).bg(sky.bottom).overflow_hidden()
    .child(div().absolute().left(0).top(0).w(gw).h(gh * 0.55).bg(sky.top))
    .when(night, (el) => el.children([[0.2, 0.3], [0.5, 0.5], [0.75, 0.25], [0.35, 0.15]].map(([sx, sy], k) =>
      div().absolute().left(((sx * gw + ox * 0.37) % gw)).top(sy * gh).size(U * 0.6).rounded_full().bg("#fff7d6").loop("opacity", { from: 0.3, to: 1, period: 1600 + k * 300 }))))
    .when(sunX >= ox - 4 * U && sunX <= ox + gw, (el) => el.child(div().absolute().left(sunX - ox).top(gh * 0.18).size(4 * U).rounded_full().bg(night ? "#f6f0d6" : "#ffe7a0")))
    .children([0, 1, 2].map((k) => {
      const period = 60000 + k * 23000; // clouds cross the whole room, slowly
      const cx = along(-12 * U, 4000, period, k * 19000) - ox;
      return div().absolute().left(cx).top(gh * (0.1 + k * 0.12)).w((9 - k * 2) * U).h(2.4 * U).rounded(2 * U).bg("#ffffff").opacity(night ? 0.15 : 0.85);
    }))
    .children(SKYLINE.filter((b) => b.x * U < ox + gw && (b.x + b.w) * U > ox).map((b) => div().absolute()
      .left(b.x * U - ox).top(gh - b.h * U).w(b.w * U).h(b.h * U).bg(city)
      .when(night && b.lit, (el) => el.child(div().absolute().left(U).top(U).size(U * 0.8).bg("#ffe7a0").opacity(0.8)))));
  return div().absolute().left(x).top(y).w(ART.window.w * U).h(ART.window.h * U)
    .child(glass).child(art("window", 0, ART.window.h * U, U));
}

// One-way motion: `loop` always goes there and back, so things that fall or drift are
// placed from the clock on every redraw instead (the view redraws every ~110 ms).
export const along = (from: number, to: number, period: number, phase = 0): number => from + (to - from) * (((Date.now() + phase) % period) / period);

// The cat clock: hands from clock/, one file per angle.
export function clock(x: number, y: number, U: number, date: Date): NativeElement {
  const h = (date.getHours() % 12) * 4 + Math.floor(date.getMinutes() / 15), m = date.getMinutes();
  const hand = (f: string) => image(`${DIR}clock/${f}.svg`).absolute().left(0).top(0).w(ART.clock.w * U).h(ART.clock.h * U);
  return div().absolute().left(x).top(y).w(ART.clock.w * U).h(ART.clock.h * U)
    .child(art("clock", 0, ART.clock.h * U, U)).child(hand(`m_${m}`)).child(hand(`h_${h}`));
}

// A tear-off calendar showing today, the clock's size: the month on the header, the day big,
// the weekday.
export function calendar(x: number, y: number, U: number, date: Date, month: string, weekday: string): NativeElement {
  const c = CALENDAR;
  return div().absolute().left(x).top(y).w(ART.calendar.w * U).h(ART.calendar.h * U)
    .child(art("calendar", 0, ART.calendar.h * U, U))
    .child(div().absolute().left(1.4 * U).top(3.4 * U).w(10.2 * U).h(3.6 * U).flex().items_center().justify_center()
      .text_size(Math.max(7, 1.9 * U)).font_bold().text_color(c.head).child(month))
    .child(div().absolute().left(1.4 * U).top(7.2 * U).w(10.2 * U).h(5.4 * U).flex().items_center().justify_center()
      .text_size(Math.max(11, 4.6 * U)).font_bold().text_color(c.day).child(String(date.getDate())))
    .child(div().absolute().left(1.4 * U).top(12.4 * U).w(10.2 * U).h(2.4 * U).flex().items_center().justify_center()
      .text_size(Math.max(7, 1.7 * U)).font_bold().text_color(c.week).child(weekday));
}

// The team board: counts by status.
export function board(x: number, y: number, U: number, rows: BoardRow[]): NativeElement {
  const b = BOARD;
  return div().absolute().left(x).top(y).w(44 * U).px(2.5 * U).py(1.6 * U).rounded(2.5 * U).bg(b.bg)
    .border_2().border_color(b.border).flex().flex_wrap().gap_x(3 * U).text_size(Math.max(9, 2.3 * U)).font_bold()
    .child(div().absolute().left(4 * U).top(-U).size(2 * U).rounded_full().bg(PINS[0]))
    .child(div().absolute().right(4 * U).top(-U).size(2 * U).rounded_full().bg(PINS[1]))
    .children(rows.filter(([, , , show]) => show !== false).map(([color, label, n]) =>
      div().w(17 * U).flex().items_center().gap(U).child(div().size(1.6 * U).flex_none().rounded_full().bg(color))
        .child(div().flex_1().text_color(b.text).child(label)).child(div().text_color(color).child(String(n)))));
}

// A face in a frame: the doll's head and shoulders.
function headshot(address: string, w: number, h: number, U: number): NativeElement {
  const p = U * 1.25;
  return div().relative().w(w).h(h).overflow_hidden().rounded(U).bg("#e6dcfa")
    .child(div().absolute().left(w / 2 - 8 * p).top(h * 0.08 - 2 * p).w(PERSON * p).h(BOX * p).child(dollSprite(address, "idle", 1, p)));
}

// The video call with everyone working from another machine. Click a tile to go there.
export function videoWall(x: number, y: number, U: number, remotes: Remote[]): NativeElement {
  const ring: Record<string, Color> = { working: "#7fb6ff", blocked: "#ff8a9a", done: "#79c9ad", idle: "#cbb8f0" };
  const ts = 13 * U; // a tile's size (not `t`: that's the translator)
  const tile = (r: Remote) => div().id(`call-${r.address}`).w(ts).h(ts).relative().overflow_hidden().rounded(2 * U)
    .border_2().border_color(ring[r.status as string] ?? ring.idle).cursor_pointer().tooltip(r.title)
    .on_click(() => { if (r.pane) run("pane.focus", { pane: r.pane }); })
    .child(headshot(r.address, ts, ts, U * 0.9))
    .when(r.status === "idle", (el) => el.child(div().absolute().left(0).top(0).size_full().bg("#5a4a63").opacity(0.35)))
    .when(r.status === "blocked", (el) => el.child(div().absolute().right(U).top(U).px(U).rounded(U).bg("#e8586f")
      .text_size(9).font_bold().text_color("#ffffff").child("!").loop("opacity", { from: 0.4, to: 1, period: 600 })))
    .when(r.status === "done", (el) => el.child(div().absolute().right(U).top(U).px(U).rounded(U).bg("#3f9a7a")
      .text_size(9).font_bold().text_color("#ffffff").child("♡")))
    .child(div().absolute().left(0).bottom(0).w_full().h(3 * U).bg("#00000066").px(U).flex().items_center()
      .text_size(Math.max(7, 1.8 * U)).text_color("#ffffff").child(div().truncate().child(r.name)));
  const machines = [...new Set(remotes.map((r) => r.machine))].join(", ");
  return div().absolute().left(x).top(y).p(U).rounded(2.5 * U).bg("#5a4a63").flex().flex_col().gap(U)
    .child(div().flex().items_center().gap(U).max_w(ts * 3 + 2 * U).text_size(Math.max(7, 1.8 * U)).font_bold()
      .child(div().size(1.4 * U).flex_none().rounded_full().bg("#ff8a9a").loop("opacity", { from: 0.3, to: 1, period: 1200 }))
      .child(div().truncate().text_color("#fffaf3").child(`${t("remote")} · ${machines}`)))
    .child(div().flex().flex_wrap().gap(U).max_w(ts * 3 + 2 * U).children(remotes.slice(0, 6).map(tile)));
}

export function door(x: number, wallBottom: number, U: number, open: boolean): NativeElement {
  return div().absolute().left(0).top(0).size_full().children([
    art(open ? "doorOpen" : "door", x, wallBottom + 0.4 * U, U),
    art("doorSign", x + 2.5 * U, wallBottom - ART.door.h * U - 0.6 * U, U),
  ]);
}
