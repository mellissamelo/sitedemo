"""Gera leads.csv e disparo.html a partir da lista de leads abaixo.

Uso: python3 gerar.py
Para adicionar leads, acrescente linhas em LEADS e rode de novo.
"""
import csv
import html
from pathlib import Path
from urllib.parse import quote

AQUI = Path(__file__).parent

OFERTA = (
    "Vi que vocês ainda não têm um site próprio, só o perfil nas redes. "
    "Eu crio sites profissionais com agendamento online e botão direto pro WhatsApp "
    "de vocês, pronto em 7 dias, por R$ 350 (pagamento único). "
    "Te mandei aqui embaixo dois sites que fiz recentemente pra você ver o padrão. "
    "Posso montar uma prévia com o nome e as fotos de vocês, sem compromisso?"
)

GANCHO = {
    "petshop": "Seus clientes poderiam marcar banho, tosa e consulta direto pelo site, 24h.",
    "fisio": "Seus pacientes poderiam agendar avaliação e sessões direto pelo site, 24h.",
}

# nicho, nome, bairro/endereço, whatsapp (só dígitos, com 55+DDD) ou "", instagram, fonte, observação
LEADS = [
    ("petshop", "Pet Shop Fazendinha", "Sítio São João · Av. Val Paraíso, 1050", "5585996376074", "petshopafazendinha", "https://www.instagram.com/petshopafazendinha/", "Também tem 85 98956-3447"),
    ("petshop", "Clínica e PetShop Bicharada", "Fortaleza", "5585991071438", "petshopbicharada", "https://www.instagram.com/petshopbicharada/", "Fixo 85 3271-1625"),
    ("petshop", "Pet Shop Bicharada", "Cidade dos Funcionários · Av. Oliveira Paiva, 1930", "5585988678426", "", "https://petshoppertodemim.com/e/pet-shop-bicharada-aqisey/", "Pode ser a mesma marca do lead acima — mande só para um"),
    ("petshop", "My Pett", "Pet shop móvel (atende em casa)", "5585986652242", "mypett", "https://www.instagram.com/mypett/", ""),
    ("petshop", "Pet Pegada Banho e Tosa", "Prefeito José Walter", "5585998527714", "", "https://petshoppertodemim.com/e/pet-pegada-banho-e-tosa-bfzora/", "Número de diretório — confirmar"),
    ("petshop", "Pet Shop Mondubim", "Mondubim · Rua 1, 1369", "5585988779328", "", "https://petshoppertodemim.com/e/pet-shop-mondubim-aoxjjf/", ""),
    ("petshop", "Pet Shop Pit Bull Banho e Tosa", "Rua 25, 155", "5585986266685", "", "https://www.facebook.com/Betebanhoetosa/", "Só Facebook"),
    ("petshop", "Pet Shop Planeta Animal", "Av. Dr. Silas Munguba, 1299", "5585997358362", "", "https://www.facebook.com/planetaanimal.ce/", "Só Facebook"),
    ("petshop", "Pet Center Vira Lata", "Montese · Av. Alberto Magno, 190", "5585986065088", "", "https://sites.google.com/view/petcenterviralata/home", "Tem só página gratuita do Google Sites — vender como upgrade"),
    ("petshop", "Pet Veras", "Parangaba · Shopping Redmall", "", "petveras_", "https://www.instagram.com/petveras_/", "Sem número público — mandar DM no Instagram"),
    ("petshop", "Clubinho Pet", "Av. Carapinima, 2200", "", "clubinhopet01", "https://www.instagram.com/clubinhopet01/", "Sem número público — mandar DM no Instagram"),
    ("fisio", "Clínica CostaPorto", "Aldeota · Av. Des. Moreira, 1300, sala 420", "5585997502773", "clinicareabilitacaocostaporto", "https://www.instagram.com/clinicareabilitacaocostaporto/", ""),
    ("fisio", "Fisioclin Messejana", "Messejana · Rua Angélica Gurgel, 226", "5585994118007", "fisioclinmessejana", "https://www.instagram.com/fisioclinmessejana/", "Bio informa WhatsApp 99411-8007"),
    ("fisio", "SoulFisio – Studio de Pilates", "Messejana · Rua Capanema, 239", "5585997188859", "studiosoulfisio", "https://www.instagram.com/studiosoulfisio/", ""),
    ("fisio", "Studio de Pilates Vanessa Pires", "Fortaleza", "", "fisioterapeutavanessapires", "https://www.instagram.com/fisioterapeutavanessapires/", "WhatsApp está no link da bio — abrir o perfil"),
    ("fisio", "Viva Saúde Pilates", "Messejana", "", "vivasaudefisiopilates", "https://www.instagram.com/vivasaudefisiopilates/", "Sem número público — DM no Instagram"),
    ("fisio", "Multiclínica Fortaleza", "Parangaba · Rua Guaratinguetá, 60", "", "multiclinicafortaleza", "https://www.instagram.com/multiclinicafortaleza/", "WhatsApp do diretor técnico na bio"),
    ("fisio", "Clínica Intorce", "Fortaleza", "", "clinicaintorce", "https://www.instagram.com/clinicaintorce/", "Só fixo 85 3023-6393 — ligar ou DM"),
    ("fisio", "ITD – Instituto de Tratamento da Dor", "Dionísio Torres · R. Henriqueta Galeno, 521", "", "itd_brasil", "https://www.instagram.com/itd_brasil/", "Sem número público — DM no Instagram"),
]


def mensagem(nicho, nome):
    return f"Oi, {nome}! Tudo bem? {GANCHO[nicho]} {OFERTA}"


