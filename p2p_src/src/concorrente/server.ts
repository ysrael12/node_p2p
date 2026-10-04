   import { createServer } from "net";
   import { gerarArquivo } from "../common/gerarArquivo";

   const PORTA = 9002;
   const TAMANHO_MB = Number(process.env.TAMANHO_MB) || 5;

   const servidor = createServer((socket) => {
     const buffer = gerarArquivo(TAMANHO_MB);
     socket.end(buffer);
   });

   servidor.listen(PORTA, () => console.log(`servidor concorrente (todos de
 uma vez) na porta ${PORTA}`));