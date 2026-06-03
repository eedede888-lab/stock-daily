"use strict";
const DATA = "data";
const cache = {}, pending = {};
let INDEX = null, curDate = null, curView = "market", curStock = null, wrChart = null;

const $ = s => document.querySelector(s);

// 以 <script> 載入資料（file:// 直接雙擊也能用，免伺服器）
window.__DATAREG = (key, data) => {
  cache[key] = data;
  if (pending[key]) { pending[key].forEach(fn => fn(data)); delete pending[key]; }
};
function loadData(key) {
  if (cache[key]) return Promise.resolve(cache[key]);
  return new Promise((resolve, reject) => {
    (pending[key] = pending[key] || []).push(resolve);
    const sc = document.createElement("script");
    sc.src = `${DATA}/${key}.js`;
    sc.onerror = () => { delete pending[key]; reject(new Error("無法載入 " + key)); };
    document.head.appendChild(sc);
  });
}
const fmtInt = n => (n === null || n === undefined || n === "") ? "" : Number(n).toLocaleString("en-US", {maximumFractionDigits: 0});
const fmt1 = n => (n === null || n === undefined || n === "") ? "" : Number(n).toLocaleString("en-US", {maximumFractionDigits: 1});
const fmt2 = n => (n === null || n === undefined || n === "") ? "" : Number(n).toLocaleString("en-US", {maximumFractionDigits: 2});
const num = n => (typeof n === "number") ? n : (parseFloat(String(n).replace(/[,%]/g, "")) || 0);

async function init() {
  INDEX = await loadData("index");
  const sel = $("#dateSel");
  sel.innerHTML = INDEX.dates.map(d => `<option value="${d.date}">${d.label}</option>`).join("");
  curDate = INDEX.dates[0].date;
  sel.onchange = () => { curDate = sel.value; curStock = null; render(); };
  document.querySelectorAll(".tab").forEach(t => t.onclick = () => {
    document.querySelectorAll(".tab").forEach(x => x.classList.remove("active"));
    t.classList.add("active");
    curView = t.dataset.view;
    document.querySelectorAll(".view").forEach(v => v.classList.remove("active"));
    $(`#view-${curView}`).classList.add("active");
    render();
  });
  render();
}

function render() {
  if (curView === "market") renderMarket();
  else if (curView === "winrate") renderWinrate();
  else renderStock();
}

function dayInfo() { return INDEX.dates.find(d => d.date === curDate); }

/* ---------- 大盤放量訊號 ---------- */
async function renderMarket() {
  const box = $("#marketGrid");
  box.innerHTML = `<div class="loading">載入中…</div>`;
  let m;
  try { m = await loadData(`${curDate}/market`); }
  catch (e) { box.innerHTML = `<div class="loading">本日無大盤資料</div>`; $("#marketCards").innerHTML = ""; return; }
  const sig = m.signals || [];
  const s3 = sig.filter(r => (r["訊號強度"] || "").length >= 3).length;
  const up5 = sig.filter(r => num(r["漲跌幅%"]) >= 5).length;
  const mchg = sig.length ? sig[0]["大盤漲跌%"] : null;
  $("#marketCards").innerHTML = [
    ["放量檔數", fmtInt(sig.length)],
    ["★★★ 強烈", fmtInt(s3)],
    ["漲幅 ≥5%", fmtInt(up5)],
    ["大盤漲跌%", (mchg != null ? (num(mchg) >= 0 ? "+" : "") + fmt2(mchg) + "%" : "—")],
  ].map(c => `<div class="card"><div class="k">${c[0]}</div><div class="v">${c[1]}</div></div>`).join("");

  const cols = [
    {name: "代號", width: "78px"},
    {name: "名稱", width: "96px"},
    {name: "市場", width: "82px"},
    {name: "類型", width: "82px"},
    {name: "強度", width: "84px", formatter: c => gridjs.html(`<span class="star">${c || ""}</span>`)},
    {name: "當日量(張)", width: "110px", formatter: c => fmtInt(c)},
    {name: "漲跌幅%", width: "100px", formatter: c => { const v = num(c); return gridjs.html(`<span class="${v >= 0 ? "up" : "down"}">${v >= 0 ? "+" : ""}${fmt2(v)}%</span>`); }},
    {name: "收盤", width: "84px", formatter: c => fmt2(c)},
    {name: "量價關係", width: "124px"},
    {name: "×MA5", width: "86px", formatter: c => fmt1(c)},
    {name: "×MA20", width: "92px", formatter: c => fmt1(c)},
    {name: "訊號說明", width: "260px"},
  ];
  const rows = sig.map(r => [
    String(r["代號"] ?? ""), r["股票名稱"] ?? "", r["市場"] ?? "", r["訊號類型"] ?? "",
    r["訊號強度"] ?? "", num(r["當日量(張)"]), num(r["漲跌幅%"]), num(r["收盤價"]),
    r["量價關係"] ?? "", num(r["較MA5倍"]), num(r["較MA20倍"]), r["訊號說明"] ?? "",
  ]);
  // 用全新的容器節點重繪：Grid.js(Preact) 會沿用容器殘留的虛擬 DOM 樹，
  // 直接對同一節點重複 render 會讓新搜尋框的事件接不上（切換日期後搜尋失效）。
  const fresh = document.createElement("div");
  fresh.id = box.id;
  box.replaceWith(fresh);
  new gridjs.Grid({
    columns: cols, data: rows, search: true, sort: true,
    pagination: {limit: 25}, fixedHeader: true,
    language: {search: {placeholder: "搜尋代號 / 名稱…"}, pagination: {previous: "上一頁", next: "下一頁", showing: "顯示", to: "至", of: "共", results: "筆"}},
  }).render(fresh);
}

