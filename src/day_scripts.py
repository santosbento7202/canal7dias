"""src/day_scripts.py - Roteiros baseados em histórias reais fascinantes e ensinamentos psicológicos contra-intuitivos.

Canal: Código Social
Estilo: Storytelling de poder, história e psicologia profunda (estilo Aperture / 48 Leis do Poder).
"""

from typing import Any, Dict

DAY_SCRIPTS = {
    1: {
        "title": "O Homem Que Dobrou Napoleão Sem Dizer Uma Palavra",
        "thumb_text": "O PODER DO SILÊNCIO",
        "hook_formula": "The Story",
        "full_narration": (
            "Em 1808, Napoleão Bonaparte — o imperador mais temido do planeta — perdeu completamente a cabeça. "
            "No palácio das Tulherias, diante de generais e diplomatas, Napoleão gritou, ameaçou e berrou durante duas horas seguidas contra Charles Talleyrand, seu próprio ministro. "
            "Sabe o que Talleyrand fez enquanto o homem mais poderoso da Europa espumava de raiva a centímetros do seu rosto? "
            "Absolutamente nada. Ele não piscou. Não cruzou os braços. Não tentou se justificar. Sustentou o olhar com uma calma quase sobrenatural. "
            "Quando Napoleão bateu a porta e saiu ensandecido, Talleyrand ajeitou suavemente o paletó, olhou para os nobres na sala e sussurrou apenas uma frase: "
            "Que pena ver um homem tão grande ser tão mal educado. "
            "Naquele instante, toda a corte compreendeu: quem perde o controle entrega o poder; quem permanece sereno domina o tabuleiro.\n\n"
            "Séculos antes, no Japão feudal, o lendário samurai Miyamoto Musashi usava exatamente a mesma arma psicológica. "
            "No duelo mais perigoso da sua vida contra Sasaki Kojiro, Musashi chegou três horas atrasado de propósito. "
            "Ele sabia que a pressa e a irritação destroem o discernimento humano. "
            "Quando Kojiro desembainhou a espada enfurecido pela espera, a mente dele já pertencia a Musashi antes mesmo do primeiro golpe.\n\n"
            "Agora traga essa sabedoria para a sua vida hoje. Aqui estão os três ensinamentos secretos dessa dinâmica.\n\n"
            "Primeiro: O efeito vácuo social. Quando alguém te faz uma ofensa ou provocação, a sua biologia quer reagir no reflexo. Não caia nessa armadilha. "
            "Faça uma pausa de três segundos olhando fixamente nos olhos do outro. O silêncio cria um vácuo psicológico insuportável, forçando quem te atacou a engolir a própria insegurança diante de todos.\n\n"
            "Segundo: A inversão de status de Júlio César. Quando foi capturado por piratas na juventude, eles pediram vinte talentos de ouro pelo resgate. "
            "César riu na cara deles, disse que não sabiam quem tinham capturado e exigiu que cobrassem cinquenta. "
            "Ao se recusar a agir como vítima, César inverteu instantaneamente a hierarquia psicológica e passou a dar ordens aos próprios captores.\n\n"
            "Terceiro: A lei da não-reatividade. Toda vez que você se ofende com as palavras de alguém, você entrega a chave do seu cérebro para essa pessoa te controlar. "
            "Quem não reage, não pode ser manipulado.\n\n"
            "O Sr. Palito não grita, não discute e não tenta provar nada. Ele apenas observa enquanto os outros se destroem com o próprio ego. "
            "Se você compreendeu o poder brutal do silêncio estratégico, comente Eu controlo minhas reações e inscreva-se no Código Social para o próximo capítulo."
        ),
        "scenes": [
            {
                "scene_num": 1,
                "title_card": "O ATAQUE DE NAPOLEÃO",
                "art_asset": "assets/branding/sr_palito_thinking.jpg",
                "narration_part": "Em 1808, Napoleão Bonaparte — o imperador mais temido do planeta — perdeu completamente a cabeça. No palácio das Tulherias, diante de generais e diplomatas, Napoleão gritou, ameaçou e berrou durante duas horas seguidas contra Charles Talleyrand, seu próprio ministro."
            },
            {
                "scene_num": 2,
                "title_card": "A CALMA SOBRENATURAL",
                "art_asset": "assets/branding/sr_palito_official.jpg",
                "narration_part": "Sabe o que Talleyrand fez enquanto o homem mais poderoso da Europa espumava de raiva a centímetros do seu rosto? Absolutamente nada. Ele não piscou. Não cruzou os braços. Não tentou se justificar. Sustentou o olhar com uma calma quase sobrenatural."
            },
            {
                "scene_num": 3,
                "title_card": "QUEM GRITA PERDE O PODER",
                "art_asset": "assets/branding/sr_palito_pointing.jpg",
                "narration_part": "Quando Napoleão bateu a porta e saiu ensandecido, Talleyrand ajeitou suavemente o paletó, olhou para os nobres na sala e sussurrou apenas uma frase: Que pena ver um homem tão grande ser tão mal educado. Naquele instante, toda a corte compreendeu: quem perde o controle entrega o poder; quem permanece sereno domina o tabuleiro."
            },
            {
                "scene_num": 4,
                "title_card": "A ESTRATÉGIA DE MUSASHI",
                "art_asset": "assets/branding/sr_palito_official_fullbody.jpg",
                "narration_part": "Séculos antes, no Japão feudal, o lendário samurai Miyamoto Musashi usava exatamente a mesma arma psicológica. No duelo mais perigoso da sua vida contra Sasaki Kojiro, Musashi chegou três horas atrasado de propósito. Ele sabia que a pressa e a irritação destroem o discernimento humano. Quando Kojiro desembainhou a espada enfurecido pela espera, a mente dele já pertencia a Musashi antes mesmo do primeiro golpe."
            },
            {
                "scene_num": 5,
                "title_card": "1. O EFEITO VÁCUO SOCIAL",
                "art_asset": "assets/branding/sr_palito_thinking.jpg",
                "narration_part": "Agora traga essa sabedoria para a sua vida hoje. Primeiro: O efeito vácuo social. Quando alguém te faz uma ofensa ou provocação, a sua biologia quer reagir no reflexo. Não caia nessa armadilha. Faça uma pausa de três segundos olhando fixamente nos olhos do outro. O silêncio cria um vácuo psicológico insuportável, forçando quem te atacou a engolir a própria insegurança diante de todos."
            },
            {
                "scene_num": 6,
                "title_card": "2. A LIÇÃO DE CÉSAR",
                "art_asset": "assets/branding/sr_palito_power.jpg",
                "narration_part": "Segundo: A inversão de status de Júlio César. Quando foi capturado por piratas na juventude, eles pediram vinte talentos de ouro pelo resgate. César riu na cara deles, disse que não sabiam quem tinham capturado e exigiu que cobrassem cinquenta. Ao se recusar a agir como vítima, César inverteu instantaneamente a hierarquia psicológica e passou a dar ordens aos próprios captores."
            },
            {
                "scene_num": 7,
                "title_card": "3. A LEI DA NÃO-REATIVIDADE",
                "art_asset": "assets/branding/sr_palito_pointing.jpg",
                "narration_part": "Terceiro: A lei da não-reatividade. Toda vez que você se ofende com as palavras de alguém, você entrega a chave do seu cérebro para essa pessoa te controlar. Quem não reage, não pode ser manipulado."
            },
            {
                "scene_num": 8,
                "title_card": "DOMINE O TABULEIRO",
                "art_asset": "assets/branding/sr_palito_power.jpg",
                "narration_part": "O Sr. Palito não grita, não discute e não tenta provar nada. Ele apenas observa enquanto os outros se destroem com o próprio ego."
            },
            {
                "scene_num": 9,
                "title_card": "CÓDIGO SOCIAL ATIVADO",
                "art_asset": "assets/branding/sr_palito_official_fullbody.jpg",
                "narration_part": "Se você compreendeu o poder brutal do silêncio estratégico, comente Eu controlo minhas reações e inscreva-se no Código Social para o próximo capítulo."
            }
        ],
        "chapters": [
            {"time": "0:00", "title": "O Ataque de Fúria de Napoleão"},
            {"time": "0:25", "title": "A Calma Sobrenatural de Talleyrand"},
            {"time": "0:48", "title": "A Frase que Destruiu o Imperador"},
            {"time": "1:10", "title": "A Estratégia Psicológica de Musashi"},
            {"time": "1:35", "title": "Regra 1: O Efeito Vácuo Social"},
            {"time": "1:58", "title": "Regra 2: A Lição de Júlio César"},
            {"time": "2:18", "title": "Regra 3: A Lei da Não-Reatividade"},
            {"time": "2:36", "title": "Como o Sr. Palito Domina o Jogo"},
            {"time": "2:52", "title": "Encerramento e Próximo Código"}
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
