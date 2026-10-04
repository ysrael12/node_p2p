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

doc.save(OUT)
print(f"Salvo: {OUT}")
