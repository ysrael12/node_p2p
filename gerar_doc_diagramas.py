"""Gera documento Word com os 4 diagramas de arquitetura (UML em quadrados).

ponytail: script fonte única, roda de novo se os diagramas mudarem.
"""
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

DIAGRAMS = "diagrams"
OUT = "Diagramas de Arquitetura - Atividade 01 P2P.docx"

doc = Document()

title = doc.add_heading("Diagramas de Arquitetura - Transferência de Arquivos", level=0)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

p = doc.add_paragraph("Atividade 01 - Unidade 2 - Sistemas Distribuídos")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph(
    "Este documento registra os diagramas das quatro arquiteturas avaliadas na atividade: "
    "cliente-servidor serial, cliente-servidor com threads, cliente-servidor com pool de threads "
    "e P2P. Cada quadrado representa um processo ou máquina distinta na rede."
)

itens = [
    {
        "num": 1,
        "nome": "Cliente-Servidor Serial",
        "img": "01_cliente_servidor_serial.png",
        "desc": (
            "O servidor atende um único cliente por vez. Enquanto um download está em andamento, "
            "os demais clientes permanecem em fila aguardando a liberação da conexão. "
            "O tempo total de transferência cresce linearmente com o número de clientes "
            "(N clientes x tempo individual)."
        ),
    },
    {
        "num": 2,
        "nome": "Cliente-Servidor com Threads",
        "img": "02_cliente_servidor_threads.png",
        "desc": (
            "O servidor cria uma thread dedicada para cada cliente que se conecta, permitindo que "
            "todos os downloads ocorram em paralelo. O tempo total se aproxima do tempo de um único "
            "download, limitado pela largura de banda disponível no servidor. "
            "Desvantagem: consumo de memória cresce com o número de clientes simultâneos."
        ),
    },
    {
        "num": 3,
        "nome": "Cliente-Servidor com Pool de Threads",
        "img": "03_cliente_servidor_pool.png",
        "desc": (
            "O servidor mantém um número fixo de N threads (no exemplo, N = 2) que são reutilizadas "
            "entre os clientes. Quando todas as threads estão ocupadas, os clientes excedentes "
            "aguardam em fila até que uma thread seja liberada. O tempo total é aproximadamente "
            "ceil(clientes / N) x tempo individual, um equilíbrio entre a arquitetura serial e a "
            "de threads ilimitadas."
        ),
    },
    {
        "num": 4,
        "nome": "P2P (Peer-to-Peer)",
        "img": "04_p2p.png",
        "desc": (
            "Um peer inicial (seed) possui o arquivo completo e distribui pedaços (chunks) para os "
            "demais peers. Diferente das arquiteturas anteriores, todo peer que já recebeu algum "
            "pedaço do arquivo também pode retransmiti-lo para outros peers, distribuindo a carga "
            "de upload. Não há um gargalo único: o throughput tende a crescer conforme mais peers "
            "entram na rede."
        ),
    },
]

for item in itens:
    doc.add_heading(f"{item['num']}. {item['nome']}", level=1)
    doc.add_paragraph(item["desc"])
    doc.add_picture(f"{DIAGRAMS}/{item['img']}", width=Cm(14))
    cap = doc.add_paragraph(f"Figura {item['num']}: {item['nome']}.")
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.runs[0].italic = True
    cap.runs[0].font.size = Pt(10)

# --- Decisões de Implementação (fonte: DECISOES.md) ---
doc.add_page_break()
doc.add_heading("Decisões de Implementação", level=0)

doc.add_heading("Stack", level=1)
doc.add_paragraph(
    "Node.js + TypeScript, estilo KISS (menor dependência possível). "
    "Rede cliente-servidor: módulo net puro (TCP), sem framework HTTP. "
    "P2P: biblioteca webtorrent, único pacote npm externo do projeto."
)

doc.add_heading("Tamanhos de arquivo", level=1)
doc.add_paragraph(
    "5 MB, 50 MB, 500 MB, gerados em runtime (buffer aleatório em memória), "
    "sem salvar em disco."
)

doc.add_heading("Topologia dos experimentos", level=1)
doc.add_paragraph(
    "Todos os processos (servidor e clientes) rodam em localhost, mesma máquina, "
    "como processos separados."
)

doc.add_heading("Estrutura do projeto (monorepo)", level=1)
estrutura = doc.add_paragraph()
estrutura.add_run(
    "p2p/\n"
    "  app/\n"
    "    src/\n"
    "      common/        gerarArquivo.ts, csv.ts\n"
    "      serial/         server.ts, client.ts\n"
    "      concorrente/     server.ts, client.ts   (equivalente a \"threads\")\n"
    "      pool/            server.ts, client.ts\n"
    "      p2p/             seed.ts, peer.ts\n"
    "    resultados.csv"
).font.name = "Consolas"

