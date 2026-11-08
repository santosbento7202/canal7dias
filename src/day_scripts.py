"""src/day_scripts.py - Roteiro aprofundado com narrativas históricas de alto impacto e psicologia profunda.

Canal: Código Social
Estrutura:
- Início: Sr. Palito FULL SCREEN (abertura magnética em 4K).
- Desenvolvimento: Cenas de filmes e situações reais em tela cheia com Sr. Palito no CANTINHO (badge circular neon).
- Encerramento: Sr. Palito FULL SCREEN (conclusão de soberania em 4K).
"""

from typing import Any, Dict

DAY_SCRIPTS = {
    1: {
        "title": "A Psicologia Sombria da Calma: Como Destruir Qualquer Provocação Sem Dizer Uma Palavra",
        "thumb_text": "O PODER DO SILÊNCIO",
        "hook_formula": "The Statistic",
        "full_narration": (
            "O maior erro neurobiológico que um homem comete em um confronto é achar que precisa se defender. "
            "Toda vez que você abre a boca no reflexo da raiva, você ativa a química da submissão. "
            "Em 1808, Napoleão Bonaparte perdeu completamente o controle no palácio das Tulherias. "
            "Diante de ministros, embaixadores e generais, o imperador berrou ameaças viscerais durante duas horas seguidas contra Charles-Maurice de Talleyrand, seu próprio diplomata. "
            "A neurociência explica o que aconteceu: Napoleão sofreu um sequestro brutal da amígdala — uma tempestade de cortisol e adrenalina que reduz qualquer intelecto ao desespero primitivo.\n\n"
            "E sabe o que Talleyrand fez enquanto o homem mais temido do mundo espumava de raiva a centímetros do seu rosto? "
            "Absolutamente nada. Não piscou, não cruzou os braços em postura defensiva e não pronunciou uma única sílaba. "
            "Na psicologia comportamental, isso se chama Espelho Negro. "
            "Quando a agressão não encontra resistência nem reação, o cérebro do atacante entra em colapso por dissonância cognitiva: "
            "sem alvo para rebater, todo o ridículo e o descontrole da explosão recaem inteiramente sobre quem gritou.\n\n"
            "Quando Napoleão bateu a porta e saiu ensandecido pelo próprio ódio, Talleyrand ajeitou com calma as abotoaduras, olhou para a sala e sussurrou apenas uma frase: "
            "Que pena ver um homem tão grande ser tão mal educado. "
            "Entenda a lei do investimento assimétrico: em qualquer dinâmica social, quem gasta mais palavras e eleva o tom de voz está na posição subordinada. "
            "Quem domina o ritmo e a respiração governa a sala.\n\n"
            "Essa mesma manipulação psicológica foi usada no Japão feudal por Miyamoto Musashi. "
            "No duelo mortal contra Sasaki Kojiro na ilha de Ganryu, Musashi atrasou três horas de propósito. "
            "A psicologia moderna chama isso de Esgotamento de Ego. "
            "A espera ansiosa drena a glicose do córtex pré-frontal do oponente. "
            "Quando Kojiro atirou a bainha na água cego de fúria, Musashi disse calmamente: Você acabou de perder a sua espada. "
            "Kojiro atacou no desespero cego e foi abatido em um único golpe. Musashi venceu a mente do adversário antes de cruzar as lâminas.\n\n"
            "Agora guarde os três códigos cirúrgicos para dominar qualquer confronto social:\n\n"
            "Primeiro: A Dilatação Temporal dos Três Segundos. Ao ser confrontado, congele. Não responda no reflexo biológico. "
            "Conte mentalmente três segundos em silêncio absoluto sustentando o olhar. "
            "A psicologia dos interrogadores comprova: a mente humana tem pavor do vácuo de informação. "
            "Esse silêncio desconcertante faz o agressor engolir a própria insegurança diante de todos.\n\n"
            "Segundo: A Pergunta de Inversão de Enquadramento. Nunca contra-ataque uma ofensa, pois isso valida o nível da briga. "
            "Em tom neutro e duas oitavas abaixo, faça apenas uma pergunta: Você está bem? Parece que o seu dia está sendo muito difícil para falar dessa forma. "
            "Essa frase inverte instantaneamente a hierarquia social: você deixa de ser o alvo atacado e assume a postura de um adulto condescendente lidando com um ataque de birra. "
            "O agressor é desarmado sem que você precise levantar um único dedo.\n\n"
            "Terceiro: A Lei do Lócus de Controle Interno. Se uma provocação consegue acelerar os seus batimentos cardíacos, você acabou de entregar o controle remoto das suas emoções para aquela pessoa. "
            "Quem não reage não pode ser manipulado. Sorrir com calma diante do ódio alheio destrói qualquer estratégia suja, porque o agressor percebe que não tem poder sobre você.\n\n"
            "O Sr. Palito nunca discute, nunca se justifica e nunca tenta convencer tolos. "
            "Ele apenas observa o tabuleiro enquanto os arrogantes se autodestroem com o próprio ego. "
            "Se você entendeu que a calma fria é a maior arma de poder do século 21, comente Eu domino minhas reações e inscreva-se no Código Social para o próximo nível."
        ),
        "scenes": [
            {
                "scene_num": 1,
                "title_card": "A QUÍMICA DA SUBMISSÃO",
                "layout_mode": "fullscreen_narrator",
                "art_asset": "assets/branding/sr_palito_steeple.jpg",
                "narration_part": "O maior erro neurobiológico que um homem comete em um confronto é achar que precisa se defender. Toda vez que você abre a boca no reflexo da raiva, você ativa a química da submissão. Em 1808, Napoleão Bonaparte perdeu completamente o controle no palácio das Tulherias."
            },
            {
                "scene_num": 2,
                "title_card": "O SEQUESTRO DA AMÍGDALA",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_thinking.png",
                "primary_clip": "assets/broll_cache/napoleon_screaming.mp4",
                "secondary_clip": "assets/broll_cache/napoleon_battle_anger.mp4",
                "narration_part": "Diante de ministros, embaixadores e generais, o imperador berrou ameaças viscerais durante duas horas seguidas contra Charles-Maurice de Talleyrand, seu próprio diplomata. A neurociência explica o que aconteceu: Napoleão sofreu um sequestro brutal da amígdala — uma tempestade de cortisol e adrenalina que reduz qualquer intelecto ao desespero primitivo."
            },
            {
                "scene_num": 3,
                "title_card": "O EFEITO ESPELHO NEGRO",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_official.png",
                "primary_clip": "assets/broll_cache/talleyrand_calm_stare.mp4",
                "secondary_clip": "assets/broll_cache/shelby_silence_stare.mp4",
                "narration_part": "E sabe o que Talleyrand fez enquanto o homem mais temido do mundo espumava de raiva a centímetros do seu rosto? Absolutamente nada. Não piscou, não cruzou os braços em postura defensiva e não pronunciou uma única sílaba. Na psicologia comportamental, isso se chama Espelho Negro. Quando a agressão não encontra resistência nem reação, o cérebro do atacante entra em colapso por dissonância cognitiva: sem alvo para rebater, todo o ridículo e o descontrole da explosão recaem inteiramente sobre quem gritou."
            },
            {
                "scene_num": 4,
                "title_card": "QUEM GASTA ENERGIA PERDE",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_pointing.png",
                "primary_clip": "assets/broll_cache/thomas_shelby_smoke.mp4",
                "secondary_clip": "assets/broll_cache/talleyrand_smirk.mp4",
                "narration_part": "Quando Napoleão bateu a porta e saiu ensandecido pelo próprio ódio, Talleyrand ajeitou com calma as abotoaduras, olhou para a sala e sussurrou apenas uma frase: Que pena ver um homem tão grande ser tão mal educado. Entenda a lei do investimento assimétrico: em qualquer dinâmica social, quem gasta mais palavras e eleva o tom de voz está na posição subordinada. Quem domina o ritmo e a respiração governa a sala."
            },
            {
                "scene_num": 5,
                "title_card": "O ESGOTAMENTO DO EGO",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_thinking.png",
                "primary_clip": "assets/broll_cache/musashi_samurai_duel.mp4",
                "secondary_clip": "assets/broll_cache/samurai_strike_fast.mp4",
                "narration_part": "Essa mesma manipulação psicológica foi usada no Japão feudal por Miyamoto Musashi. No duelo mortal contra Sasaki Kojiro na ilha de Ganryu, Musashi atrasou três horas de propósito. A psicologia moderna chama isso de Esgotamento de Ego. A espera ansiosa drena a glicose do córtex pré-frontal do oponente. Quando Kojiro atirou a bainha na água cego de fúria, Musashi disse calmamente: Você acabou de perder a sua espada. Kojiro atacou no desespero cego e foi abatido em um único golpe. Musashi venceu a mente do adversário antes de cruzar as lâminas."
            },
            {
                "scene_num": 6,
                "title_card": "1. A DILATAÇÃO TEMPORAL",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_pointing.png",
                "primary_clip": "assets/broll_cache/hannibal_eye_contact.mp4",
                "secondary_clip": "assets/broll_cache/vacuum_eye_stare.mp4",
                "narration_part": "Agora guarde os três códigos cirúrgicos para dominar qualquer confronto social: Primeiro: A Dilatação Temporal dos Três Segundos. Ao ser confrontado, congele. Não responda no reflexo biológico. Conte mentalmente três segundos em silêncio absoluto sustentando o olhar. A psicologia dos interrogadores comprova: a mente humana tem pavor do vácuo de informação. Esse silêncio desconcertante faz o agressor engolir a própria insegurança diante de todos."
            },
            {
                "scene_num": 7,
                "title_card": "2. A PERGUNTA CIRÚRGICA",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_power.png",
                "primary_clip": "assets/broll_cache/american_psycho_sweat.mp4",
                "secondary_clip": "assets/broll_cache/logan_roy_stare.mp4",
                "narration_part": "Segundo: A Pergunta de Inversão de Enquadramento. Nunca contra-ataque uma ofensa, pois isso valida o nível da briga. Em tom neutro e duas oitavas abaixo, faça apenas uma pergunta: Você está bem? Parece que o seu dia está sendo muito difícil para falar dessa forma. Essa frase inverte instantaneamente a hierarquia social: você deixa de ser o alvo atacado e assume a postura de um adulto condescendente lidando com um ataque de birra. O agressor é desarmado sem que você precise levantar um único dedo."
            },
            {
                "scene_num": 8,
                "title_card": "3. A IMUNIDADE EMOCIONAL",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_official.png",
                "primary_clip": "assets/broll_cache/fight_club_unreactive.mp4",
                "secondary_clip": "assets/broll_cache/godfather_door_close.mp4",
                "narration_part": "Terceiro: A Lei do Lócus de Controle Interno. Se uma provocação consegue acelerar os seus batimentos cardíacos, você acabou de entregar o controle remoto das suas emoções para aquela pessoa. Quem não reage não pode ser manipulado. Sorrir com calma diante do ódio alheio destrói qualquer estratégia suja, porque o agressor percebe que não tem poder sobre você."
            },
            {
                "scene_num": 9,
                "title_card": "DOMINE O TABULEIRO",
                "layout_mode": "fullscreen_narrator",
                "art_asset": "assets/branding/sr_palito_cufflinks.jpg",
                "narration_part": "O Sr. Palito nunca discute, nunca se justifica e nunca tenta convencer tolos. Ele apenas observa o tabuleiro enquanto os arrogantes se autodestroem com o próprio ego. Se você entendeu que a calma fria é a maior arma de poder do século 21, comente Eu domino minhas reações e inscreva-se no Código Social para o próximo nível."
            }
        ],
        "chapters": [
            {"time": "0:00", "title": "A Química da Submissão"},
            {"time": "0:25", "title": "O Sequestro da Amígdala de Napoleão"},
            {"time": "0:52", "title": "O Efeito Espelho Negro de Talleyrand"},
            {"time": "1:22", "title": "A Lei do Investimento Assimétrico"},
            {"time": "1:50", "title": "A Guerra Psicológica de Musashi"},
            {"time": "2:20", "title": "Código 1: Dilatação Temporal dos 3 Segundos"},
            {"time": "2:46", "title": "Código 2: A Pergunta de Inversão de Status"},
            {"time": "3:10", "title": "Código 3: Imunidade e Lócus de Controle"},
            {"time": "3:30", "title": "O Soberano no Tabuleiro Social"}
        ],
        "shorts_stories": [
            {
                "short_num": 1,
                "title": "A Psicologia da Calma de Thomas Shelby e Napoleão",
                "narration": "Em 1808, Napoleão berrou durante duas horas seguidas contra o ministro Talleyrand. Sabe o que o ministro fez? Absolutamente nada. Quando Napoleão saiu furioso batendo a porta, Talleyrand ajeitou o terno e sussurrou: Que pena ver um homem tão grande ser tão mal educado. Quem gasta energia entrega o poder; quem domina o silêncio reina sobre a sala."
            },
            {
                "short_num": 2,
                "title": "O Efeito Psicológico Que Musashi Usou Para Vencer",
                "narration": "Miyamoto Musashi chegou três horas atrasado para o duelo mais perigoso da sua vida contra Sasaki Kojiro. Ele sabia que a espera forçada causa esgotamento de ego e destrói o córtex pré-frontal do inimigo. Quando Kojiro atacou cego de ódio, a mente dele já pertencia a Musashi. Quem perde a paciência perde a guerra."
            },
            {
                "short_num": 3,
                "title": "A Única Frase Que Destrói Qualquer Provocação",
                "narration": "Quando alguém tentar te humilhar ou provocar em público, nunca responda com raiva. Olhe nos olhos da pessoa, espere três segundos em silêncio e pergunte em tom calmo: Você está bem? Isso inverte o enquadramento: você vira o adulto da sala e a pessoa percebe que acabou de passar vergonha sozinha."
            }
        ]
    },
    2: {
        "title": "5 Sinais Ocultos de Que Alguém Está Mentindo Para Você",
        "thumb_text": "OLHE PARA OS PÉS",
        "hook_formula": "The Mistake",
        "full_narration": (
            "Você ainda acredita no mito ingênuo de que quem mente desvia o olhar? "
            "A psicologia forense e os interrogadores de elite comprovam exatamente o oposto: "
            "o mentiroso experiente te encara fixamente nos olhos sem piscar, para monitorar a sua reação e conferir se você comprou a farsa.\n\n"
            "Se você quer descobrir a verdade, precisa aprender a ler a Lei do Vazamento Não-Verbal de Paul Ekman. "
            "O cérebro límbico — a parte mais primitiva e honesta da mente humana — controla os pés e as pernas antes de tentar controlar as microexpressões do rosto. "
            "Aqui estão os cinco sinais científicos de engano que ninguém consegue ocultar:\n\n"
            "Primeiro: A Orientação de Fuga dos Pés. Em uma conversa tensa, o tronco e o rosto da pessoa podem estar voltados educadamente para você, "
            "mas se os pés estiverem virados para a porta ou apontando para longe, o subconsciente dela já decretou o desejo biológico de escapar da mentira.\n\n"
            "Segundo: O Congelamento Límbico. Uma pessoa dizendo a verdade gesticula com fluidez e assimetria natural. "
            "Quem inventa uma farsa sofre uma sobrecarga cognitiva brutal para não cometer contradições. "
            "O cérebro entra no reflexo de congelamento: os braços colam ao corpo, as mãos agarram objetos ou os dedos travam sobre a mesa para poupar energia neural.\n\n"
            "Terceiro: A Microexpressão Universal do Desprezo. O mentiroso arrogante não sente apenas medo; ele sente o que os psicólogos chamam de Deleite do Engano. "
            "Preste atenção no canto da boca. Um leve puxão unilateral para cima durante uma fração de segundo revela a convicção de que ele é mais inteligente do que você.\n\n"
            "Quarto: A Dissonância Temporal do Gesto. Quando uma história é verdadeira, o corpo gesticula milissegundos antes ou no exato instante da fala. "
            "Na mentira ensaiada, ocorre um atraso perceptível: a boca afirma Eu não fiz isso, e apenas um segundo depois a cabeça assente em negação forçada.\n\n"
            "Quinto: A Técnica Colombo de Sobrecarga Mental. Nunca confronte um mentiroso de frente acusando-o de mentir, pois ele ativará a defensiva imediata. "
            "Faça como os grandes detetives: finja inocência e peça para ele recontar os fatos em ordem cronológica inversa, do fim para o começo. "
            "A mentira é construída em linha reta; ao inverter a ordem, a carga cognitiva explode e a narrativa desmorona diante dos seus olhos.\n\n"
            "O Sr. Palito nunca perde a calma para tirar satisfações. Ele apenas observa os sinais silenciosos e deixa que os tolos se enforquem na própria mentira. "
            "Se você quer dominar a leitura da mente humana, comente Eu enxergo os sinais e inscreva-se no Código Social para o próximo nível."
        ),
        "scenes": [
            {
                "scene_num": 1,
                "title_card": "O MITO DO OLHAR",
                "layout_mode": "fullscreen_narrator",
                "art_asset": "assets/branding/sr_palito_blueprint.jpg",
                "narration_part": "Você ainda acredita no mito ingênuo de que quem mente desvia o olhar? A psicologia forense e os interrogadores de elite comprovam exatamente o oposto: o mentiroso experiente te encara fixamente nos olhos sem piscar, para monitorar a sua reação e conferir se você comprou a farsa."
            },
            {
                "scene_num": 2,
                "title_card": "1. OS PÉS ENTREGAM A FUGA",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_thinking.png",
                "primary_clip": "assets/broll_cache/feet_pointing_door.mp4",
                "secondary_clip": "assets/broll_cache/interrogation_mirror.mp4",
                "narration_part": "Se você quer descobrir a verdade, precisa aprender a ler a Lei do Vazamento Não-Verbal de Paul Ekman. O cérebro límbico controla os pés antes de controlar o rosto. Se os pés estiverem virados para a porta ou apontando para longe, o subconsciente da pessoa já decretou o desejo biológico de escapar da mentira."
            },
            {
                "scene_num": 3,
                "title_card": "2. O CONGELAMENTO LÍMBICO",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_official.png",
                "primary_clip": "assets/broll_cache/nervous_hands_fidget.mp4",
                "secondary_clip": "assets/broll_cache/american_psycho_sweat.mp4",
                "narration_part": "Segundo sinal: O Congelamento Límbico. Uma pessoa verdadeira gesticula com fluidez. Quem inventa uma farsa sofre uma sobrecarga cognitiva brutal para não cometer contradições. O cérebro entra no reflexo de congelamento: os braços colam ao corpo e as mãos travam para economizar processamento neural."
            },
            {
                "scene_num": 4,
                "title_card": "3. O MICRO-DESPREZO",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_pointing.png",
                "primary_clip": "assets/broll_cache/talleyrand_smirk.mp4",
                "secondary_clip": "assets/broll_cache/hannibal_eye_contact.mp4",
                "narration_part": "Terceiro sinal: A Microexpressão Universal do Desprezo. O mentiroso arrogante sente o que os psicólogos chamam de Deleite do Engano. Preste atenção no canto da boca: um leve puxão unilateral para cima durante uma fração de segundo revela a convicção de que ele é mais inteligente do que você."
            },
            {
                "scene_num": 5,
                "title_card": "4. A DISSONÂNCIA TEMPORAL",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_thinking.png",
                "primary_clip": "assets/broll_cache/eye_shift_nervous.mp4",
                "secondary_clip": "assets/broll_cache/shelby_silence_stare.mp4",
                "narration_part": "Quarto sinal: A Dissonância Temporal do Gesto. Na história real, o corpo gesticula sincronizado com a fala. Na mentira ensaiada, ocorre um atraso perceptível: a boca afirma Eu não fiz isso, e apenas um segundo depois a cabeça assente em negação forçada."
            },
            {
                "scene_num": 6,
                "title_card": "5. O PROTOCOLO COLOMBO",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_power.png",
                "primary_clip": "assets/broll_cache/logan_roy_stare.mp4",
                "secondary_clip": "assets/broll_cache/godfather_door_close.mp4",
                "narration_part": "Quinto sinal: A Técnica Colombo de Sobrecarga Mental. Nunca confronte um mentiroso acusando-o de frente. Finja inocência e peça para ele recontar os fatos em ordem cronológica inversa, do fim para o começo. A mentira é construída em linha reta; ao inverter a ordem, a carga cognitiva explode e a farsa desmorona."
            },
            {
                "scene_num": 7,
                "title_card": "DOMINE O TABULEIRO",
                "layout_mode": "fullscreen_narrator",
                "art_asset": "assets/branding/sr_palito_skyscraper.jpg",
                "narration_part": "O Sr. Palito nunca perde a calma para tirar satisfações. Ele apenas observa os sinais silenciosos e deixa que os tolos se enforquem na própria mentira. Se você quer dominar a leitura da mente humana, comente Eu enxergo os sinais e inscreva-se no Código Social para o próximo nível."
            }
        ],
        "chapters": [
            {"time": "0:00", "title": "O Mito do Olhar na Mentira"},
            {"time": "0:30", "title": "Sinal 1: A Orientação de Fuga dos Pés"},
            {"time": "0:58", "title": "Sinal 2: O Congelamento Límbico"},
            {"time": "1:26", "title": "Sinal 3: O Micro-Desprezo Unilateral"},
            {"time": "1:55", "title": "Sinal 4: A Dissonância Temporal dos Gestos"},
            {"time": "2:22", "title": "Sinal 5: O Protocolo Colombo do FBI"},
            {"time": "2:50", "title": "O Silêncio de Quem Enxerga o Tabuleiro"}
        ],
        "shorts_stories": [
            {
                "short_num": 1,
                "title": "O Segredo dos Pés: Como Pegar Uma Mentira",
                "narration": "Você acha que quem mente desvia o olhar? Mentirosos te encaram nos olhos para conferir se você acreditou. Mas o cérebro límbico sempre entrega a verdade nos pés: se a pessoa fala com você mas os pés apontam para a saída, ela quer fugir da própria mentira."
            },
            {
                "short_num": 2,
                "title": "A Técnica de Interrogatório Que Ninguém Escapa",
                "narration": "Nunca acuse alguém de mentir. Peça para a pessoa contar a história em ordem inversa, do fim para o começo. Como mentiras são decoradas em linha reta, o cérebro do mentiroso entra em colapso e a farsa se desmonta sozinha."
            },
            {
                "short_num": 3,
                "title": "O Sinal do Desprezo Que Entrega a Mentira",
                "narration": "Preste atenção no canto da boca quando alguém inventa uma desculpa. Um puxão sutil de milissegundos para cima revela o que a psicologia chama de Deleite do Engano: a pessoa acha que é mais inteligente do que você antes da máscara cair."
            }
        ]
    }
}


def get_curated_master_script(day: int) -> Dict[str, Any]:
    return DAY_SCRIPTS.get(day, DAY_SCRIPTS[1])
