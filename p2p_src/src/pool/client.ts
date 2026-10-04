import { createConnection } from "net";
import { salvarResultado } from "../common/csv";

const PORTA = 9003;
const TAMANHO_MB = 5;
const CLIENTE_ID = Number(process.argv[2] || 1);

const inicio = Date.now();
const socket = createConnection(PORTA, "127.0.0.1");

socket.on("data", () => {}); // so queremos o tempo, dado é descartado

socket.on("end", () => {
    const duracaoMs = Date.now() - inicio;
    salvarResultado("pool", TAMANHO_MB, CLIENTE_ID, duracaoMs);
    console.log(`cliente ${CLIENTE_ID} terminou em ${duracaoMs}ms`);
});