def main():
    with open(AQUI / "leads.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["nicho", "nome", "local", "whatsapp", "instagram", "fonte", "observacao", "link_whatsapp", "mensagem", "status"])
        for nicho, nome, local, zap, ig, fonte, obs in LEADS:
            msg = mensagem(nicho, nome)
            link = f"https://wa.me/{zap}?text={quote(msg)}" if zap else ""
            w.writerow([nicho, nome, local, zap, f"@{ig}" if ig else "", fonte, obs, link, msg, "a contatar"])

    cards = []
    for i, (nicho, nome, local, zap, ig, fonte, obs) in enumerate(LEADS):
        msg = mensagem(nicho, nome)
        e = html.escape
        botoes = []
        if zap:
            botoes.append(f'<a class="btn zap" target="_blank" href="https://wa.me/{zap}?text={quote(msg)}">Abrir WhatsApp</a>')
        if ig:
            botoes.append(f'<a class="btn" target="_blank" href="https://ig.me/m/{ig}">DM Instagram</a>')
        botoes.append(f'<button class="btn" onclick="copiar({i})">Copiar mensagem</button>')
        botoes.append(f'<label class="feito"><input type="checkbox" data-id="{i}"> enviado</label>')
        cards.append(f"""
<article class="card" data-nicho="{nicho}">
  <div class="tag {nicho}">{"Pet shop" if nicho == "petshop" else "Fisioterapia"}</div>
  <h3>{e(nome)}</h3>
  <p class="meta">{e(local)}{" · @" + e(ig) if ig else ""}{" · +" + zap if zap else ""}</p>
  {f'<p class="obs">{e(obs)}</p>' if obs else ""}
  <p class="msg" id="m{i}">{e(msg)}</p>
  <div class="acoes">{"".join(botoes)}</div>
  <p class="fonte"><a target="_blank" href="{e(fonte)}">fonte</a></p>
</article>""")

    pagina = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Disparo de Leads</title>
<style>
:root{{--bg:#f6f4ef;--card:#fff;--tx:#1d2b24;--mut:#6b7570;--ac:#1f4535;--zap:#1fae5b;--bd:#e4e0d6}}
@media (prefers-color-scheme:dark){{:root{{--bg:#141816;--card:#1d2420;--tx:#e8ece9;--mut:#9aa5a0;--ac:#7fc4a2;--bd:#2c3530}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--tx);font:15px/1.5 system-ui,sans-serif}}
main{{max-width:1100px;margin:auto;padding:24px 16px}}h1{{margin:0 0 4px}}.sub{{color:var(--mut);margin:0 0 20px}}
.demos{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin-bottom:20px}}
.demos img{{width:100%;border-radius:10px;border:1px solid var(--bd)}}
.filtros button{{margin-right:6px}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px;margin-top:14px}}
.card{{background:var(--card);border:1px solid var(--bd);border-radius:14px;padding:16px}}.card.ok{{opacity:.5}}
.card h3{{margin:6px 0 2px}}.meta,.fonte{{color:var(--mut);font-size:13px;margin:0}}.obs{{font-size:13px;background:#f3c96b33;padding:4px 8px;border-radius:6px}}
.msg{{font-size:13px;background:var(--bg);padding:10px;border-radius:8px}}.tag{{display:inline-block;font-size:11px;font-weight:600;padding:2px 8px;border-radius:99px;background:#5aa3d633}}
.tag.fisio{{background:#c5a46a44}}.acoes{{display:flex;flex-wrap:wrap;gap:6px;align-items:center}}
.btn{{border:1px solid var(--ac);color:var(--ac);background:none;padding:6px 10px;border-radius:99px;font-size:13px;text-decoration:none;cursor:pointer}}
.btn.zap{{background:var(--zap);border-color:var(--zap);color:#fff}}.feito{{font-size:13px;color:var(--mut)}}
</style></head><body><main>
<h1>Prospecção: sites R$ 350 em 7 dias</h1>
<p class="sub">{len(LEADS)} leads em Fortaleza sem site próprio encontrado. Clique em <b>Abrir WhatsApp</b>, a mensagem já vai preenchida. Depois anexe as imagens abaixo (o link do WhatsApp não anexa imagens sozinho).</p>
<div class="demos"><img src="img/demo-petshop-1.jpg" alt="Demo pet shop"><img src="img/demo-petshop-2.jpg" alt="Demo pet shop serviços"><img src="img/demo-dentista-1.jpg" alt="Demo dentista"><img src="img/demo-dentista-2.jpg" alt="Demo dentista serviços"></div>
<div class="filtros"><button class="btn" onclick="filtrar('')">Todos</button><button class="btn" onclick="filtrar('petshop')">Pet shops</button><button class="btn" onclick="filtrar('fisio')">Fisioterapia</button></div>
<section class="grid">{"".join(cards)}</section>
</main><script>
function copiar(i){{navigator.clipboard.writeText(document.getElementById('m'+i).innerText)}}
function filtrar(n){{document.querySelectorAll('.card').forEach(c=>c.style.display=!n||c.dataset.nicho===n?'':'none')}}
document.querySelectorAll('[data-id]').forEach(cb=>{{let k='lead'+cb.dataset.id;try{{cb.checked=localStorage.getItem(k)==='1'}}catch(e){{}}
cb.closest('.card').classList.toggle('ok',cb.checked);cb.onchange=()=>{{try{{localStorage.setItem(k,cb.checked?'1':'0')}}catch(e){{}}cb.closest('.card').classList.toggle('ok',cb.checked)}}}})
</script></body></html>"""
    (AQUI / "disparo.html").write_text(pagina, encoding="utf-8")
    print(f"{len(LEADS)} leads -> leads.csv, disparo.html")


if __name__ == "__main__":
    main()
