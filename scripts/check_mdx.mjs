// Parses every .mdx page with the same MDX pipeline Mintlify uses and reports
// all syntax errors at once (mint's own checker stops at the first failure).
//
// Usage: node scripts/check_mdx.mjs
import { readdir, readFile } from "node:fs/promises";
import { join, relative } from "node:path";
import { compile } from "@mdx-js/mdx";
import remarkGfm from "remark-gfm";

const root = process.cwd();
const skip = new Set([".git", "node_modules", "images", "scripts"]);

async function walk(dir) {
  const out = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    if (entry.name.startsWith(".") || skip.has(entry.name)) continue;
    const full = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...(await walk(full)));
    else if (entry.name.endsWith(".mdx")) out.push(full);
  }
  return out;
}

const files = await walk(root);
let failures = 0;

for (const file of files) {
  const source = await readFile(file, "utf8");
  try {
    await compile(source, { remarkPlugins: [remarkGfm] });
  } catch (error) {
    failures += 1;
    const place = error.line ? `${error.line}:${error.column}` : "";
    console.log(`${relative(root, file)}:${place} ${error.reason ?? error.message}`);
  }
}

console.log(`\n${files.length} files, ${failures} with syntax errors`);
process.exit(failures ? 1 : 0);
