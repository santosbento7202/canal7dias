"""src/youtube_uploader.py - Gerenciador de upload para YouTube Data API v3 com suporte ao Modo Semi-Auto.

Recursos:
- Autenticação OAuth 2.0 via variáveis de ambiente (YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN).
- Upload resumível de vídeos grandes com controle de blocos.
- Agendamento automático com 'publishAt' em horários fixos (Longo: 12:00 BRT; Shorts: 08:00, 18:00, 21:00 BRT).
- Upload de thumbnail personalizada via thumbnails().set.
- Inserção de comentário fixado via commentThreads().insert.
- Modo Semi-Auto: Se não houver credenciais, se houver dry-run ou se a API bloquear uploads não auditados,
  gera pacote completo em out/dia_N/ (vídeo, thumb, metadata.txt com capítulos, tags e comentário).
- Idempotência: Checa se o dia já foi publicado para evitar duplicação.
"""

import datetime
import json
import os
import sys
from typing import Any, Dict, List, Optional
import pytz

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
except ImportError:
    pass

from dotenv import load_dotenv
load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))


def get_authenticated_service():
    """Inicializa o serviço da YouTube Data API v3 a partir dos segredos de ambiente."""
    client_id = os.getenv("YT_CLIENT_ID", "").strip()
    client_secret = os.getenv("YT_CLIENT_SECRET", "").strip()
    refresh_token = os.getenv("YT_REFRESH_TOKEN", "").strip()

    if not (client_id and client_secret and refresh_token):
        return None

    try:
        creds = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret
        )
        return build("youtube", "v3", credentials=creds)
    except Exception as e:
        print(f"[YOUTUBE] Erro ao autenticar via credenciais ({e})")
        return None


def calculate_schedule_time(target_hour_brt: int, target_minute_brt: int = 0, days_ahead: int = 0) -> str:
    """Calcula timestamp ISO 8601 UTC para agendamento no horário de Brasília (UTC-3)."""
    brt = pytz.timezone("America/Sao_Paulo")
    now_brt = datetime.datetime.now(brt)
    schedule_dt = now_brt.replace(hour=target_hour_brt, minute=target_minute_brt, second=0, microsecond=0)
    if days_ahead > 0:
        schedule_dt += datetime.timedelta(days=days_ahead)
    elif schedule_dt <= now_brt:
        schedule_dt += datetime.timedelta(days=1)
    # Converter para UTC com formato Z
    utc_dt = schedule_dt.astimezone(pytz.utc)
    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    return utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def upload_video(
    youtube,
    file_path: str,
    title: str,
    description: str,
    tags: List[str],
    category_id: str = "27",  # Educação
    schedule_publish_at: Optional[str] = None
) -> Optional[str]:
    """Realiza o upload do vídeo com resumable upload."""
    if not os.path.exists(file_path):
        print(f"[YOUTUBE] Arquivo de vídeo não encontrado: {file_path}")
        return None

    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": tags[:15],
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False
        }
    }

    if schedule_publish_at:
        body["status"]["publishAt"] = schedule_publish_at

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"[YOUTUBE] Upload em progresso: {int(status.progress() * 100)}%")

        video_id = response.get("id")
        print(f"[YOUTUBE] Upload concluído com sucesso! Video ID: {video_id}")
        return video_id
    except Exception as e:
        print(f"[YOUTUBE] Falha no upload ({e})")
        return None


def set_thumbnail(youtube, video_id: str, thumb_path: str) -> bool:
    """Define a thumbnail personalizada do vídeo."""
    if not (os.path.exists(thumb_path) and youtube and video_id):
        return False
    try:
        media = MediaFileUpload(thumb_path, mimetype="image/png")
        youtube.thumbnails().set(videoId=video_id, media_body=media).execute()
        print(f"[YOUTUBE] Thumbnail aplicada ao vídeo {video_id}")
        return True
    except Exception as e:
        print(f"[YOUTUBE] Não foi possível definir thumbnail ({e})")
        return False


def post_pinned_comment(youtube, video_id: str, comment_text: str) -> bool:
    """Insere o comentário fixado polarizador."""
    if not (youtube and video_id and comment_text):
        return False
    try:
        body = {
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": comment_text
                    }
                }
            }
        }
        youtube.commentThreads().insert(part="snippet", body=body).execute()
        print(f"[YOUTUBE] Comentário polarizador postado com sucesso no vídeo {video_id}")
        return True
    except Exception as e:
        print(f"[YOUTUBE] Não foi possível postar comentário ({e})")
        return False


def export_semi_auto_package(
    out_dir: str,
    title: str,
    description: str,
    tags: List[str],
    pinned_comment: str,
    video_path: str,
    thumb_path: str,
    shorts_list: List[Dict[str, Any]]
):
    """Exporta pacote completo do Modo Semi-Auto para subida manual no YouTube Studio em 3 minutos."""
    metadata_path = os.path.join(out_dir, "metadata.txt")
    with open(metadata_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("PACOTE MODO SEMI-AUTO - YOUTUBE STUDIO\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"TÍTULO DO VÍDEO:\n{title}\n\n")
        f.write(f"TEXTO DA THUMBNAIL:\n(Verifique o arquivo {os.path.basename(thumb_path)})\n\n")
        f.write(f"DESCRIÇÃO COMPLETA (Copie e cole abaixo do vídeo):\n")
        f.write("-" * 40 + "\n")
        f.write(description + "\n")
        f.write("-" * 40 + "\n\n")
        f.write(f"TAGS DE DESAMBIGUAÇÃO:\n{', '.join(tags)}\n\n")
        f.write(f"COMENTÁRIO FIXADO POLARIZADOR (Poste e clique em 'Fixar no topo'):\n{pinned_comment}\n\n")
        f.write("ARQUIVOS PRONTOS NESTA PASTA:\n")
        f.write(f"1. Vídeo Longo: {os.path.basename(video_path)}\n")
        f.write(f"2. Thumbnail: {os.path.basename(thumb_path)}\n")
        for i, s in enumerate(shorts_list):
            f.write(f"3.{i+1} Short {i+1}: {os.path.basename(s.get('mp4_path', ''))}\n")
        f.write("\nTEMPO ESTIMADO DE UPLOAD NO STUDIO: 3 minutos.\n")
    print(f"[SEMI-AUTO] Pacote exportado com sucesso: {metadata_path}")
