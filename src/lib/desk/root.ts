import { existsSync } from "node:fs";
import path from "node:path";

export function resolveDeskRoot(requireMt5Script = false): string {
  const cwd = process.cwd();
  const parent = path.dirname(cwd);
  const grandparent = path.dirname(parent);
  const candidates = path.basename(cwd) === "standalone" && path.basename(parent) === ".next"
    ? [grandparent, cwd, parent]
    : [cwd, parent, grandparent];
  const hasDesk = (dir: string) => existsSync(path.join(/* turbopackIgnore: true */ dir, "desk", "state.json"));
  if (requireMt5Script) {
    const withScript = candidates.find((dir) => hasDesk(dir) && existsSync(path.join(/* turbopackIgnore: true */ dir, "scripts", "mt5_punch.py")));
    if (withScript) return withScript;
  }
  return candidates.find(hasDesk) ?? cwd;
}