/* ---------- 勝率回測 ---------- */
async function renderWinrate() {
  const box = $("#wrTables");
  box.innerHTML = `<div class="loading">載入中…</div>`;
  let m;
  try { m = await loadData(`${curDate}/market`); }
  catch (e) { box.innerHTML = `<div class="loading">本日無資料</div>`; return; }
  const wr = m.winrate || [];
  // 圖表：星等分組的 D+5 / D+10 / D+15 勝率
  const star = wr.filter(r => r["分類"] === "星等");
  const labels = star.map(r => r["分組"]);
  const ds = [["D+5", "D+5_勝率%", "#4da3ff"], ["D+10", "D+10_勝率%", "#ffcb3d"], ["D+15", "D+15_勝率%", "#39c46e"]]
    .map(([lab, key, col]) => ({label: lab, data: star.map(r => num(r[key])), backgroundColor: col}));
  if (wrChart) wrChart.destroy();
  wrChart = new Chart($("#wrChart"), {
    type: "bar",
    data: {labels, datasets: ds},
    options: {responsive: true, plugins: {legend: {labels: {color: "#e6edf3"}}, title: {display: true, text: "各星等勝率 (%)", color: "#8b9bb0"}},
      scales: {x: {ticks: {color: "#e6edf3"}, grid: {color: "#2c3a4f"}}, y: {ticks: {color: "#8b9bb0"}, grid: {color: "#2c3a4f"}}}},
  });
  // 分組表格
  const groups = {};
  wr.forEach(r => { (groups[r["分類"]] ||= []).push(r); });
  let html = "";
  for (const [cat, recs] of Object.entries(groups)) {
    html += `<h3>${cat}</h3><table class="simple"><thead><tr>
      <th>分組</th><th>樣本數</th><th>D+5 勝率</th><th>D+5 均報酬</th><th>D+10 勝率</th><th>D+10 均報酬</th><th>D+15 勝率</th><th>D+15 均報酬</th>
      </tr></thead><tbody>`;
    recs.forEach(r => {
      const pct = (v, suf = "%") => v === null || v === undefined || v === "" ? "" : fmt1(v) + suf;
      const ret = v => { const n = num(v); return `<span class="${n >= 0 ? "up" : "down"}">${n >= 0 ? "+" : ""}${fmt2(n)}%</span>`; };
      html += `<tr><td>${r["分組"] ?? ""}</td><td>${fmtInt(r["樣本數"])}</td>
        <td>${pct(r["D+5_勝率%"])}</td><td>${ret(r["D+5_均報酬%"])}</td>
        <td>${pct(r["D+10_勝率%"])}</td><td>${ret(r["D+10_均報酬%"])}</td>
        <td>${pct(r["D+15_勝率%"])}</td><td>${ret(r["D+15_均報酬%"])}</td></tr>`;
    });
    html += `</tbody></table>`;
  }
  box.innerHTML = html || `<div class="loading">本日無勝率回測資料</div>`;
}

/* ---------- 個股分析 ---------- */
function renderStock() {
  const di = dayInfo();
  const list = $("#stockList");
  list.innerHTML = (di.stocks || []).map(s =>
    `<div class="stockchip${s.code === curStock ? " active" : ""}" data-code="${s.code}">${s.code} ${s.name || ""}</div>`).join("");
  list.querySelectorAll(".stockchip").forEach(c => c.onclick = () => { curStock = c.dataset.code; renderStock(); });
  if (!curStock) { $("#stockBody").innerHTML = `<div class="loading">請選擇上方個股</div>`; return; }
  loadStock(curStock);
}

