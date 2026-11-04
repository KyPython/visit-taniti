import assert from "node:assert/strict";
import test from "node:test";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Traceability: TAN-1.1. Coral text and button pairs must meet WCAG 2.2 AA
// (4.5:1) against their backgrounds.

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const css = readFileSync(join(ROOT, "styles.css"), "utf8");

function varColor(name) {
  const match = css.match(new RegExp(`${name}:\\s*(#[0-9a-fA-F]{6})`));
  assert.ok(match, `expected ${name} in :root`);
  return match[1];
}

function luminance(hex) {
  const rgb = [1, 3, 5].map((i) => {
    const channel = parseInt(hex.slice(i, i + 2), 16) / 255;
    return channel <= 0.03928
      ? channel / 12.92
      : Math.pow((channel + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
}

function ratio(fg, bg) {
  const [lighter, darker] = [luminance(fg), luminance(bg)].sort((a, b) => b - a);
  return (lighter + 0.05) / (darker + 0.05);
}

test("button text pairs meet AA", () => {
  const coral = varColor("--coral");
  const hover = varColor("--coral-hover");
  assert.ok(ratio("#ffffff", coral) >= 4.5, `white on ${coral}`);
  assert.ok(ratio("#ffffff", hover) >= 4.5, `white on ${hover}`);
});

test("coral text meets AA on page backgrounds", () => {
  const coral = varColor("--coral");
  const sand = varColor("--sand");
  assert.ok(ratio(coral, sand) >= 4.5, `${coral} on ${sand}`);
  assert.ok(ratio(coral, "#ffffff") >= 4.5, `${coral} on white`);
});
