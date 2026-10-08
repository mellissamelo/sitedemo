"""Gera leads.csv e disparo.html a partir da lista de leads abaixo.

Uso: python3 gerar.py
Para adicionar leads, acrescente linhas em LEADS e rode de novo.
"""
import csv
import json
import html
from pathlib import Path
from urllib.parse import quote

AQUI = Path(__file__).parent

OFERTA = (
    "Vi que vocês ainda não têm um site próprio. "
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
    ("fisio", "Fisioclin Messejana", "Messejana · Rua Angélica Gurgel, 226", "5585994118007", "fisioclinmessejana", "https://www.instagram.com/fisioclinmessejana/", "Bio informa WhatsApp 99411-8007"),
    ("fisio", "SoulFisio – Studio de Pilates", "Messejana · Rua Capanema, 239", "5585997188859", "studiosoulfisio", "https://www.instagram.com/studiosoulfisio/", "Tem só página Wix gratuita — vender como upgrade"),
    ("fisio", "Studio de Pilates Vanessa Pires", "Fortaleza", "", "fisioterapeutavanessapires", "https://www.instagram.com/fisioterapeutavanessapires/", "WhatsApp está no link da bio — abrir o perfil"),
    ("fisio", "Viva Saúde Pilates", "Messejana", "", "vivasaudefisiopilates", "https://www.instagram.com/vivasaudefisiopilates/", "Sem número público — DM no Instagram"),
    ("fisio", "Clínica Intorce", "Fortaleza", "", "clinicaintorce", "https://www.instagram.com/clinicaintorce/", "Só fixo 85 3023-6393 — ligar ou DM"),
]

D9 = "Número antigo de 8 dígitos — 9 adicionado, confirmar"