doc.add_heading("Diferença das 3 variações cliente-servidor em Node", level=1)
doc.add_paragraph(
    "Node é single-thread com event loop não-bloqueante, diferente do modelo de threads "
    "do Python/Java. Equivalência adotada:"
)
doc.add_paragraph(
    "Serial: servidor só aceita a próxima conexão depois que a anterior terminar o "
    "download completo (fila manual, bloqueio intencional).", style="List Bullet"
)
doc.add_paragraph(
    "Concorrente (todos de uma vez): comportamento padrão do net.createServer, aceita "
    "todas as conexões simultaneamente. Não usa worker_threads (seria over-engineering "
    "para I/O puro); o paralelismo real vem da natureza assíncrona do event loop.", style="List Bullet"
)
doc.add_paragraph(
    "Pool N: limite de conexões ativas simultâneas via semáforo simples (contador); "
    "excedente espera em fila até uma vaga liberar.", style="List Bullet"
)

doc.add_heading("Métrica", level=1)
doc.add_paragraph(
    "Tempo medido no cliente: do connect até o fim do download (EOF/stream completo). "
    "Resultado salvo em CSV (append), sem biblioteca extra."
)

doc.add_heading("Clientes por teste", level=1)
doc.add_paragraph("2 clientes por experimento (arquitetura x tamanho).")

doc.add_heading("Formato do CSV", level=1)
doc.add_paragraph("Colunas, sem header repetido (append puro):")
csv_fmt = doc.add_paragraph()
csv_fmt.add_run("arquitetura,tamanhoMB,cliente,duracaoMs").font.name = "Consolas"
doc.add_paragraph("Exemplo:")
csv_ex = doc.add_paragraph()
csv_ex.add_run("serial,5,1,842\nserial,5,2,1690").font.name = "Consolas"

doc.add_heading("Script de agregação", level=1)
doc.add_paragraph(
    "agregar.ts: lê o CSV, agrupa por arquitetura+tamanhoMB, calcula min/média/máx "
    "com reduce puro (sem lib), imprime tabela no console."
)

# --- Registro do Processo de Implementação ---
doc.add_page_break()
doc.add_heading("Registro do Processo de Implementação", level=0)
doc.add_paragraph(
    "Ordem real de desenvolvimento, com as decisões técnicas tomadas a partir de testes "
    "práticos (não suposições). Cada módulo foi escrito, compilado (tsc --noEmit) e testado "
    "de ponta a ponta antes de seguir para o próximo."
)

doc.add_heading("1. Módulos comuns", level=1)
doc.add_paragraph(
    "gerarArquivo.ts (buffer aleatório em memória via crypto.randomBytes) e csv.ts "
    "(append de resultado) implementados e testados primeiro, por serem usados por "
    "todas as arquiteturas.", style="List Bullet"
)

doc.add_heading("2. Arquitetura Serial", level=1)
doc.add_paragraph(
    "Primeira versão usou servidor.maxConnections = 1. Teste prático revelou que essa opção "
    "RECUSA a conexão excedente (destroy imediato, sem erro explícito) em vez de enfileirar — "
    "o cliente 2 seria desconectado sem receber dado, incompatível com medir \"tempo até o "
    "fim do download\". Confirmado via teste isolado com net.createConnection antes de decidir.",
    style="List Bullet"
)
doc.add_paragraph(
    "Solução adotada: fila manual (array de sockets) com flag ocupado. socket.end(buffer, "
    "callback) — o callback só dispara quando o envio termina de fato, garantindo atendimento "
    "verdadeiramente serial. Testado com 2 clientes reais: segundo cliente só recebeu dado "
    "após o primeiro terminar.", style="List Bullet"
)

doc.add_heading("3. Arquitetura Concorrente", level=1)
doc.add_paragraph(
    "Mesma base do serial, sem fila e sem limite — o event loop do Node já atende todas as "
    "conexões em paralelo nativamente. Testado com 2 clientes: ambos terminaram quase juntos "
    "(tempos próximos), confirmando paralelismo real (diferente do serial).", style="List Bullet"
)

doc.add_heading("4. Arquitetura Pool (N)", level=1)
doc.add_paragraph(
    "Combina fila (serial) com paralelismo limitado (concorrente): contador de conexões "
    "ativas (semáforo simples) em vez de flag booleana. Com N = 2, testado com 3 clientes "
    "simultâneos (teste dedicado com delay artificial no servidor): os 2 primeiros foram "
    "atendidos em paralelo, o 3º esperou uma vaga liberar antes de começar — comportamento "
    "de pool confirmado na prática, não apenas por leitura do código.", style="List Bullet"
)

