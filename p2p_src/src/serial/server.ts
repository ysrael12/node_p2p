import { createServer, Socket } from "net";
import { gerarArquivo } from "../common/gerarArquivo";

const PORTA = 9001;
const TAMANHO_MB = 5;

// fila manual: toda conexão entra aqui, mas só 1 é atendida por vez
const fila: Socket[] = [];
let ocupado = false;

function atenderProximo() {
    if (ocupado || fila.length === 0) return;
    const socket = fila.shift()!;
    ocupado = true;

    const buffer = gerarArquivo(TAMANHO_MB);
    socket.end(buffer, () => {
        ocupado = false;
        atenderProximo(); // libera e tenta atender o próximo da fila
    });
}

const servidor = createServer((socket) => {
    fila.push(socket);
    atenderProximo();
});

servidor.listen(PORTA, () => console.log(`servidor serial (um por vez) na porta ${PORTA}`));
