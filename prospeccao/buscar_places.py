"""Busca leads no Google Maps pela API oficial do Google Places (mesma fonte do ProspectOS).

O telefone vem da ficha do Google Meu Negócio, que o próprio dono mantém, então é
bem mais confiável que guias montados a partir do CNPJ. A ficha também diz se o
negócio tem site, então "sem site" deixa de ser chute.

Uso:
    export PLACES_API_KEY=suachave
    python3 buscar_places.py              # todos os bairros da lista
    python3 buscar_places.py Messejana    # só um bairro

Gera places_leads.json, que o gerar.py inclui automaticamente na página.
Chave: https://console.cloud.google.com/apis/library/places.googleapis.com
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

AQUI = Path(__file__).parent
SAIDA = AQUI / "places_leads.json"
URL = "https://places.googleapis.com/v1/places:searchText"
CAMPOS = ",".join(f"places.{c}" for c in [
    "id", "displayName", "formattedAddress", "nationalPhoneNumber",
    "websiteUri", "businessStatus", "rating", "userRatingCount", "googleMapsUri",
]) + ",nextPageToken"

NICHOS = {"petshop": "pet shop", "fisio": "clínica de fisioterapia", "consultoria": "consultoria empresarial"}

BAIRROS = [
    "Aldeota", "Meireles", "Dionísio Torres", "Papicu", "Cocó", "Varjota", "Joaquim Távora",
    "Fátima", "Benfica", "Montese", "Parquelândia", "Antônio Bezerra", "Barra do Ceará",
    "Álvaro Weyne", "Quintino Cunha", "Henrique Jorge", "João XXIII", "Bom Jardim",
    "Conjunto Ceará", "Granja Portugal", "Siqueira", "Mondubim", "Maraponga",
    "Jardim Cearense", "Parangaba", "Itaperi", "Serrinha", "Vila Peri", "Passaré",
    "Jangurussu", "Messejana", "Cambeba", "Lagoa Redonda", "Sapiranga", "Edson Queiroz",
    "Cidade dos Funcionários", "Cajazeiras", "Prefeito José Walter", "Dias Macêdo",
]

# Link de rede social no campo "site" não é site de verdade: continua sendo lead.
NAO_E_SITE = re.compile(r"instagram\.com|facebook\.com|wa\.me|whatsapp\.com|linktr\.ee|linkbio|bio\.link|beacons\.ai", re.I)


def consultar(chave, corpo):
    req = urllib.request.Request(
        URL, data=json.dumps(corpo).encode(), method="POST",
        headers={"Content-Type": "application/json", "X-Goog-Api-Key": chave, "X-Goog-FieldMask": CAMPOS},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Erro da API ({e.code}): {e.read().decode()[:300]}")


def celular(telefone):
    """'(85) 99637-6074' -> '5585996376074'; None se for fixo ou de outro DDD."""
    d = re.sub(r"\D", "", telefone or "")
    if len(d) == 11 and d.startswith("85") and d[2] == "9":
        return "55" + d
    return None


def buscar(chave, nicho, bairro):
    corpo = {"textQuery": f"{NICHOS[nicho]} em {bairro}, Fortaleza - CE", "languageCode": "pt-BR",
             "regionCode": "BR", "pageSize": 20}
    for _ in range(3):  # a API devolve no máximo 60 resultados por busca
        resp = consultar(chave, corpo)
        yield from resp.get("places", [])
        if not resp.get("nextPageToken"):
            break
        corpo["pageToken"] = resp["nextPageToken"]
        time.sleep(2)


def main():
    chave = os.environ.get("PLACES_API_KEY") or sys.exit("Defina PLACES_API_KEY (veja o topo do arquivo).")
    bairros = sys.argv[1:] or BAIRROS
    leads = {l["id"]: l for l in json.loads(SAIDA.read_text(encoding="utf-8"))} if SAIDA.exists() else {}
    for bairro in bairros:
        for nicho in NICHOS:
            novos = 0
            for p in buscar(chave, nicho, bairro):
                site = p.get("websiteUri", "")
                zap = celular(p.get("nationalPhoneNumber"))
                if p.get("businessStatus", "OPERATIONAL") != "OPERATIONAL" or not zap:
                    continue
                if site and not NAO_E_SITE.search(site):
                    continue
                if p["id"] not in leads:
                    novos += 1
                leads[p["id"]] = {
                    "id": p["id"], "nicho": nicho, "nome": p["displayName"]["text"],
                    "local": p.get("formattedAddress", "").replace(", Fortaleza - CE", "").split(", 6")[0],
                    "whatsapp": zap, "rede_social": site, "nota": p.get("rating"),
                    "avaliacoes": p.get("userRatingCount", 0), "maps": p.get("googleMapsUri", ""),
                }
            print(f"{bairro:<25} {NICHOS[nicho]:<25} +{novos}")
    SAIDA.write_text(json.dumps(list(leads.values()), ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(leads)} leads em {SAIDA.name}. Rode python3 gerar.py para atualizar a página.")


if __name__ == "__main__":
    main()
