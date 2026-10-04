import { salvarResultado } from "./csv";
import { readFileSync, unlinkSync, existsSync } from "fs";

if (existsSync("resultados.csv")) unlinkSync("resultados.csv");

salvarResultado("serial", 5, 1, 842);
salvarResultado("serial", 5, 2, 1690);

const conteudo = readFileSync("resultados.csv", "utf-8");
const esperado = "serial,5,1,842\nserial,5,2,1690\n";
console.assert(conteudo === esperado, `esperado ${JSON.stringify(esperado)}, veio ${JSON.stringify(conteudo)}`);
console.log("ok:", JSON.stringify(conteudo));
