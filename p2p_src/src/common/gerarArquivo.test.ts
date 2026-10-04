import { gerarArquivo } from "./gerarArquivo";

const buf = gerarArquivo(5);
const esperado = 5 * 1024 * 1024;
console.assert(buf.length === esperado, `esperado ${esperado}, veio ${buf.length}`);
console.log("ok:", buf.length, "bytes");
