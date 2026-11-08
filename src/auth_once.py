"""src/auth_once.py - Script executado localmente uma única vez para autenticar OAuth do YouTube.

Gera:
- YT_CLIENT_ID
- YT_CLIENT_SECRET
- YT_REFRESH_TOKEN

Instruções:
1. Crie as credenciais OAuth 2.0 (Aplicativo para Computador) no Google Cloud Console.
2. Baixe o client_secret.json e coloque nesta pasta ou informe o caminho.
3. Execute: python src/auth_once.py --client-secrets client_secret.json
4. O navegador abrirá para autorização. Conceda permissão total para gerenciar o YouTube.
5. Copie os 3 valores exibidos no terminal e cole nos GitHub Secrets do repositório.
"""

import argparse
import json
import os
import sys

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("Execute: pip install google-auth-oauthlib google-api-python-client")
    sys.exit(1)

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube"
]


def main():
    parser = argparse.ArgumentParser(description="Autenticação OAuth única do YouTube.")
    parser.add_argument("--client-secrets", default="client_secret.json", help="Arquivo client_secret.json baixado do Google Cloud")
    args = parser.parse_args()

    if not os.path.exists(args.client_secrets):
        print(f"Erro: Arquivo '{args.client_secrets}' não encontrado.")
        print("Siga o passo a passo em SETUP_CANAL.md para baixar o client_secret.json.")
        sys.exit(1)

    with open(args.client_secrets, "r", encoding="utf-8") as f:
        secret_data = json.load(f)

    # Identificar cliente instalado ou web
    app_type = "installed" if "installed" in secret_data else "web"
    client_id = secret_data[app_type]["client_id"]
    client_secret = secret_data[app_type]["client_secret"]

    flow = InstalledAppFlow.from_client_secrets_file(args.client_secrets, SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")

    print("\n" + "=" * 60)
    print("AUTENTICAÇÃO CONCLUÍDA COM SUCESSO!")
    print("Copie as variáveis abaixo para os GitHub Secrets do repositório:")
    print("=" * 60)
    print(f"YT_CLIENT_ID={client_id}")
    print(f"YT_CLIENT_SECRET={client_secret}")
    print(f"YT_REFRESH_TOKEN={creds.refresh_token}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
