import fs from "node:fs";
import path from "node:path";

const rootDir = path.resolve(process.cwd());
const docsDir = path.join(rootDir, "docs");
const abCsvPath = path.join(docsDir, "seo-title-ab.csv");
const perfCsvPath = path.join(docsDir, "seo-title-performance.csv");

function parseCsvLine(line) {
  const result = [];
  let current = "";
  let inQuotes = false;
  for (let i = 0; i < line.length; i += 1) {
    const char = line[i];
    if (char === '"') {
      if (inQuotes && line[i + 1] === '"') {
        current += '"';
        i += 1;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (char === "," && !inQuotes) {
      result.push(current);
      current = "";
    } else {
      current += char;
    }
  }
  result.push(current);
  return result;
}

function parseCsv(content) {
  const lines = content
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);
  if (lines.length < 2) return [];
  const headers = parseCsvLine(lines[0]);
  return lines.slice(1).map((line) => {
    const values = parseCsvLine(line);
    const row = {};
    headers.forEach((header, idx) => {
      row[header] = values[idx] ?? "";
    });
    return row;
  });
}

function toNumber(v) {
  const n = Number(v);
  return Number.isFinite(n) ? n : 0;
}

function chooseWinner(row, perfMap) {
  const perf = perfMap.get(row.url);
  if (!perf) {
    return row.applied_variant === "B" ? "B" : "A";
  }

  const ctrA = toNumber(perf.ctr_a);
  const ctrB = toNumber(perf.ctr_b);
  const clicksA = toNumber(perf.clicks_a);
  const clicksB = toNumber(perf.clicks_b);

  if (ctrA > ctrB) return "A";
  if (ctrB > ctrA) return "B";
  if (clicksA > clicksB) return "A";
  if (clicksB > clicksA) return "B";
  return row.applied_variant === "B" ? "B" : "A";
}

function updateTagContent(html, tag, text) {
  const regex = new RegExp(`<${tag}>[\\s\\S]*?<\\/${tag}>`, "i");
  return html.replace(regex, `<${tag}>${text}</${tag}>`);
}

function updateMetaProperty(html, property, text) {
  const regex = new RegExp(`(<meta\\s+property="${property}"\\s+content=")([^"]*)("\\s*\\/?>)`, "i");
  return html.replace(regex, `$1${text}$3`);
}

function urlToFilePath(url) {
  const normalized = url.replace(/^https?:\/\/[^/]+/i, "");
  const rel = normalized.endsWith("/") ? normalized : `${normalized}/`;
  return path.join(docsDir, rel, "index.html");
}

function run() {
  if (!fs.existsSync(abCsvPath)) {
    console.error("Missing docs/seo-title-ab.csv. Run generate:seo1000 first.");
    process.exit(1);
  }

  const abRows = parseCsv(fs.readFileSync(abCsvPath, "utf8"));
  const perfRows = fs.existsSync(perfCsvPath) ? parseCsv(fs.readFileSync(perfCsvPath, "utf8")) : [];
  const perfMap = new Map(perfRows.map((row) => [row.url, row]));

  let updatedCount = 0;
  const outputRows = ["url,title_a,title_b,applied_variant,applied_title,winner_variant,winner_title"];

  for (const row of abRows) {
    const winner = chooseWinner(row, perfMap);
    const winnerTitle = winner === "B" ? row.title_b : row.title_a;
    const filePath = urlToFilePath(row.url);

    if (!fs.existsSync(filePath)) {
      continue;
    }

    let html = fs.readFileSync(filePath, "utf8");
    html = updateTagContent(html, "title", winnerTitle);
    html = updateMetaProperty(html, "og:title", winnerTitle);
    fs.writeFileSync(filePath, html, "utf8");
    updatedCount += 1;

    const csvSafe = (v) => `"${String(v ?? "").replaceAll("\"", "\"\"")}"`;
    outputRows.push(
      [row.url, row.title_a, row.title_b, row.applied_variant, row.applied_title, winner, winnerTitle]
        .map(csvSafe)
        .join(",")
    );
  }

  fs.writeFileSync(path.join(docsDir, "seo-title-ab-result.csv"), `${outputRows.join("\n")}\n`, "utf8");

  console.log(`A/B rows loaded: ${abRows.length}`);
  console.log(`Performance rows loaded: ${perfRows.length}`);
  console.log(`Winner titles applied: ${updatedCount}`);
  console.log("Output: docs/seo-title-ab-result.csv");
}

run();