async function loadStock(code) {
  const body = $("#stockBody");
  body.innerHTML = `<div class="loading">載入 ${code} …</div>`;
  let d;
  try { d = await loadData(`${curDate}/${code}`); }
  catch (e) { body.innerHTML = `<div class="loading">本日無 ${code} 資料</div>`; return; }
  let html = "";

  // 技術圖表：用 buy_top/sell_top/broker_detail 由 Chart.js 即時繪製（不再使用 PNG）
  if ((d.buy_top && d.buy_top.length) || (d.sell_top && d.sell_top.length)) {
    html += `<h3>技術圖表</h3><div class="broker-charts">` +
      [1, 2, 3, 4, 5, 6].map(i => `<div class="chartbox"><canvas id="bc${i}" height="150"></canvas></div>`).join("") + `</div>`;
  }

  // 買賣前20
  const topTable = (recs, title) => {
    if (!recs || !recs.length) return "";
    let t = `<table class="simple"><thead><tr><th>券商</th><th>買量(張)</th><th>買均價</th><th>賣量(張)</th><th>賣均價</th><th>買賣超(張)</th></tr></thead><tbody>`;
    recs.forEach(r => {
      const diff = num(r["buy_sell_diff"]);
      t += `<tr><td>${r["券商"] ?? ""}</td><td>${fmtInt(r["buy_total_qty"])}</td><td>${fmt2(r["buy_avg_price"])}</td>
        <td>${fmtInt(r["sell_total_qty"])}</td><td>${fmt2(r["sell_avg_price"])}</td>
        <td class="${diff >= 0 ? "up" : "down"}">${diff >= 0 ? "+" : ""}${fmtInt(diff)}</td></tr>`;
    });
    return `<h3>${title}</h3>` + t + `</tbody></table>`;
  };
  html += `<div class="two-col"><div>${topTable(d.buy_top, "買超前 20 大券商")}</div><div>${topTable(d.sell_top, "賣超前 20 大券商")}</div></div>`;

  // 各價位成交量
  if (d.price_volume && d.price_volume.length) {
    html += `<h3>各價位成交量分布</h3><div class="chartbox"><canvas id="pvChart" height="90"></canvas></div>`;
  }

  // 券商明細
  if (d.broker_detail && d.broker_detail.length) {
    html += `<h3>券商分點明細（共 ${fmtInt(d.broker_detail.length)} 筆，可搜尋券商）</h3><div id="detailGrid"></div>`;
  }
  body.innerHTML = html;

  // 價量圖
  if (d.price_volume && d.price_volume.length) {
    new Chart($("#pvChart"), {
      type: "bar",
      data: {labels: d.price_volume.map(r => fmt2(r["股價"])),
        datasets: [{label: "成交量(股)", data: d.price_volume.map(r => num(r["買進股數"])), backgroundColor: "#4da3ff"}]},
      options: {responsive: true, plugins: {legend: {labels: {color: "#e6edf3"}}},
        scales: {x: {ticks: {color: "#8b9bb0"}, grid: {color: "#2c3a4f"}}, y: {ticks: {color: "#8b9bb0"}, grid: {color: "#2c3a4f"}}}},
    });
  }

  // 技術圖表（Chart.js）
  renderBrokerCharts(d);

  // 明細表
  if (d.broker_detail && d.broker_detail.length) {
    const rows = d.broker_detail.map(r => [
      fmt2(r["股價"]), r["券商"] ?? "", num(r["買進股數"]), num(r["賣出股數"]),
      r["買進占比"] != null ? fmt2(r["買進占比"]) + "%" : "", r["賣出占比"] != null ? fmt2(r["賣出占比"]) + "%" : "",
    ]);
    new gridjs.Grid({
      columns: [{name: "股價"}, {name: "券商"}, {name: "買進股數", formatter: c => fmtInt(c)}, {name: "賣出股數", formatter: c => fmtInt(c)}, {name: "買進占比"}, {name: "賣出占比"}],
      data: rows, search: true, sort: true, pagination: {limit: 20}, fixedHeader: true,
      language: {search: {placeholder: "搜尋券商…"}, pagination: {previous: "上一頁", next: "下一頁", showing: "顯示", to: "至", of: "共", results: "筆"}},
    }).render($("#detailGrid"));
  }
}

/* ---------- 技術圖表（Chart.js 版・POC）----------
   6 張券商圖全部用 buy_top / sell_top / broker_detail 即時畫，不需要 PNG。 */
