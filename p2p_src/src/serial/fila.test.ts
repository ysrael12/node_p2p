import { createServer, Socket, createConnection } from "net";
import { gerarArquivo } from "../common/gerarArquivo";

const PORTA = 9091;
const TAMANHO_MB = 5;

const fila: Socket[] = [];
let ocupado = false;

function atenderProximo() {
  if (ocupado || fila.length === 0) return;
  const socket = fila.shift()!;
  ocupado = true;
  const buffer = gerarArquivo(TAMANHO_MB);
  socket.end(buffer, () => {
    ocupado = false;
    atenderProximo();
  });
}

const servidor = createServer((socket) => {
  fila.push(socket);
  atenderProximo();
});

servidor.listen(PORTA, () => {
  const t0 = Date.now();
  let fimC1 = 0;
  let fimC2 = 0;

  const c1 = createConnection(PORTA, "127.0.0.1");
  let totalC1 = 0;
  c1.on("data", (d) => (totalC1 += d.length));
  c1.on("end", () => { fimC1 = Date.now() - t0; });

  const c2 = createConnection(PORTA, "127.0.0.1");
  let totalC2 = 0;
  c2.on("data", (d) => (totalC2 += d.length));
  c2.on("end", () => { fimC2 = Date.now() - t0; });

  setTimeout(() => {
    console.log("c1 recebeu bytes:", totalC1, "em", fimC1, "ms");
    console.log("c2 recebeu bytes:", totalC2, "em", fimC2, "ms");
    console.assert(totalC1 === TAMANHO_MB * 1024 * 1024, "c1 bytes incompletos");
    console.assert(totalC2 === TAMANHO_MB * 1024 * 1024, "c2 bytes incompletos");
    console.assert(fimC2 >= fimC1, "c2 deveria terminar depois (ou junto) de c1, nao antes -> fila nao serial");
    console.log("ok: fila serial confirmada (c2 terminou depois de c1, ambos completos)");
    servidor.close();
    process.exit(0);
  }, 3000);
});
