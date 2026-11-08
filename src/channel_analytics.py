"""src/channel_analytics.py - Monitoramento inteligente de views e adaptação dinâmica de conteúdo.

Recursos:
- Consulta métricas gerais do canal via YouTube Data API v3 (total_views, subscriberCount, videoCount, recent_views).
- Se não houver credenciais da API ou em dry-run, opera com histórico local em reports/channel_metrics.json.
- Diagnostica o desempenho ('low_views', 'healthy', 'viral').
- Quando 'low_views' é detectado, ativa automaticamente o 'MODO TRAÇÃO MÁXIMA / VIRAL BOOST':
  1. Título & Thumbnail: Injeta gatilhos de urgência, contraste extremo e badges de alerta psicológico.
  2. Ritmo & Cortes: Acelera transições de cena para 2.8s - 3.2s (retenção agressiva).
  3. Hooks: Prioriza fórmulas de alta polarização (Contrarian Shock, The Negative Consequence).
  4. Shorts: Otimiza encaixe de loop infinito e ganchos em 2 segundos.
  5. Engajamento: Comentário fixado provocativo para multiplicar volume de comentários.
"""

import datetime
import json
import os
from typing import Any, Dict, List, Optional

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METRICS_HISTORY_PATH = os.path.join(PROJECT_ROOT, "reports", "channel_metrics.json")
GATES_CONFIG_PATH = os.path.join(PROJECT_ROOT, "config", "gates.json")


def load_metrics_history() -> Dict[str, Any]:
    """Carrega o histórico de métricas do canal."""
    if os.path.exists(METRICS_HISTORY_PATH):
        try:
            with open(METRICS_HISTORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "channel_id": "",
        "history": [],
        "current_status": "low_views",
        "last_updated": None
    }


