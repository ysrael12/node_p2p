import { readFileSync } from "fs";

interface Linha {
  arquitetura: string;
  tamanhoMB: number;
  cliente: number;
  duracaoMs: number;
}

function lerCsv(caminho: string): Linha[] {
  const texto = readFileSync(caminho, "utf-8").trim();
  if (!texto) return [];
  return texto.split("\n").map((linha) => {
    const [arquitetura, tamanhoMB, cliente, duracaoMs] = linha.split(",");
    return {
      arquitetura: arquitetura!,
      tamanhoMB: Number(tamanhoMB),
      cliente: Number(cliente),
      duracaoMs: Number(duracaoMs),
    };
  });
}

function agrupar(linhas: Linha[]): Map<string, number[]> {
  const grupos = new Map<string, number[]>();
  for (const linha of linhas) {
    const chave = `${linha.arquitetura},${linha.tamanhoMB}`;
    const tempos = grupos.get(chave) ?? [];
    tempos.push(linha.duracaoMs);
    grupos.set(chave, tempos);
  }
  return grupos;
}

function minMediaMax(tempos: number[]) {
  const min = tempos.reduce((a, b) => Math.min(a, b));
  const max = tempos.reduce((a, b) => Math.max(a, b));
  const media = tempos.reduce((a, b) => a + b, 0) / tempos.length;
  return { min, media, max };
}

function main() {
  const caminho = process.argv[2] || "resultados.csv";
  const linhas = lerCsv(caminho);
  const grupos = agrupar(linhas);

  console.log("arquitetura,tamanhoMB,minMs,mediaMs,maxMs");
  for (const [chave, tempos] of grupos) {
    const { min, media, max } = minMediaMax(tempos);
    console.log(`${chave},${min},${media.toFixed(1)},${max}`);
  }
}

main();
