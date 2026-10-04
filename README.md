# Atividade 02 — Transferência de Arquivos (Sistemas Distribuídos)

Comparação de 4 arquiteturas de transferência de arquivo — cliente-servidor
serial, concorrente, pool de N conexões, e P2P — medindo tempo min/médio/máx
em 3 tamanhos de arquivo (5MB, 50MB, 500MB).

Código-fonte em [`p2p_src/`](p2p_src/) (Node.js + TypeScript). Ver
[`p2p_src/README.md`](p2p_src/README.md) para setup e comandos.

## 1. Cliente-Servidor Serial

Servidor atende **um cliente por vez**; os demais esperam em fila. Tempo
total cresce linearmente com o número de clientes.

```mermaid
sequenceDiagram
    participant C1 as Cliente 1
    participant C2 as Cliente 2
    participant S as Servidor (fila manual)

    C1->>S: conecta
    C2->>S: conecta (entra na fila)
    S->>C1: envia arquivo completo
    Note over C2: espera na fila
    S->>C2: envia arquivo completo (só após C1 terminar)
```

## 2. Cliente-Servidor Concorrente

Servidor atende **todos ao mesmo tempo**, sem fila. Em Node.js isso vem
nativo do event loop assíncrono (sem threads reais).

```mermaid
sequenceDiagram
    participant C1 as Cliente 1
    participant C2 as Cliente 2
    participant S as Servidor

    C1->>S: conecta
    C2->>S: conecta
    par Envio paralelo
        S->>C1: envia arquivo completo
    and
        S->>C2: envia arquivo completo
    end
```

## 3. Cliente-Servidor Pool (N)

Servidor mantém **N conexões ativas simultâneas** (semáforo); excedente
espera em fila até uma vaga liberar.

```mermaid
sequenceDiagram
    participant C1 as Cliente 1
    participant C2 as Cliente 2
    participant C3 as Cliente 3
    participant S as Servidor (pool N=2)

    C1->>S: conecta (vaga 1/2)
    C2->>S: conecta (vaga 2/2)
    C3->>S: conecta (fila, pool cheio)
    par Até N em paralelo
        S->>C1: envia arquivo
    and
        S->>C2: envia arquivo
    end
    Note over C3: espera vaga liberar
    S->>C3: envia arquivo (após C1 ou C2 terminar)
```

## 4. P2P (webtorrent)

Um peer inicial (seed) distribui pedaços do arquivo; peers que já têm algum
pedaço também retransmitem para outros.

```mermaid
graph LR
    Seed["Seed<br/>(arquivo completo)"] -->|chunks| P1["Peer 1"]
    Seed -->|chunks| P2["Peer 2"]
    P1 <-->|chunks| P2
```

## Resultados (localhost, 2 clientes por teste, tempo médio em ms)

| Arquitetura | 5MB | 50MB | 500MB |
|---|---|---|---|
| serial | 29.5 | 346.0 | 2078.0 |
| concorrente | 32.5 | 182.0 | 1769.5 |
| pool (N=2) | 26.0 | 204.0 | 2176.5 |
| p2p | 312.0 | 376.5 | **1359.0** |

P2P tem overhead de protocolo alto em arquivo pequeno (mais lento em 5MB),
mas vira a arquitetura mais rápida das quatro em 500MB — o custo fixo se
dilui conforme o arquivo cresce. Dados brutos completos em
[`p2p_src/resultados_experimento_final.csv`](p2p_src/resultados_experimento_final.csv).

## Decisões de design

Ver [`DECISOES.md`](DECISOES.md) — stack, métrica, formato do CSV, e por que
cada arquitetura foi implementada da forma que foi (ex.: por que serial usa
fila manual em vez de `maxConnections`, por que P2P usa dynamic import).
