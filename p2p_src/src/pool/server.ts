import { createServer, Socket } from "net";
import { gerarArquivo } from "../common/gerarArquivo";

const PORTA = 9003;
const TAMANHO_MB = Number(process.env.TAMANHO_MB) || 5;
const N = 2; // tamanho do pool: max de conexões ativas simultâneas

const fila: Socket[] = [];
let ativos = 0;

function atenderProximo() {
    if (ativos >= N || fila.length === 0) return;
    const socket = fila.shift()!;
    ativos++;

    const buffer = gerarArquivo(TAMANHO_MB);
    socket.end(buffer, () => {
        ativos--;
        atenderProximo(); // libera vaga, tenta atender o próximo da fila
    });
}

const servidor = createServer((socket) => {
    fila.push(socket);
    atenderProximo();
});

servidor.listen(PORTA, () => console.log(`servidor pool (N=${N}) na porta ${PORTA}`));
