import { createServer, Socket, createConnection } from "net";
import { gerarArquivo } from "../common/gerarArquivo";

const PORTA = 9093;
const TAMANHO_MB = 5;
const N = 2;

const fila: Socket[] = [];
let ativos = 0;

function atenderProximo() {
  if (ativos >= N || fila.length === 0) return;
  const socket = fila.shift()!;
  ativos++;
  const buffer = gerarArquivo(TAMANHO_MB);
  setTimeout(() => {
    socket.end(buffer, () => {
      ativos--;
      atenderProximo();
    });
  }, 300); // segura a conexão um pouco pra forçar a 3ª esperar
}

const servidor = createServer((socket) => {
  fila.push(socket);
  atenderProximo();
});

servidor.listen(PORTA, () => {
  const t0 = Date.now();
  const tempos: number[] = [];

  function cliente(id: number) {
    const sock = createConnection(PORTA, "127.0.0.1");
    let total = 0;
    sock.on("data", (d) => (total += d.length));
    sock.on("end", () => {
      tempos[id] = Date.now() - t0;
    });
  }

  cliente(1);
  cliente(2);
  cliente(3); // deve esperar vaga, so começa depois que 1 ou 2 libera

  setTimeout(() => {
    console.log("tempos:", tempos);
    // com N=2 e delay de 300ms, cliente 3 so termina depois dos 2 primeiros
    console.assert(tempos[3]! > tempos[1]!, "c3 deveria terminar depois de c1 (pool N=2 deveria enfileirar)");
    console.assert(tempos[3]! > tempos[2]!, "c3 deveria terminar depois de c2 (pool N=2 deveria enfileirar)");
    console.log("ok: pool N=2 enfileira o 3o cliente corretamente");
    servidor.close();
    process.exit(0);
  }, 2000);
});
