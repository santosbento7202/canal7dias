# SETUP_CANAL.md - Manual Completo de Configuração: Canal Código Social

Este guia contém o passo a passo exato e obrigatório que o proprietário do canal deve realizar manualmente uma única vez antes de ativar a automação diária.

---

## 0. Metas Honestas e Regras do YouTube (Leia com Atenção)

O objetivo é monetizar o canal exclusivamente com anúncios do Programa de Parcerias do YouTube (YPP), **sem venda de produtos e sem links de afiliados**.

### Regras Oficiais do YPP (Tier 2):
- **1.000 inscritos** + **4.000 horas públicas de exibição** em vídeos longos (nos últimos 12 meses) **OU** **10 milhões de visualizações** em Shorts (nos últimos 90 dias).
- **Importante:** Visualizações e horas de Shorts **NÃO** contam para as 4.000 horas de vídeos longos.
- **Atenção ao Prazo:** A partir de **01/02/2027**, novos canais precisarão de **8.000 horas** ou **20 milhões de visualizações em Shorts**.
- A análise do canal após atingir os requisitos leva cerca de 30 dias.
- Em um sprint de 7 dias, a monetização só ocorre se 1 ou 2 vídeos viralizarem organicamente. O algoritmo não pode ser forçado. É expressamente proibido comprar inscritos, usar bots ou sub4sub (isso causa encerramento da conta).
- **Estratégia Oficial:** Sprint de 7 dias para maximizar a chance de viralização inicial + Plano estruturado de 12 semanas para candidatura antes de 01/02/2027.

---

## 1. Identidade do Canal e Branding

### Nome e Handles:
- **Nome do Canal:** `Código Social`
- **Handle Principal (Desejado):** `@CodigoSocialOficial`
- **3 Alternativas Oficiais (caso o principal esteja em uso):**
  1. `@CodigoSocialCanal`
  2. `@CodigoSocialBr`
  3. `@CanalCodigoSocial`

### Descrição Oficial do Canal (Primeiros 150 caracteres otimizados para SEO):
```
Decodifique a linguagem silenciosa do comportamento humano. Regras práticas sobre respeito, postura, detecção de mentiras e defesa contra manipulação.
```
*Descrição completa sugerida:*
> Eles jogam. Você enxerga. O Código Social decodifica a linguagem silenciosa das interações humanas, revelando a psicologia prática por trás do respeito, autoridade e convivência diária. Sem jargões e sem fórmulas mágicas: apenas observação cirúrgica.
> 
> Vídeos longos com análises aprofundadas e pílulas diárias em Shorts.
> Contato institucional: canalcodigosocial@gmail.com

### Palavras-chave do Canal (Exatamente 15 tags de desambiguação):
`psicologia prática`, `linguagem corporal`, `dinâmica social`, `comunicação assertiva`, `respeito`, `postura`, `detecção de mentiras`, `manipulação psicológica`, `inteligência emocional`, `comportamento humano`, `microexpressões`, `leis do poder`, `autocontrole`, `psicologia comportamental`, `código social`

### Arquivos de Imagem Prontos:
- **Foto de Perfil / Avatar (800x800):** `assets/branding/avatar_800x800.png` (Fundo preto, anel dourado 14px e stickman coroado).
- **Banner do Canal (2560x1440):** `assets/branding/banner_2560x1440.png` (Safe area central 1546x423 com título em branco e subtítulo em ouro).

---

## 2. Configurações Manuais no YouTube Studio

