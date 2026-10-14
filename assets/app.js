"use strict";
const $ = (id) => document.getElementById(id);
const basisLabel = {
  bonus: "Bonus funds",
  deposit_plus_bonus: "Deposit + bonus",
  deposit: "Deposit only",
  unspecified: "Basis not specified"
};
function cell(label, value) {
  const td = document.createElement("td");
  td.dataset.label = label;
  td.textContent = String(value ?? "Not stated");
  return td;
}
function renderRow(item) {
  const tr = document.createElement("tr");
  const casino = cell("Casino", item.casino);
  casino.className = "casino-name";
  tr.append(casino);
  const bonus = cell("Welcome bonus", item.welcome_bonus);
  bonus.className = "bonus-copy";
  tr.append(bonus);
  const wager = document.createElement("td");
  wager.dataset.label = "Wagering";
  const chip = document.createElement("span");
  chip.className = "wager-chip";
  chip.textContent = String(item.wagering_multiplier) + "x";
  wager.append(chip);
  const detail = document.createElement("div");
  detail.className = "wager-detail";
  detail.textContent = basisLabel[item.wagering_basis] || "Basis not stated";
  wager.append(detail);
  tr.append(wager);
  tr.append(cell("Minimum deposit", item.minimum_deposit));
  const linkCell = document.createElement("td");
  linkCell.dataset.label = "Source";
  const link = document.createElement("a");
  if (typeof item.source_url === "string" && item.source_url.startsWith("https://betproof.co.za/")) {
    link.href = item.source_url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = "Source ↗";
    link.className = "source-link";
    linkCell.append(link);
  } else {
    linkCell.textContent = "Source unavailable";
  }
  tr.append(linkCell);
  return tr;
}
let allItems = [];
function renderFiltered() {
  const query = document.getElementById("search").value.trim().toLowerCase();
  const sort = document.getElementById("sort").value;
  const shown = allItems.filter(row => row.casino.toLowerCase().includes(query) || row.welcome_bonus.toLowerCase().includes(query));
  if (sort === "name") shown.sort((a,b)=>a.casino.localeCompare(b.casino));
  if (sort === "wager_asc") shown.sort((a,b)=>a.wagering_multiplier-b.wagering_multiplier);
  if (sort === "wager_desc") shown.sort((a,b)=>b.wagering_multiplier-a.wagering_multiplier);
  if (sort === "deposit_asc") shown.sort((a,b)=>Number(a.minimum_deposit.replace(/[^0-9.]/g,""))-Number(b.minimum_deposit.replace(/[^0-9.]/g,"")));
  const tbody = document.getElementById("bonus-rows");
  tbody.replaceChildren(...shown.map(renderRow));
  if (!shown.length) {
    const tr = document.createElement("tr"), td = document.createElement("td");
    td.colSpan = 5; td.className = "empty";
    td.textContent = allItems.length ? "No casino offers match this search." : "No verified offers yet. Run the scraper to populate the table.";
    tr.append(td); tbody.append(tr);
  }
  document.getElementById("rows-label").textContent = shown.length + " of " + allItems.length + " records";
}
async function loadBonuses() {
  const tbody = $("bonus-rows");
  try {
    const response = await fetch("./data/bonuses.json?v=" + Date.now(), {cache: "no-store"});
    if (!response.ok) throw new Error("HTTP " + response.status);
    const data = await response.json();
    if (!Array.isArray(data.casinos) || (data.status === "live_scrape" && data.casinos.length !== 3)) {
      throw new Error("Expected three entries in bonuses.json");
    }
    allItems = data.casinos;
    renderFiltered();
    $("casino-count").textContent = data.casinos.length;
    $("rows-label").textContent = data.casinos.length + " records";
    const live = data.status === "live_scrape" && data.casinos.length === 3 && !!data.generated_at;
    $("data-status").textContent = live ? "● Verified scraper output" : "◌ Awaiting verified scrape";
    $("data-status").className = live ? "status status-live" : "status status-preview";
    $("data-timestamp").textContent = live && data.generated_at
      ? "Scraped " + new Date(data.generated_at).toLocaleString(undefined, {dateStyle:"medium",timeStyle:"short"})
      : "Data will appear here after a verified AI-assisted scraping run.";
  } catch (error) {
    allItems = [];
    tbody.replaceChildren();
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 5;
    td.className = "empty";
    td.textContent = "Data unavailable. Run python -m scraper.scrape and serve this folder over HTTP.";
    tr.append(td);
    tbody.append(tr);
    $("data-status").textContent = "Data unavailable";
    $("rows-label").textContent = "0 records";
    console.error("Unable to load bonus data", error);
  }
}
$("search").addEventListener("input", renderFiltered);
$("sort").addEventListener("change", renderFiltered);
$("reload-data").addEventListener("click", loadBonuses);
loadBonuses();
