// Copies the entry image to the output directory.
//
// The image is the repository's own entry.png (a 1024x1024 PNG summing up
// 18 November 2026's world news). The program writes the same bytes on
// every run: it only copies the file, never re-renders it.
import { copyFileSync, readFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dst = join(outDir, "entry.png");

const bytes = readFileSync(src);
const magic = bytes.subarray(0, 8);
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!magic.equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a PNG file (bad magic bytes)");
}
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
const written = readFileSync(dst);
if (!written.equals(bytes)) {
  throw new Error("copied entry.png does not match the source bytes");
}
console.log(`wrote ${dst} (${written.length} bytes, verified identical)`);
