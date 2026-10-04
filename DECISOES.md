# Decisões de Implementação — Atividade 01 P2P

## Stack

- **Node.js + TypeScript**, estilo KISS (menor dependência possível).
- Rede cliente-servidor: módulo `net` puro (TCP), sem framework HTTP.
- P2P: biblioteca `webtorrent` (único pacote npm externo do projeto).

## Tamanhos de arquivo

5 MB, 50 MB, 500 MB — gerados em runtime (buffer aleatório em memória), sem salvar em disco.

## Topologia dos experimentos

Todos os processos (servidor e clientes) rodam em **localhost**, mesma máquina, como processos separados.

## Estrutura do projeto (monorepo)

```
p2p/
  app/
    src/
      common/        gerarArquivo.ts, csv.ts
      serial/         server.ts, client.ts
      concorrente/     server.ts, client.ts   (equivalente a "threads")
      pool/            server.ts, client.ts
      p2p/             seed.ts, peer.ts
    resultados.csv
```

## Diferença das 3 variações cliente-servidor em Node

Node é single-thread + event loop não-bloqueante (diferente do modelo de threads do Python/Java).
Equivalência adotada:

- **Serial**: servidor só aceita a próxima conexão depois que a anterior terminar o download completo (fila manual, bloqueio intencional).
- **Concorrente ("todos de uma vez")**: comportamento padrão do `net.createServer`, aceita todas as conexões simultaneamente. Não usa `worker_threads` (seria over-engineering para I/O puro); o paralelismo real vem da natureza assíncrona do event loop.
- **Pool N**: limite de conexões **ativas** simultâneas via semáforo simples (contador); excedente espera em fila até uma vaga liberar.

## Métrica

Tempo medido **no cliente**: do `connect` até o fim do download (EOF/stream completo).
Resultado salvo em **CSV** (append), sem biblioteca extra.

## Clientes por teste

**2 clientes** por experimento (arquitetura x tamanho).

## Formato do CSV

Colunas, sem header repetido (append puro):

```
arquitetura,tamanhoMB,cliente,duracaoMs
```

Exemplo:

```
serial,5,1,842
serial,5,2,1690
```

## Script de agregação

`agregar.ts`: lê o CSV, agrupa por `arquitetura+tamanhoMB`, calcula min/média/máx com `reduce` puro (sem lib), imprime tabela no console.