let brokerCharts = [];
function renderBrokerCharts(d) {
  if (typeof Chart === "undefined") return;
  brokerCharts.forEach(c => { try { c.destroy(); } catch (e) {} });
  brokerCharts = [];
  const C = {text: "#e6edf3", muted: "#8b9bb0", grid: "#2c3a4f", up: "#ff5d5d", down: "#39c46e",
    upA: "rgba(255,93,93,.55)", downA: "rgba(57,196,110,.55)", line: "#e6edf3"};
  const mk = (id, cfg) => { const el = $("#" + id); if (el) brokerCharts.push(new Chart(el, cfg)); };
  const xAxis = {ticks: {color: C.muted, maxRotation: 90, minRotation: 55, font: {size: 10}}, grid: {color: C.grid}};
  const dualOpts = title => ({
    responsive: true, interaction: {mode: "index", intersect: false},
    plugins: {legend: {labels: {color: C.text, boxWidth: 12, font: {size: 11}}}, title: {display: true, text: title, color: C.muted}},
    scales: {x: xAxis,
      y: {position: "left", ticks: {color: C.muted}, grid: {color: C.grid}, title: {display: true, text: "股數(張)", color: C.muted}},
      y1: {position: "right", ticks: {color: C.muted}, grid: {drawOnChartArea: false}, title: {display: true, text: "均價", color: C.muted}}},
  });
  const netOpts = title => ({
    responsive: true,
    plugins: {legend: {display: false}, title: {display: true, text: title, color: C.muted}},
    scales: {x: xAxis, y: {ticks: {color: C.muted}, grid: {color: C.grid}, title: {display: true, text: "買賣超(張)", color: C.muted}}},
  });
  const bar = (label, data, color, extra) => Object.assign({type: "bar", label, data, backgroundColor: color, yAxisID: "y", order: 2}, extra || {});
  // 均價線：金色加粗、order 較小 → 畫在長條最上層，避免被柱子蓋住
  const line = (label, data) => ({type: "line", label, data, borderColor: "#ffcb3d", backgroundColor: "#ffcb3d",
    borderWidth: 2.5, yAxisID: "y1", tension: 0, pointRadius: 2, pointBackgroundColor: "#ffcb3d", order: 1});
  const bt = d.buy_top || [], st = d.sell_top || [];

  if (bt.length) mk("bc1", {data: {labels: bt.map(r => r["券商"]),
    datasets: [bar("買進股數(張)", bt.map(r => num(r["buy_total_qty"])), C.up), line("均價", bt.map(r => num(r["buy_avg_price"])))]},
    options: dualOpts("買進股數前20名與均價")});
  if (st.length) mk("bc2", {data: {labels: st.map(r => r["券商"]),
    datasets: [bar("賣出股數(張)", st.map(r => num(r["sell_total_qty"])), C.down), line("均價", st.map(r => num(r["sell_avg_price"])))]},
    options: dualOpts("賣出股數前20名與均價")});
  if (bt.length) mk("bc3", {data: {labels: bt.map(r => r["券商"]),
    datasets: [bar("買進股數(張)", bt.map(r => num(r["buy_total_qty"])), C.upA), bar("賣出股數(張)", bt.map(r => num(r["sell_total_qty"])), C.downA), line("均價", bt.map(r => num(r["buy_avg_price"])))]},
    options: dualOpts("買進前20名：買量 vs 賣量")});
  if (st.length) mk("bc4", {data: {labels: st.map(r => r["券商"]),
    datasets: [bar("賣出股數(張)", st.map(r => num(r["sell_total_qty"])), C.downA), bar("買進股數(張)", st.map(r => num(r["buy_total_qty"])), C.upA), line("均價", st.map(r => num(r["sell_avg_price"])))]},
    options: dualOpts("賣出前20名：賣量 vs 買量")});

  // 買超 / 賣超：用 broker_detail 依券商加總淨買（股）→ 張，再取前/後 20
  const net = {};
  (d.broker_detail || []).forEach(r => { const b = r["券商"] || ""; net[b] = (net[b] || 0) + (num(r["買進股數"]) - num(r["賣出股數"])); });
  const arr = Object.entries(net).map(([b, v]) => [b.replace(/^[0-9A-Za-z]{3,4}/, "").trim() || b, v / 1000]);
  const buyTop = [...arr].sort((a, b) => b[1] - a[1]).slice(0, 20);
  const sellTop = [...arr].sort((a, b) => a[1] - b[1]).slice(0, 20);
  if (buyTop.length) mk("bc5", {type: "bar", data: {labels: buyTop.map(x => x[0]),
    datasets: [{label: "買超(張)", data: buyTop.map(x => x[1]), backgroundColor: C.up}]}, options: netOpts("買超前20名")});
  if (sellTop.length) mk("bc6", {type: "bar", data: {labels: sellTop.map(x => x[0]),
    datasets: [{label: "賣超(張)", data: sellTop.map(x => x[1]), backgroundColor: C.down}]}, options: netOpts("賣超前20名")});
}

init().catch(e => { document.querySelector("main").innerHTML = `<div class="loading">載入失敗：${e.message}<br>請確認 data 資料夾與 index.html 在一起</div>`; });