# Lote 2 (busca de 08/10/2026 por bairro)
LEADS_LOTE2 = [
    ("petshop", "Isaac Estética Animal", "Aldeota · Rua Jorge da Rocha, 78", "5585987247708", "", "https://www.veterinarios.biz/sobre/dog-cat-pet-shop-veterinaria", D9),
    ("petshop", "Tia Kao Pet", "Meireles · Av. da Abolição, 3000", "5585994140025", "", "https://www.apontador.com.br/local/ce/fortaleza/pet_shops/NX8223SY/pet_shop_aldeota.html", D9),
    ("petshop", "Petit Pet Store", "Cambeba · Av. Viena Weyne, 195", "5585984350503", "", "https://petshoppertodemim.com/e/petit-pet-store-aineev/", "Outro número listado: 85 8929-7863"),
    ("petshop", "Docg Cambeba", "Cambeba · Rua Crisanto Moreira da Rocha, 1550", "5585997926780", "", "https://petshoppertodemim.com/e/docg-cambeba-advhpy/", ""),
    ("petshop", "Traquinas Pet Shop", "Cambeba", "5585997898510", "", "https://petshoppertodemim.com/e/traquinas-pet-shop-aquhgw/", ""),
    ("petshop", "Dubicho Pet Shop", "Bom Jardim · Av. Oscar Araripe, 549", "5585991279314", "", "https://petshoppertodemim.com/e/dubicho-pet-shop-anelhi/", ""),
    ("petshop", "Pet Show", "Antônio Bezerra · Rua Martins Neto, 618", "5585987174003", "", "https://petshoppertodemim.com/e/pet-show-rjgik/", ""),
    ("petshop", "Ray Pet Shop", "Antônio Bezerra · Rua Demétrio Menezes, 4093", "5585986078562", "", "https://www.apontador.com.br/local/ce/fortaleza/animais/C414190130033N033F/ray_pet_shop.html", ""),
    ("petshop", "Patas & Manhas", "Fátima · Rua Mário Mamede, 778 (tem unidade na Cid. dos Funcionários)", "5585991131139", "", "https://www.facebook.com/patasemanhas/", "Outro celular: 85 99103-0723"),
    ("petshop", "Petnerd", "Fortaleza", "5585994100112", "", "https://guia.fortal.br/pet-shops-em-fortaleza-ce/pagina95", D9),
    ("petshop", "Petshop Colares", "Bom Futuro", "5585994372556", "", "https://guia.fortal.br/pet-shops-em-fortaleza-ce/pagina95", D9),
    ("petshop", "PetStore", "Edson Queiroz · Av. Edilson Brasil Soares, 1720", "5585997042020", "clinicapetstore", "https://www.instagram.com/clinicapetstore/", "Pode ser a mesma Pet Store do Cidade 2000"),
    ("petshop", "Meu Vira Lata Clínica", "Edson Queiroz · Shopping Salinas", "5585985114218", "", "https://www.tutorcanino.com.br/guias/melhores-pet-shops-fortaleza", ""),
    ("petshop", "PetStop Maraponga", "Maraponga · Rua Francisco Glicério, 21 A", "5585992758197", "", "https://www.locaisdobrasil.com.br/encontre/pet-shop/fortaleza-ce/petstop-maraponga/619398edbd703e8618cf7653", "WhatsApp confirmado no guia"),
    ("petshop", "Pethome Pet Shop", "Maraponga · Av. Godofredo Maciel, 2640", "5585996762173", "", "https://petshoppertodemim.com/e/pethome-pet-shop-amvbre/", ""),
    ("petshop", "Realleza Pet", "Mondubim · Av. Benjamim Brasil, 1685", "5585997665306", "", "https://petshoppertodemim.com/e/realleza-pet-abmpru/", ""),
    ("petshop", "Farma Pet Passaré", "Passaré · Av. Dr. Silas Munguba, 5014", "5585986357332", "", "https://petshoppertodemim.com/e/animal-passare-ahfgee/", "Mesmo número da 'Animal Passaré'"),
    ("petshop", "Nosso Cantinho do Pet", "Joaquim Távora · Av. Antônio Sales, 746", "5585989946736", "", "https://petshoppertodemim.com/e/nosso-cantinho-do-pet-ayfnky/", ""),
    ("petshop", "A Rações", "Papicu · Av. Eng. Alberto Sá, 1464", "5585982150202", "", "https://www.diariocidade.com/ce/fortaleza/guia/pet-shop-e-veterinarios/", D9),
    ("petshop", "Toda Boa Pet", "Parquelândia · Rua Dom Manuel de Medeiros, 1117", "5585989293910", "", "https://guiapinzon.com.br/ce/fortaleza/parquelandia/pet-shop-em-parquelandia", ""),
    ("petshop", "Rações Patas e Pegadas", "Quintino Cunha · Rua Dona Lúcia Pinheiro, 2324", "5585999277774", "", "https://petshoppertodemim.com/pet-shop-em_quintino-cunha_fortaleza-ce/", ""),
    ("petshop", "Dog Mania", "Jangurussu · Rua Verde 35, 589", "5585989563714", "", "https://petshoppertodemim.com/e/dog-mania-tsiuu/", ""),
    ("petshop", "Amigos Pet", "Dias Macêdo · Rua Pedro Dantas, 504", "5585991509739", "", "https://www.apontador.com.br/em/dias-macedo-fortaleza-ce/animais", ""),
    ("petshop", "Preto Pet & Rações", "Serrinha", "5585988574966", "", "https://www.locaisdobrasil.com.br/encontre/pet-shop/serrinha/fortaleza-ce", ""),
    ("petshop", "Pet Shop Bons Amigos", "Vila Peri · Rua Mucuna, 87", "5585987193650", "", "https://petshoppertodemim.com/e/pet-shop-bons-amigos-arguqg/", ""),
    ("petshop", "Par de Patas Clínica Veterinária e Pet Shop", "Luciano Cavalcante · Rua Rev. Bolívar Pinto Bandeira, 136", "5585986300369", "", "https://petshoppertodemim.com/e/par-de-patas-clinica-veterinaria-e-pet-shop-cwshkj/", ""),
    ("petshop", "Doc Vet Clínica Veterinária", "Vila União · Rua Abel Garcia, 1055", "5585999800178", "", "https://www.guiamais.com.br/fortaleza-ce/serrinha/servicos-para-animais/pet-shop", ""),
    ("petshop", "Viana's Pet Shop", "Messejana · Av. Frei Cirilo, 3270, loja 19", "", "vianaspetshop", "https://www.instagram.com/vianaspetshop/", "Só fixo 85 3295-0999 — DM no Instagram"),
    ("fisio", "Clínica Recupera", "Messejana · Rua Santa Ângela, 120", "5585997930312", "", "https://fisioterapeutaspertodemim.com/e/clinica-recupera-aiuimc/", ""),
    ("fisio", "GCV Fisioterapia", "Parangaba · Rua D (Lot. Centro Sul), 81", "5585986851570", "", "https://www.solutudo.com.br/empresas/ce/fortaleza/fisioterapia", ""),
    ("fisio", "Elaine Liberato Fisioterapia", "Parangaba · Av. Gen. Osório de Paiva, 973", "5585987272285", "", "https://www.solutudo.com.br/empresas/ce/fortaleza/fisioterapia", "Profissional autônoma"),
    ("fisio", "Clínica Intense Fisio", "Mondubim · Av. Benjamim Brasil, 1685", "5585997714198", "", "https://www.solutudo.com.br/empresas/ce/fortaleza/fisioterapia", ""),
    ("fisio", "Falcão Fisioterapia", "Mondubim · Rua 08, Pq. São Mateus I, 45", "5585998233013", "", "https://www.solutudo.com.br/empresas/ce/fortaleza/fisioterapia", "Outro: 85 99826-5023"),
    ("fisio", "ConsultaFisio", "Prefeito José Walter · Rua 5, 147", "5585987464172", "", "https://wellhub.com/pt-br/search/partners/consultafisio-prefeito-jose-walter-fortaleza/", "Agenda só pelo WhatsApp"),
    ("fisio", "Fisioterapia em Movimento", "Passaré · Rua Oiticicas, 501", "5585991805839", "", "https://www.solutudo.com.br/empresas/ce/fortaleza/fisioterapia", ""),
    ("fisio", "Studio Along Pilates e Fisioterapia", "Passaré · Av. Heróis do Acre, 344", "5585981827886", "", "https://www.solutudo.com.br/empresas/ce/fortaleza/fisioterapia", ""),
    ("fisio", "Unifisio", "Aldeota · Rua Barbosa de Freitas, 1741", "5585988120997", "", "https://fisioterapeutaspertodemim.com/e/unifisio-servicos-de-fisioterapia-bubpzi/", ""),
    ("fisio", "Aline Moreira Fisioterapia", "Fátima · Av. Treze de Maio, 1383", "5585988353634", "", "https://www.guiatelefone.com/empresas/fortaleza-ce/clinicas-medicos-e-terapias/clinicas-de-fisioterapia", "Outro: 85 98826-5837"),
    ("fisio", "K Pilates Studio", "Cidade dos Funcionários · Rua Joãozito Arruda, 2315", "5585988994092", "", "https://localtreino.com/estudios-de-pilates/fortaleza/k-pilates-studio/", ""),
    ("fisio", "Realize Studio Pilates", "Edson Queiroz · Rua Eliseu Oriá, 376, loja 05", "5585999195132", "", "https://www.telelistas.net/ce/fortaleza/pilates", D9 + "; outro 85 98805-0755"),
    ("fisio", "Proximal Fisioterapia", "Domiciliar · Fortaleza e Caucaia", "5585994496838", "proximal_fisioterapia", "https://www.instagram.com/proximal_fisioterapia/", "Atende em casa — gancho: agendamento de visitas"),
    ("fisio", "CIF – Centro Integrado de Fisioterapia", "Aldeota · Av. Sen. Virgílio Távora, 1950 C", "558530454535", "", "https://xsteam.com.br/hub/fisioterapia/fisioterapi-em-fortaleza", "WhatsApp em número fixo"),
    ("fisio", "Larissa Fernandes Studio Pilates e Fisioterapia", "Messejana · Rua Santa Rosália, 33", "5585985881125", "", "https://www.solutudo.com.br/empresas/ce/fortaleza/fisioterapia", ""),
    ("fisio", "Roberta Lucatelli Fisioterapia e Pilates", "Messejana · Av. Mem de Sá, 430", "5585987203558", "", "https://www.solutudo.com.br/empresas/ce/fortaleza/fisioterapia", ""),
    ("fisio", "Vitality Pilates e Fisioterapia", "Maraponga · Av. Godofredo Maciel, 2290, sala 16", "5585996515199", "", "https://www.benditoguia.com.br/empresa/vitality-pilates-e-fisioterapia-maraponga-fortaleza-ce", ""),
    ("fisio", "Clínica Zelo Fisioterapia e Pilates", "Maraponga · Av. Godofredo Maciel, 2540", "5585998301248", "", "https://wellhub.com/pt-br/search/partners/clinica-zelo-fisioterapia-e-pilates-maraponga/", "Outro: 85 99944-6666"),
    ("fisio", "Imagem Corporal – Espaço de Pilates", "Parquelândia · Rua Érico Mota, 266", "5585985414344", "", "https://metacorpuspilates.com.br/studios/ceara/fortaleza/", "Outros: 85 99973-0089 / 98802-7521"),
    ("fisio", "Benefisio", "Itaperi · Av. Dr. Silas Munguba, 1518, loja 03", "5585986897991", "", "https://fisioterapeutaspertodemim.com/e/benefisio-clinica-de-estetica-e-fisioterapia-cskmfq/", ""),
    ("fisio", "Clínica Posturale", "Aldeota · Av. Santos Dumont, 3131", "5585996627770", "", "https://fisioterapeutaspertodemim.com/e/clinica-posturale-aljxsa/", ""),
    ("fisio", "Estação Fisio", "Papicu · Rua Valdetário Mota, 260", "5585997601040", "", "https://metacorpuspilates.com.br/studios/ceara/fortaleza/", ""),
]