def save_metrics_history(data: Dict[str, Any]):
    """Salva histórico de métricas em reports/channel_metrics.json."""
    os.makedirs(os.path.dirname(METRICS_HISTORY_PATH), exist_ok=True)
    with open(METRICS_HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def fetch_youtube_channel_metrics(youtube_service=None) -> Dict[str, Any]:
    """Obtém estatísticas do canal via YouTube Data API v3 ou fallback monitorado."""
    if youtube_service is None:
        try:
            from src.youtube_uploader import get_authenticated_service
            youtube_service = get_authenticated_service()
        except Exception:
            youtube_service = None

    metrics = {
        "total_views": 0,
        "subscribers": 0,
        "video_count": 0,
        "recent_video_views": [],
        "avg_recent_views": 0.0,
        "is_live_api": False
    }

    if youtube_service:
        try:
            resp = youtube_service.channels().list(
                part="statistics,contentDetails",
                mine=True
            ).execute()

            items = resp.get("items", [])
            if items:
                stats = items[0].get("statistics", {})
                metrics["total_views"] = int(stats.get("viewCount", 0))
                metrics["subscribers"] = int(stats.get("subscriberCount", 0))
                metrics["video_count"] = int(stats.get("videoCount", 0))
                metrics["is_live_api"] = True

                # Buscar visualizações dos últimos vídeos no canal
                uploads_list_id = items[0].get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
                if uploads_list_id:
                    playlist_resp = youtube_service.playlistItems().list(
                        part="snippet,contentDetails",
                        playlistId=uploads_list_id,
                        maxResults=5
                    ).execute()

                    video_ids = [it["contentDetails"]["videoId"] for it in playlist_resp.get("items", [])]
                    if video_ids:
                        v_resp = youtube_service.videos().list(
                            part="statistics",
                            id=",".join(video_ids)
                        ).execute()
                        v_views = [int(v.get("statistics", {}).get("viewCount", 0)) for v in v_resp.get("items", [])]
                        metrics["recent_video_views"] = v_views
                        if v_views:
                            metrics["avg_recent_views"] = sum(v_views) / len(v_views)
                return metrics
        except Exception as e:
            print(f"[ANALYTICS] Aviso ao consultar YouTube API ({e}). Usando histórico local.")

    # Fallback para histórico local ou baseline de canal em crescimento
    history = load_metrics_history()
    recent_entry = history.get("history", [])[-1] if history.get("history") else {}
    metrics["total_views"] = recent_entry.get("total_views", 120)
    metrics["subscribers"] = recent_entry.get("subscribers", 15)
    metrics["video_count"] = recent_entry.get("video_count", 1)
    metrics["avg_recent_views"] = recent_entry.get("avg_recent_views", 85.0)
    metrics["is_live_api"] = False
    return metrics


def evaluate_channel_performance(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Avalia se as views estão baixas e determina o pacote de adaptação do conteúdo."""
    avg_views = metrics.get("avg_recent_views", 0.0)
    total_views = metrics.get("total_views", 0)

    # Limiares de avaliação
    # Canal com média abaixo de 500 views nos últimos vídeos ou total < 2.000 entra em MODO TRAÇÃO MÁXIMA
    is_low = (avg_views < 500.0) or (total_views < 2000)

    if is_low:
        status = "low_views"
        urgency_level = "maximum_boost"
        recommendations = [
            "Aumentar velocidade de cortes para 2.8s a 3.2s (redução de tédio)",
            "Priorizar hooks de 'Alerta de Ameaça' e 'Choque Contrariano' (+35% CTR)",
            "Aplicar badge vermelho urgente na thumbnail ('ERRO FATAL' / 'NUNCA DIGA ISSO')",
            "Intensificar loop de retenção nos Shorts com encaixe gramatical de 1 frase",
            "Disparar pergunta polarizante no comentário fixado para explodir interações"
        ]
        adaptations = {
            "mode": "viral_traction_boost",
            "pacing_multiplier": 0.80,         # Cortes 20% mais rápidos
            "thumb_badge_text": "ERRO FATAL",  # Substitui badges neutros por urgência
            "thumb_badge_color": (220, 20, 20),
            "hook_priority_formula": "The Mistake",
            "shorts_pace": "fast",
            "pinned_comment_style": "provocative"
        }
    elif avg_views < 5000.0:
        status = "healthy"
        urgency_level = "standard_growth"
        recommendations = [
            "Manter cadência de autoridade e retenção equilibrada",
            "Alternar entre curiosidade e lições de psicologia prática"
        ]
        adaptations = {
            "mode": "standard_growth",
            "pacing_multiplier": 1.0,
            "thumb_badge_text": "LEI DO PODER",
            "thumb_badge_color": (220, 20, 20),
            "hook_priority_formula": "The Statistic",
            "shorts_pace": "normal",
            "pinned_comment_style": "reflective"
        }
    else:
        status = "viral"
        urgency_level = "scale_mode"
        recommendations = [
            "Canal em forte tração orgânica; sustentar identidade de mentor soberano"
        ]
        adaptations = {
            "mode": "scale_mode",
            "pacing_multiplier": 1.0,
            "thumb_badge_text": "CÓDIGO SOCIAL",
            "thumb_badge_color": (255, 215, 0),
            "hook_priority_formula": "The Story",
            "shorts_pace": "normal",
            "pinned_comment_style": "community"
        }

    return {
        "status": status,
        "urgency_level": urgency_level,
        "avg_recent_views": avg_views,
        "total_views": total_views,
        "is_low": is_low,
        "recommendations": recommendations,
        "adaptations": adaptations
    }


def record_daily_analytics_check() -> Dict[str, Any]:
    """Executa a verificação completa diária do canal e persiste os dados."""
    metrics = fetch_youtube_channel_metrics()
    eval_res = evaluate_channel_performance(metrics)

    history_data = load_metrics_history()
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    entry = {
        "timestamp": now_iso,
        "total_views": metrics["total_views"],
        "subscribers": metrics["subscribers"],
        "video_count": metrics["video_count"],
        "avg_recent_views": metrics["avg_recent_views"],
        "status": eval_res["status"],
        "mode_activated": eval_res["adaptations"]["mode"]
    }
    history_data["history"].append(entry)
    # Manter últimos 60 registros
    history_data["history"] = history_data["history"][-60:]
    history_data["current_status"] = eval_res["status"]
    history_data["last_updated"] = now_iso

    save_metrics_history(history_data)

    print("\n" + "=" * 65)
    print(">>> [LOOP DE RETROALIMENTAÇÃO: VIEWS DO CANAL]")
    print(f"Views Totais: {metrics['total_views']} | Média Recente: {metrics['avg_recent_views']:.1f} views")
    print(f"Status do Canal: {eval_res['status'].upper()} (Urgência: {eval_res['urgency_level']})")
    if eval_res["is_low"]:
        print(">>> [ALERTA: VIEWS BAIXAS DETECTADAS] Ativando MODO TRAÇÃO MÁXIMA / VIRAL BOOST:")
        for r in eval_res["recommendations"]:
            print(f"  • {r}")
    else:
        print(f">>> Canal operando em modo: {eval_res['adaptations']['mode']}")
    print("=" * 65 + "\n")

    return eval_res
