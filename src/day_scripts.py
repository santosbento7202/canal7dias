"""src/day_scripts.py - Roteiro aprofundado com narrativas históricas de alto impacto e psicologia profunda.

Canal: Código Social
Estrutura:
- Início: Sr. Palito FULL SCREEN (abertura magnética).
- Desenvolvimento: Cenas de filmes e situações reais em tela cheia com Sr. Palito no CANTINHO (badge circular neon).
- Encerramento: Sr. Palito FULL SCREEN (conclusão de poder).
"""

from typing import Any, Dict

DAY_SCRIPTS = {
    1: {
        "title": "O Homem Que Dobrou Napoleão Sem Dizer Uma Palavra",
        "thumb_text": "O PODER DO SILÊNCIO",
        "hook_formula": "The Story",
        "full_narration": (
            "O maior erro que um homem comete em um confronto é abrir a boca para se defender. "
            "Em 1808, Napoleão Bonaparte — no auge de sua conquista militar sobre a Europa — perdeu completamente o controle no palácio das Tulherias. "
            "Diante de ministros, embaixadores e generais, o imperador gritou, ameaçou de morte e berrou insultos viscerais durante duas horas seguidas contra Charles-Maurice de Talleyrand, seu próprio diplomata. "
            "Sabe o que Talleyrand fez enquanto o homem mais temido do planeta espumava de cólera a centímetros do seu rosto? "
            "Absolutamente nada. Ele não piscou. Não cruzou os braços em postura defensiva. Não pronunciou uma única sílaba. Sustentou o olhar com uma frieza quase desumana. "
            "Quando Napoleão bateu a porta e saiu ensandecido pelo próprio ódio, Talleyrand ajeitou com calma o terno, olhou para os nobres na sala e sussurrou apenas uma frase: "
            "Que pena ver um homem tão grande ser tão mal educado. "
            "Naquele instante, a corte inteira compreendeu: Napoleão tinha o exército, mas Talleyrand era o verdadeiro dono do poder. "
            "Quem perde a calma se torna um espetáculo público; quem domina o silêncio reina sobre a sala.\n\n"
            "Essa mesma estratégia foi usada no Japão feudal pelo lendário samurai Miyamoto Musashi. "
            "No duelo decisivo na ilha de Ganryu contra Sasaki Kojiro — considerado o duelista mais rápido do império —, Musashi chegou três horas atrasado de propósito. "
            "Ele desceu do barco descalço, esculpindo um remo de madeira como espada. "
            "Quando Kojiro arremessou a bainha na água cego de fúria pela espera, Musashi disse calmamente: Você acabou de perder a sua espada. "
            "Kojiro atacou no desespero da raiva e foi abatido em um único golpe. "
            "Musashi venceu o duelo antes da primeira gota de sangue, porque quem tem pressa entrega a própria mente ao adversário.\n\n"
            "Agora entenda a neurociência por trás disso. Quando alguém tenta te desestabilizar com uma ofensa ou provocação, o cérebro do agressor espera a sua reação para justificar o ataque. "
            "Aqui estão os três códigos práticos para dominar qualquer confronto social:\n\n"
            "Primeiro: O vácuo dos três segundos. Ao ser provocado, não responda no reflexo. Conte três segundos em silêncio absoluto sustentando o olhar. "
            "A natureza humana odeia o vácuo. Esse silêncio desconcertante faz o agressor engolir a própria insegurança diante de todos.\n\n"
            "Segundo: A inversão de status de Júlio César. Capturado por piratas cilícios que pediram vinte talentos pelo seu resgate, César riu e exigiu que cobrassem cinquenta, passando a dar ordens aos próprios sequestradores. "
            "Nunca aja como vítima. Quem não aceita a posição de inferioridade destrói a hierarquia do agressor.\n\n"
            "Terceiro: A lei da não-reatividade. Se uma ofensa te atinge, você concedeu ao outro o controle remoto das suas emoções. Quem não reage não pode ser manipulado.\n\n"
            "O Sr. Palito nunca discute, não levanta a voz e não tenta convencer tolos. Ele apenas observa o tabuleiro enquanto os outros se destroem com o próprio ego. "
            "Se você entendeu que a calma é a maior arma de poder, comente Eu controlo minhas reações e inscreva-se no Código Social para o próximo nível."
        ),
        "scenes": [
            {
                "scene_num": 1,
                "title_card": "O HOMEM QUE DOBROU NAPOLEÃO",
                "layout_mode": "fullscreen_narrator",
                "art_asset": "assets/branding/sr_palito_thinking.jpg",
                "narration_part": "O maior erro que um homem comete em um confronto é abrir a boca para se defender. Em 1808, Napoleão Bonaparte — no auge de sua conquista militar sobre a Europa — perdeu completamente o controle no palácio das Tulherias."
            },
            {
                "scene_num": 2,
                "title_card": "A FÚRIA DO IMPERADOR",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_thinking.png",
                "primary_clip": "assets/broll_cache/napoleon_screaming.mp4",
                "secondary_clip": "assets/broll_cache/napoleon_battle_anger.mp4",
                "narration_part": "Diante de ministros, embaixadores e generais, o imperador gritou, ameaçou de morte e berrou insultos viscerais durante duas horas seguidas contra Charles-Maurice de Talleyrand, seu próprio diplomata."
            },
            {
                "scene_num": 3,
                "title_card": "A CALMA DESUMANA",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_official.png",
                "primary_clip": "assets/broll_cache/talleyrand_calm_stare.mp4",
                "secondary_clip": "assets/broll_cache/peaky_meeting_silence.mp4",
                "narration_part": "Sabe o que Talleyrand fez enquanto o homem mais temido do planeta espumava de cólera a centímetros do seu rosto? Absolutamente nada. Ele não piscou. Não cruzou os braços em postura defensiva. Não pronunciou uma única sílaba. Sustentou o olhar com uma frieza quase desumana."
            },
            {
                "scene_num": 4,
                "title_card": "QUEM GRITA ENTREGA O PODER",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_pointing.png",
                "primary_clip": "assets/broll_cache/talleyrand_smirk.mp4",
                "secondary_clip": "assets/broll_cache/walking_calm.mp4",
                "narration_part": "Quando Napoleão bateu a porta e saiu ensandecido pelo próprio ódio, Talleyrand ajeitou com calma o terno, olhou para os nobres na sala e sussurrou apenas uma frase: Que pena ver um homem tão grande ser tão mal educado. Naquele instante, a corte inteira compreendeu: Napoleão tinha o exército, mas Talleyrand era o verdadeiro dono do poder. Quem perde a calma se torna um espetáculo público; quem domina o silêncio reina sobre a sala."
            },
            {
                "scene_num": 5,
                "title_card": "A ESTRATÉGIA DE MUSASHI",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_thinking.png",
                "primary_clip": "assets/broll_cache/musashi_samurai_duel.mp4",
                "secondary_clip": "assets/broll_cache/samurai_strike_fast.mp4",
                "narration_part": "Essa mesma estratégia foi usada no Japão feudal pelo lendário samurai Miyamoto Musashi. No duelo decisivo na ilha de Ganryu contra Sasaki Kojiro — considerado o duelista mais rápido do império —, Musashi chegou três horas atrasado de propósito. Ele desceu do barco descalço, esculpindo um remo de madeira como espada. Quando Kojiro arremessou a bainha na água cego de fúria pela espera, Musashi disse calmamente: Você acabou de perder a sua espada. Kojiro atacou no desespero da raiva e foi abatido em um único golpe. Musashi venceu o duelo antes da primeira gota de sangue, porque quem tem pressa entrega a própria mente ao adversário."
            },
            {
                "scene_num": 6,
                "title_card": "1. O VÁCUO DOS 3 SEGUNDOS",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_pointing.png",
                "primary_clip": "assets/broll_cache/vacuum_eye_stare.mp4",
                "secondary_clip": "assets/broll_cache/peaky_meeting_silence.mp4",
                "narration_part": "Agora entenda a neurociência por trás disso. Quando alguém tenta te desestabilizar com uma ofensa ou provocação, o cérebro do agressor espera a sua reação para justificar o ataque. Primeiro: O vácuo dos três segundos. Ao ser provocado, não responda no reflexo. Conte três segundos em silêncio absoluto sustentando o olhar. A natureza humana odeia o vácuo. Esse silêncio desconcertante faz o agressor engolir a própria insegurança diante de todos."
            },
            {
                "scene_num": 7,
                "title_card": "2. A LIÇÃO DE JÚLIO CÉSAR",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_power.png",
                "primary_clip": "assets/broll_cache/julius_caesar_power.mp4",
                "secondary_clip": "assets/broll_cache/roman_legions_march.mp4",
                "narration_part": "Segundo: A inversão de status de Júlio César. Capturado por piratas cilícios que pediram vinte talentos pelo seu resgate, César riu e exigiu que cobrassem cinquenta, passando a dar ordens aos próprios sequestradores. Nunca aja como vítima. Quem não aceita a posição de inferioridade destrói a hierarquia do agressor."
            },
            {
                "scene_num": 8,
                "title_card": "3. A LEI DA NÃO-REATIVIDADE",
                "layout_mode": "corner_narrator",
                "badge_asset": "assets/branding/narrator_badge_official.png",
                "primary_clip": "assets/broll_cache/godfather_calm.mp4",
                "secondary_clip": "assets/broll_cache/chess_checkmate_drama.mp4",
                "narration_part": "Terceiro: A lei da não-reatividade. Se uma ofensa te atinge, você concedeu ao outro o controle remoto das suas emoções. Quem não reage não pode ser manipulado. O Sr. Palito nunca discute, não levanta a voz e não tenta convencer tolos. Ele apenas observa o tabuleiro enquanto os outros se destroem com o próprio ego."
            },
            {
                "scene_num": 9,
                "title_card": "DOMINE O TABULEIRO",
                "layout_mode": "fullscreen_narrator",
                "art_asset": "assets/branding/sr_palito_power.jpg",
                "narration_part": "Se você entendeu que a calma é a maior arma de poder, comente Eu controlo minhas reações e inscreva-se no Código Social para o próximo nível."
            }
        ],
        "chapters": [
            {"time": "0:00", "title": "O Maior Erro no Confronto"},
            {"time": "0:25", "title": "A Fúria de Napoleão no Palácio"},
            {"time": "0:48", "title": "A Calma Desumana de Talleyrand"},
            {"time": "1:15", "title": "A Frase que Virou a História"},
            {"time": "1:42", "title": "A Estratégia de Miyamoto Musashi"},
            {"time": "2:15", "title": "Protocolo 1: O Vácuo dos 3 Segundos"},
            {"time": "2:38", "title": "Protocolo 2: A Lição de Júlio César"},
            {"time": "2:58", "title": "Protocolo 3: A Lei da Não-Reatividade"},
            {"time": "3:18", "title": "Encerramento e Ativação do Código"}
        ],
        "shorts_stories": [
            {
                "short_num": 1,
                "title": "Como Dobrar Napoleão Usando Apenas o Silêncio",
                "narration": "Em 1808, Napoleão gritou durante duas horas seguidas contra o ministro Talleyrand. Sabe o que o ministro fez? Absolutamente nada. Quando Napoleão bateu a porta e saiu furioso, Talleyrand sussurrou para a corte: Que pena ver um homem tão grande ser tão mal educado. Quem grita entrega o poder; quem se cala domina a sala."
            },
            {
                "short_num": 2,
                "title": "A Estratégia de Miyamoto Musashi Para Vencer Sem Lutar",
                "narration": "Miyamoto Musashi chegou três horas atrasado para o duelo mais perigoso da sua vida contra Sasaki Kojiro. Ele não estava com pressa. Ele sabia que a raiva e a ansiedade destroem o foco do inimigo. Quando Kojiro desembainhou a espada enfurecido, a mente dele já pertencia a Musashi."
            },
            {
                "short_num": 3,
                "title": "A Lição de Júlio César Contra os Piratas",
                "narration": "Quando piratas capturaram Júlio César e pediram 20 talentos de ouro pelo resgate, César caiu na risada. Ele disse que eles não sabiam quem tinham capturado e ordenou que cobrassem 50. Ao se recusar a agir como vítima, César assumiu o comando imediato."
            }
        ]
    }
}


def get_curated_master_script(day: int) -> Dict[str, Any]:
    return DAY_SCRIPTS.get(day, DAY_SCRIPTS[1])