# Número publicado pelo próprio negócio (bio, página, ficha de parceiro) é confiável.
# Guias montados a partir do CNPJ costumam trazer o número do contador ou um antigo.
FONTES_DO_NEGOCIO = ("instagram.com", "facebook.com", "sites.google.com", "wellhub.com", "google.com/maps", "maps.google")


def confianca(zap, fonte, obs):
    if not zap:
        return "dm"
    if D9 in obs or not any(d in fonte for d in FONTES_DO_NEGOCIO):
        return "baixa"
    return "alta"


def leads_do_maps():
    arq = AQUI / "places_leads.json"
    if not arq.exists():
        return []
    conhecidos = {l[3] for l in LEADS + LEADS_LOTE2 if l[3]}
    saida = []
    for p in json.loads(arq.read_text(encoding="utf-8")):
        if p["whatsapp"] in conhecidos:
            continue
        obs = f"Google Maps: nota {p['nota']} ({p['avaliacoes']} avaliações)" if p.get("nota") else "Google Maps"
        if p.get("rede_social"):
            obs += " · site na ficha é só rede social"
        saida.append((p["nicho"], p["nome"], p["local"], p["whatsapp"], "", p["maps"], obs, "maps"))
    return saida


LEADS = [(*l, 1) for l in LEADS] + [(*l, 2) for l in LEADS_LOTE2] + leads_do_maps()
LEADS = [(*l, confianca(l[3], l[5], l[6])) for l in LEADS]
LEADS.sort(key=lambda l: {"alta": 0, "baixa": 1, "dm": 2}[l[8]])
SELO = {
    "alta": ("ok", "✓ Número divulgado pelo próprio negócio"),
    "baixa": ("aviso", "⚠ Número de guia/CNPJ — pode estar errado; se não abrir, tente o Instagram"),
    "dm": ("dm", "Sem celular — contato pelo Instagram"),
}