doc.add_heading("5. Arquitetura P2P", level=1)
doc.add_paragraph(
    "Antes de escrever código, a API real da lib webtorrent foi inspecionada "
    "(README, index.d.ts de @types/webtorrent, código-fonte de index.js) em vez de assumida. "
    "Descoberta de um problema de compatibilidade real: webtorrent 3.x é um pacote ESM puro "
    "(\"type\": \"module\"), enquanto o projeto é CommonJS — import direto falhava com "
    "ERR_PACKAGE_PATH_NOT_EXPORTED ao rodar via tsx.", style="List Bullet"
)
doc.add_paragraph(
    "Solução adotada: dynamic import (await import(\"webtorrent\")) isolado dentro das "
    "funções async de seed.ts e peer.ts, em vez de migrar o projeto inteiro para ESM. "
    "Resolve a incompatibilidade sem afetar os módulos common/serial/concorrente/pool, que "
    "continuam em CommonJS com require(). Confirmado com teste exploratório (seed + 2 peers "
    "locais) antes de integrar à medição de tempo e ao CSV.", style="List Bullet"
)

doc.add_heading("6. Script de Agregação", level=1)
doc.add_paragraph(
    "agregar.ts testado com CSV sintético de valores conhecidos (ex.: 100 e 200 → média "
    "esperada 150) antes de ser usado nos dados reais dos experimentos, confirmando o "
    "agrupamento por arquitetura+tamanho e o cálculo de min/média/máx.", style="List Bullet"
)

doc.add_heading("Controle de versão", level=1)
doc.add_paragraph(
    "Projeto versionado em Git com commits separados por módulo/decisão (setup, cada "
    "arquitetura, dependência webtorrent, script de agregação), preservando o histórico "
    "do processo de construção."
)

# --- Resultados dos Experimentos ---
doc.add_page_break()
doc.add_heading("Resultados dos Experimentos", level=0)
doc.add_paragraph(
    "Execução real das 4 arquiteturas, 3 tamanhos de arquivo (5, 50, 500 MB), 2 clientes "
    "por experimento, em localhost. Tempo medido no cliente: do connect/add até o fim do "
    "download. Valores em milissegundos (ms)."
)

resultados = [
    ("serial", 5, 25, 29.5, 34),
    ("serial", 50, 320, 346.0, 372),
    ("serial", 500, 1919, 2078.0, 2237),
    ("concorrente", 5, 20, 32.5, 45),
    ("concorrente", 50, 169, 182.0, 195),
    ("concorrente", 500, 1525, 1769.5, 2014),
    ("pool", 5, 19, 26.0, 33),
    ("pool", 50, 183, 204.0, 225),
    ("pool", 500, 1965, 2176.5, 2388),
    ("p2p", 5, 312, 312.0, 312),
    ("p2p", 50, 376, 376.5, 377),
    ("p2p", 500, 1343, 1359.0, 1375),
]

tabela = doc.add_table(rows=1, cols=5)
tabela.style = "Light Grid Accent 1"
hdr = tabela.rows[0].cells
hdr[0].text = "Arquitetura"
hdr[1].text = "Tamanho (MB)"
hdr[2].text = "Min (ms)"
hdr[3].text = "Média (ms)"
hdr[4].text = "Máx (ms)"

for arq, mb, minimo, media, maximo in resultados:
    row = tabela.add_row().cells
    row[0].text = arq
    row[1].text = str(mb)
    row[2].text = str(minimo)
    row[3].text = str(media)
    row[4].text = str(maximo)

doc.add_paragraph()
doc.add_heading("Observações sobre os resultados", level=1)
doc.add_paragraph(
    "Com apenas 2 clientes por teste, serial/concorrente/pool apresentam tempos próximos: "
    "a vantagem do paralelismo (concorrente/pool) sobre o serial só fica evidente com mais "
    "clientes simultâneos disputando o servidor (com 2 clientes e pool N=2, o pool se comporta "
    "igual ao concorrente, como esperado e já observado nos testes unitários).", style="List Bullet"
)
doc.add_paragraph(
    "O P2P tem um custo fixo de inicialização (handshake de protocolo, descoberta de peer) que "
    "domina o tempo em arquivos pequenos (312ms para 5MB, mais lento que as demais arquiteturas "
    "nesse tamanho). Em arquivos maiores esse custo fixo se dilui: 500MB em P2P (1359ms média) "
    "foi mais rápido que serial (2078ms) e pool (2176ms), e competitivo com concorrente (1769ms), "
    "mesmo rodando como dois peers locais sem benefício real de distribuição de carga de upload.",
    style="List Bullet"
)
doc.add_paragraph(
    "Todos os experimentos rodaram em localhost (mesma máquina), portanto os tempos refletem "
    "overhead de protocolo e processamento, não latência de rede real.", style="List Bullet"
)

doc.add_heading("Dados brutos", level=1)
doc.add_paragraph(
    "CSV completo (24 linhas: 4 arquiteturas x 3 tamanhos x 2 clientes) disponível em "
    "p2p_src/resultados_experimento_final.csv, gerado pelo script rodar_experimentos.sh e "
    "agregado por agregar.ts."
)

doc.save(OUT)
print(f"Salvo: {OUT}")
