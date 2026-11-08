# Acompanhamento Semanal de Metas - Canal Código Social

## Marcos Oficiais (Sprint de 7 dias + Plano de 12 Semanas)
Acompanhar semanalmente com os dados reais exportados do YouTube Studio.
Objetivo: Candidatura ao YPP antes do novo marco de 01/02/2027 (que exigirá 8.000 horas ou 20 mi de visualizações em Shorts).

| Semana | Inscritos Meta | Inscritos Real | Horas Públicas (Longos) Meta | Horas Públicas Real | Status |
|---|---|---|---|---|---|
| 1 | 100 | - | 100 | - | Em andamento |
| 4 | 350 | - | 800 | - | Planejado |
| 8 | 700 | - | 2.200 | - | Planejado |
| 12 | 1.000 | - | 4.000 | - | Planejado |

## Regra de Decisão da Semana 4
- Se na Semana 4 o número de inscritos ou de horas estiver **abaixo de 50% da meta** (< 175 inscritos ou < 400 horas):
  1. NÃO aumente o volume de postagens. Volume sem retenção queima o canal.
  2. Execute a auditoria com o script `vendor/yt_skill/retention.py` exportando os dados de retenção do Studio.
  3. Altere **APENAS UMA COISA**: ou a fórmula de Hook (primeiros 15 segundos), ou o Tema central, ou a Composição das Thumbnails.
  4. Meça por 7 dias antes de alterar outro parâmetro.

## Registro Diário do Sprint de 7 Dias
- Dia 1: "7 Regras Silenciosas Que Fazem os Outros Te Respeitar" | Longo + 3 Shorts
- Dia 2: "5 Sinais de Que Alguém Está Mentindo" | Longo + 3 Shorts
- Dia 3: "Como Responder a uma Falta de Respeito com Classe" | Longo + 3 Shorts (Exportar retenção do Dia 1 e rodar `retention.py`)
- Dia 4: "6 Sinais Sutis de Que um Amigo Quer Ver Você Fracassar" | Longo + 3 Shorts
- Dia 5: "Por Que as Pessoas Só Dão Valor Quando Você Some?" | Longo + 3 Shorts
- Dia 6: "Como Fazer as Pessoas Gostarem de Você Sem Dizer Nada" | Longo + 3 Shorts
- Dia 7: "Manual Completo de Defesa Contra Manipulação (22 Min)" | Longo + 3 Shorts (Rodar `/yt-audit` e planejar semana 2)
