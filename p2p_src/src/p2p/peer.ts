import { salvarResultado } from "../common/csv";

const MAGNET_URI = process.argv[2];
const CLIENTE_ID = Number(process.argv[3] || 1);
const TAMANHO_MB = 5;

if (!MAGNET_URI) {
  console.error("uso: peer.ts <magnetURI> <clienteId>");
  process.exit(1);
}

async function main() {
  const { default: WebTorrent } = await import("webtorrent");
  const client: any = new WebTorrent();

  const t0 = Date.now();
  client.add(MAGNET_URI, (torrent: any) => {
    torrent.on("done", () => {
      const duracaoMs = Date.now() - t0;
      salvarResultado("p2p", TAMANHO_MB, CLIENTE_ID, duracaoMs);
      console.log(`cliente ${CLIENTE_ID} terminou em ${duracaoMs}ms`);
      client.destroy(() => process.exit(0));
    });
  });
}

main();
