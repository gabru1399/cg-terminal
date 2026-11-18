// Parity harness: stdin JSON {sym, candles:[{t,o,h,l,c,v,tbb}]} → stdout {cards, ctx}.
// Runs the REAL production engine (src/lib/strategy/playbook.ts) — Node 24
// strips types natively (--experimental-strip-types is on by default since 23).
import { readFileSync } from "node:fs";
import { runPlaybook } from "../src/lib/strategy/playbook.ts";

const input = JSON.parse(readFileSync(0, "utf8"));
const { cards, ctx } = runPlaybook(input.candles, input.sym);
process.stdout.write(JSON.stringify({ cards, ctx }));
