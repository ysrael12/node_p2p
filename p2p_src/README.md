# Atividade 01 - Transferência de Arquivos (Sistemas Distribuídos)

Comparação de 4 arquiteturas de transferência de arquivo: cliente-servidor
serial, concorrente, pool de N conexões, e P2P. Node.js + TypeScript, zero
dependência externa exceto `webtorrent` (único pacote npm do projeto).

## Setup

```bash
npm install
```

## Estrutura

```
src/
  common/        gerarArquivo.ts (buffer aleatório em memória), csv.ts (append de resultado)
  serial/        server.ts + client.ts — 1 cliente por vez (fila manual)
  concorrente/   server.ts + client.ts — todos ao mesmo tempo (event loop nativo)
  pool/          server.ts + client.ts — N conexões simultâneas (semáforo), excedente em fila
  p2p/           seed.ts (distribui) + peer.ts (baixa) — via webtorrent
  agregar.ts     lê resultados.csv, agrupa e calcula min/média/máx
```

Cada módulo não-trivial tem seu próprio `.test.ts` ao lado (sem framework,
`console.assert`): `serial/fila.test.ts`, `pool/fila.test.ts`,
`p2p/webtorrent.api.test.ts`, `common/*.test.ts`.

## Rodar um experimento manualmente

Cada arquitetura cliente-servidor segue o mesmo padrão: suba o servidor, rode
1+ clientes. Tamanho do arquivo é configurável via `TAMANHO_MB` (padrão 5).

```bash
# serial (porta 9001)
TAMANHO_MB=50 npx tsx src/serial/server.ts
TAMANHO_MB=50 npx tsx src/serial/client.ts 1   # em outro terminal
TAMANHO_MB=50 npx tsx src/serial/client.ts 2   # em outro terminal

# concorrente (porta 9002) e pool (porta 9003) seguem o mesmo padrão,
# troque "serial" pela pasta correspondente.
```

P2P não usa porta fixa (protocolo BitTorrent/DHT) — o `seed.ts` imprime um
magnet URI que o `peer.ts` recebe por argumento:

```bash
TAMANHO_MB=50 npx tsx src/p2p/seed.ts
# copia o magnetURI impresso, usa nos peers:
TAMANHO_MB=50 npx tsx src/p2p/peer.ts "magnet:?xt=..." 1
TAMANHO_MB=50 npx tsx src/p2p/peer.ts "magnet:?xt=..." 2
```

Cada cliente/peer grava uma linha em `resultados.csv`:
`arquitetura,tamanhoMB,cliente,duracaoMs`.

## Rodar todos os experimentos de uma vez

`rodar_experimentos.sh` automatiza as 3 arquiteturas cliente-servidor (sobe
servidor, roda 2 clientes, mata servidor) para 5/50/500MB. P2P é manual (ver
seção anterior) por precisar do magnet URI entre seed e peer.

```bash
bash rodar_experimentos.sh
```

> ponytail: script usa `taskkill //PID` pra matar o servidor pela porta real
> (Windows/git-bash não propaga `kill` pro processo node real via `npx`/`tsx`
> wrapper). Específico de Windows; em Linux/Mac um `kill $PID` simples basta.

## Agregar resultados

```bash
npx tsx src/agregar.ts resultados.csv
```

Imprime `arquitetura,tamanhoMB,minMs,mediaMs,maxMs` agrupado.

## Decisões de design

Ver `../DECISOES.md` (raiz do repositório) e o documento
`Diagramas de Arquitetura - Atividade 01 P2P.docx`, que também registra o
processo de implementação e os resultados reais dos experimentos.

## Por que `dynamic import` no P2P

`webtorrent@3.x` é ESM-only (`"type": "module"`); o resto do projeto é
CommonJS. Migrar tudo pra ESM só por essa dependência seria over-engineering —
`await import("webtorrent")` isolado em `seed.ts`/`peer.ts` resolve sem afetar
nenhum outro módulo.
