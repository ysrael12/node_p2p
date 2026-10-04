import { gerarArquivo } from "../common/gerarArquivo";

const TAMANHO_MB = 5;

async function main() {
  const { default: WebTorrent } = await import("webtorrent");
  const client: any = new WebTorrent();

  const buf: any = gerarArquivo(TAMANHO_MB);
  buf.name = "arquivo-teste.bin";

  client.seed(buf, (torrent: any) => {
    console.log("SEED rodando. magnetURI:");
    console.log(torrent.magnetURI);
  });
}

main();