def mensagem(nicho, nome):
    return f"Oi, {nome}! Tudo bem? {GANCHO[nicho]} {OFERTA}"


def main():
    with open(AQUI / "leads.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["nicho", "nome", "local", "whatsapp", "instagram", "fonte", "observacao", "link_whatsapp", "mensagem", "status", "lote", "confianca"])
        for nicho, nome, local, zap, ig, fonte, obs, lote, conf in LEADS:
            msg = mensagem(nicho, nome)
            link = f"https://wa.me/{zap}?text={quote(msg)}" if zap else ""
            w.writerow([nicho, nome, local, zap, f"@{ig}" if ig else "", fonte, obs, link, msg, "a contatar", lote, conf])

    cards = []
    for i, (nicho, nome, local, zap, ig, fonte, obs, lote, conf) in enumerate(LEADS):
        msg = mensagem(nicho, nome)
        e = html.escape
        botoes = []
        if zap:
            botoes.append(f'<a class="btn zap" target="_blank" href="https://wa.me/{zap}?text={quote(msg)}">Abrir WhatsApp</a>')
        if ig:
            botoes.append(f'<a class="btn" target="_blank" href="https://ig.me/m/{ig}">DM Instagram</a>')
        botoes.append(f'<button class="btn" onclick="copiar({i})">Copiar mensagem</button>')
        botoes.append(f'<label class="feito"><input type="checkbox" data-id="{e(nome)}"> enviado</label>')
        cards.append(f"""
<article class="card" data-nicho="{nicho}" data-lote="{lote}" data-conf="{conf}">
  <div class="tag {nicho}">{"Pet shop" if nicho == "petshop" else "Fisioterapia"}</div> <div class="tag">Lote {lote}</div>
  <h3>{e(nome)}</h3>
  <p class="meta">{e(local)}{" · @" + e(ig) if ig else ""}{" · +" + zap if zap else ""}</p>
  <p class="selo {SELO[conf][0]}">{SELO[conf][1]}</p>
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
.tag.fisio{{background:#c5a46a44}}.selo{{font-size:12px;font-weight:600;margin:6px 0}}.selo.ok{{color:#1fae5b}}.selo.aviso{{color:#c77d00}}.selo.dm{{color:var(--mut)}}.acoes{{display:flex;flex-wrap:wrap;gap:6px;align-items:center}}
.btn{{border:1px solid var(--ac);color:var(--ac);background:none;padding:6px 10px;border-radius:99px;font-size:13px;text-decoration:none;cursor:pointer}}
.btn.zap{{background:var(--zap);border-color:var(--zap);color:#fff}}.feito{{font-size:13px;color:var(--mut)}}
</style></head><body><main>
<h1>Prospecção: sites R$ 350 em 7 dias</h1>
<p class="sub">{len(LEADS)} leads em Fortaleza sem site próprio encontrado, {sum(l[8] == "alta" for l in LEADS)} com número confiável (aparecem primeiro). Clique em <b>Abrir WhatsApp</b>, a mensagem já vai preenchida. Depois anexe as imagens abaixo (o link do WhatsApp não anexa imagens sozinho).</p>
<div class="demos"><img src="img/demo-petshop-1.jpg" alt="Demo pet shop"><img src="img/demo-petshop-2.jpg" alt="Demo pet shop serviços"><img src="img/demo-dentista-1.jpg" alt="Demo dentista"><img src="img/demo-dentista-2.jpg" alt="Demo dentista serviços"></div>
<div class="filtros"><button class="btn" onclick="filtrar('')">Todos</button><button class="btn" onclick="filtrar('petshop')">Pet shops</button><button class="btn" onclick="filtrar('fisio')">Fisioterapia</button><button class="btn" onclick="filtrarConf('alta')">Só números confiáveis</button><button class="btn" onclick="filtrarLote('maps')">Google Maps</button><button class="btn" onclick="filtrarLote('1')">Lote 1</button><button class="btn" onclick="filtrarLote('2')">Lote 2</button></div>
<section class="grid">{"".join(cards)}</section>
</main><script>
function copiar(i){{navigator.clipboard.writeText(document.getElementById('m'+i).innerText)}}
function filtrarConf(c){{document.querySelectorAll('.card').forEach(x=>x.style.display=x.dataset.conf===c?'':'none')}}
function filtrarLote(l){{document.querySelectorAll('.card').forEach(c=>c.style.display=c.dataset.lote===l?'':'none')}}
function filtrar(n){{document.querySelectorAll('.card').forEach(c=>c.style.display=!n||c.dataset.nicho===n?'':'none')}}
document.querySelectorAll('[data-id]').forEach(cb=>{{let k='lead'+cb.dataset.id;try{{cb.checked=localStorage.getItem(k)==='1'}}catch(e){{}}
cb.closest('.card').classList.toggle('ok',cb.checked);cb.onchange=()=>{{try{{localStorage.setItem(k,cb.checked?'1':'0')}}catch(e){{}}cb.closest('.card').classList.toggle('ok',cb.checked)}}}})
</script></body></html>"""
    (AQUI / "disparo.html").write_text(pagina, encoding="utf-8")
    print(f"{len(LEADS)} leads -> leads.csv, disparo.html")


if __name__ == "__main__":
    main()
