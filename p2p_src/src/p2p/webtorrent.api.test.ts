// Teste exploratório: confirma dynamic import funciona em CJS pro webtorrent (ESM-only)
import { gerarArquivo } from "../common/gerarArquivo";

async function main() {
  const { default: WebTorrent } = await import("webtorrent");

  const client: any = new WebTorrent();
  const buf: any = gerarArquivo(1); // 1MB pra teste rapido
  buf.name = "arquivo-teste.bin";

  client.seed(buf, (torrent: any) => {
    console.log("seed ok, magnetURI:", torrent.magnetURI.slice(0, 50) + "...");
    console.log("length:", torrent.length, "esperado:", 1 * 1024 * 1024);

    const client2: any = new WebTorrent();
    const t0 = Date.now();
    client2.add(torrent.magnetURI, (t2: any) => {
      t2.on("done", () => {
        const duracao = Date.now() - t0;
        console.log("download concluido em", duracao, "ms");
        console.log("bytes recebidos:", t2.length);
        console.assert(t2.length === 1 * 1024 * 1024, "tamanho incorreto");
        client2.destroy(() => client.destroy(() => process.exit(0)));
      });
    });
  });
}

main();

setTimeout(() => {
  console.log("TIMEOUT - 15s sem terminar");
  process.exit(1);
}, 15000);