1. **Criar o Canal:** Acesse [YouTube Studio](https://studio.youtube.com/) e crie o canal com o nome **Código Social**.
2. **Verificação de Telefone (Obrigatório):**
   - Acesse **Configurações -> Canal -> Qualificação para recursos**.
   - Ative os **Recursos Intermediários** via SMS/chamada.
   - *Por que é obrigatório?* Sem isso, o canal fica proibido de enviar miniaturas (thumbnails) personalizadas e vídeos acima de 15 minutos (necessário para o Dia 7).
3. **Verificação em 2 Etapas (2FA):**
   - Ative a segurança em 2 etapas na Conta Google do canal. O YouTube exige isso para se candidatar ao YPP.
4. **Criar Conta no Google AdSense (Gratuito):**
   - Acesse [Google AdSense](https://adsense.google.com/) e vincule seu e-mail agora. A aprovação da conta AdSense pode levar dias ou semanas; antecipe para não travar a monetização quando bater os números.

---

## 3. Google Cloud Console & Credenciais da YouTube API

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/).
2. Crie um novo projeto chamado `Codigo-Social-Pipeline`.
3. No menu lateral, acesse **APIs e Serviços -> Biblioteca**.
4. Pesquise por **YouTube Data API v3** e clique em **Ativar**.
5. Vá em **APIs e Serviços -> Tela de consentimento OAuth**:
   - Selecione **Externo** e clique em Criar.
   - Nome do aplicativo: `Codigo Social Uploader`.
   - E-mail de suporte e dados do desenvolvedor: seu e-mail.
   - Em **Escopos**, adicione `.../auth/youtube.upload` e `.../auth/youtube.force-ssl`.
   - **CRÍTICO - ATENÇÃO:** Mude o status da tela de consentimento de "Teste" para **"Em produção"** (In production).
   - *Aviso:* Em modo "Teste", o token de atualização (`refresh_token`) **expira em 7 dias**. O pipeline morreria no dia 8. Em modo "Em produção", ele é permanente.
6. Vá em **APIs e Serviços -> Credenciais**:
   - Clique em **Criar credenciais -> ID do cliente OAuth**.
   - Tipo de aplicativo: **Aplicativo para Computador** (Desktop App).
   - Baixe o arquivo JSON gerado e salve-o na raiz deste projeto com o nome `client_secret.json`.

---

## 4. Gerando as Chaves de Acesso (`src/auth_once.py`)

Execute o script de autenticação local no seu terminal (uma única vez):

```powershell
python src/auth_once.py --client-secrets client_secret.json
```

1. Seu navegador abrirá a página de autorização do Google.
2. Selecione a conta do canal e conceda permissão total.
3. O terminal exibirá 3 valores. Copie-os com segurança:
   - `YT_CLIENT_ID`
   - `YT_CLIENT_SECRET`
   - `YT_REFRESH_TOKEN`

---

## 5. Configurando os GitHub Secrets

No seu repositório no GitHub (mantenha o repositório como **PÚBLICO** para minutos ilimitados de GitHub Actions):
Acesse: **Settings -> Secrets and variables -> Actions -> New repository secret**.

Adicione os seguintes segredos:

| Nome do Segredo | Descrição | Onde Obter |
|---|---|---|
| `YT_CLIENT_ID` | Client ID OAuth da Google Cloud | Gerado no passo 4 |
| `YT_CLIENT_SECRET` | Client Secret OAuth da Google Cloud | Gerado no passo 4 |
| `YT_REFRESH_TOKEN` | Refresh Token permanente | Gerado no passo 4 |
| `OPENROUTER_API_KEY` | Chave de API da OpenRouter (gratuita) | [openrouter.ai/keys](https://openrouter.ai/keys) |
| `PEXELS_API_KEY` | Chave da API gratuita de vídeos da Pexels | [pexels.com/api](https://www.pexels.com/api/) |

---

## 6. Teste de Upload Obrigatório e Modo Semi-Auto

### O Teste de Upload de 10 Segundos:
Após configurar as credenciais, execute um teste de upload para validar a permissão do canal:
```powershell
python -m src.run_day --day 1
```

### O que observar no YouTube Studio:
- Se o vídeo for enviado e ficar agendado normalmente: **Modo Automático Total Aprovado**.
- **Se o vídeo ficar trancado como "Privado" (Locked Private) com aviso da API:**
  O YouTube por vezes bloqueia uploads automáticos públicos de projetos de API que ainda não passaram por auditoria formal de conformidade do Google.
- **Plano de Contingência Oficial (Modo Semi-Auto):**
  Se isso ocorrer, não se preocupe! O pipeline opera perfeitamente no **Modo Semi-Auto**:
  1. O pipeline diário gera automaticamente na pasta `out/dia_N/`:
     - O vídeo longo (`video.mp4` em 1080p);
     - A miniatura oficial (`thumb.png` em 1280x720);
     - O arquivo `metadata.txt` com o título exato, descrição otimizada, minutagem de capítulos e comentário fixado;
     - Os 3 Shorts diários prontos (`shorts/short_1.mp4`, etc.).
  2. O dono abre o [YouTube Studio](https://studio.youtube.com/) e sobe os arquivos manualmente em **3 minutos**.
  3. A automação garante 100% da criação, edição, renderização e controle de qualidade.

---

## 7. Rotina Humana Diária de 15 Minutos (O Que Realmente Move a Agulha)

Nenhuma automação substitui o calor humano e os primeiros sinais de engajamento do algoritmo:

1. **Primeiras 2 Horas:** Assim que o vídeo longo for publicado (12:00 BRT), fixe o comentário polarizador e responda aos 10 primeiros comentários. O algoritmo prioriza vídeos com conversas ativas logo no início.
2. **Dia 3:** Acesse o YouTube Studio -> Estatísticas do vídeo do Dia 1 -> Retenção de Público. Baixe o CSV e rode:
   ```powershell
   python vendor/yt_skill/retention.py retention.csv --transcript out/dia_1/transcript.srt
   ```
   Identifique o segundo exato onde houve queda e ajuste a entonação dos ganchos dos dias seguintes.
3. **Dia 7:** Execute uma auditoria geral de retenção e CTR. Escolha **UMA única correção** para a semana 2 (ajustar título, hook ou contraste da thumb).
4. **Divulgação Inicial:** Compartilhe o link do vídeo e dos Shorts nos seus círculos e comunidades afins nos primeiros 60 minutos.
