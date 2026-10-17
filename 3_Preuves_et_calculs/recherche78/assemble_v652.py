"""Assembler le corpus récupéré, sans prétendre restaurer les sources absentes."""
from pathlib import Path
import argparse,copy,html,importlib.util,json,re,shutil,subprocess,sys
from urllib.parse import unquote,urlsplit
from html.parser import HTMLParser

S77="77_MECANISMES_POUR_LE_SIGNE_UNIVERSEL"
S78="78_TRANSPORT_POSITIF_RESERVE_ET_BRIQUE_INITIALE"
RESULT=("Transport positif : sommation compatible, pont stock–Fenchel et première "
        "ligne non minimale encadrée sans RH. Diagnostics jusqu’à1000. Loi globale du signe ouverte.")

def mod(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m

def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

class Links(HTMLParser):
    def __init__(self):super().__init__();self.values=[]
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ("href","src") and v:self.values.append(v)

def check(root,pages):
    missing=[];count=0;dynamic=0
    for rel in pages:
        path=root/rel;p=Links();p.feed(path.read_text(encoding="utf-8-sig"))
        for raw in p.values:
            u=urlsplit(raw)
            if u.scheme or u.netloc or not u.path:continue
            if "$"+"{" in raw or "<" in raw or "{" in raw:dynamic+=1;continue
            count+=1;target=(path.parent/unquote(u.path)).resolve()
            if not target.exists():missing.append(dict(page=rel,href=raw,target=str(target.relative_to(root))))
    return missing,count,dynamic

def main(root,work):
    root=root.resolve();work=work.resolve();P=root/"1_Presentation";D=root/"3_Preuves_et_calculs/data"
    state=json.loads((D/"v651_etat_recherche.json").read_text(encoding="utf-8-sig"))
    state.update(version="V6.52",date="2026-10-14",result=RESULT,document=S78+".pdf",graph=S78+".html",
      global_sign_certified=False,maturity_levels_unchanged=True,complete_historical_recovery=False,
      current_protocol="v652_protocole_transport.json",next_actions=[
        "Construire les lignes non minimales suivantes avec bilans exacts.",
        "Imposer l’admissibilité à tous les rangs par une loi arithmétique indépendante.",
        "Conserver les lignes validées et rouvrir honnêtement le bord.",
        "Couvrir toutes les échelles sans plancher positif uniforme."])
    state["new_auxiliary_proofs"]=dict(countable_subcoupling_suffices=True,radial_stock_fenchel_link=True,
      initial_nonminimal_line_interval_verified=True,unconditional_global_arithmetic_sign=False)
    write(D/"v652_etat_recherche.json",state)
    write(D/"v652_protocole_transport.json",dict(target="Weil positivity via the specific Suzuki scalar bridge",
      RH_proved=False,global_sign_certified=False,finite_prime_power_cutoff=1000,
      invariant="positive residual; exact mass and first moment in each line",
      open_obligation="admissibility of every future arithmetic demand",
      forbidden_inference="finite closure atom equals actual future prime atoms",source_recovery_complete=False))
    for name in [S78+".md",S78+".tex",S78+".pdf","78_CARTE_TRANSPORT.png","78_CARTE_TRANSPORT.svg",S77+".md"]:
        shutil.copy2(work/name,P/name)
    rec=json.loads((root/"RECUPERATION_2026_10_14.json").read_text())
    rec["explicit_later_missing_references"]=[
      "3_Preuves_et_calculs/scripts/v650_support_transport_experiment.py",
      "3_Preuves_et_calculs/scripts/v651_verifier_pistes_globales.py",
      "3_Preuves_et_calculs/data/v651_pistes_globales_resultats.json"]
    note=("# Récupération du corpus - 14 octobre2026\n\n"
      "L’ancien ZIP V6.51 est incomplet : absence de répertoire central,803 entrées locales "
      "complètes seulement. Leurs données ont été vérifiées par CRC.\n\n"
      "Les documents de présentation récents, leurs PDF et LaTeX, et les pages du portail "
      "ont été récupérés. Les fichiers plus anciens disponibles et quinze résultats "
      "enregistrés séparément ont été ajoutés. Ce n’est pas une récupération intégrale "
      "des1321 éléments annoncés auparavant.\n\n"
      "Les expériences nouvelles de recherche78 sont reproductibles. Certains scripts "
      "scientifiques antérieurs ne sont pas récupérés ; leurs anciens résultats ne sont "
      "pas présentés comme rejoués dans cette version.\n\n"
      "RECUPERATION_2026_10_14.json conserve la provenance.\n\n## Pièces indisponibles\n\n")
    note+="\n".join("- "+p for p in rec["missing_source_paths_from_v649_index"]+rec["explicit_later_missing_references"])+"\n"
    def recovery_page():
        (root/"RECUPERATION.md").write_text(note,encoding="utf-8-sig")
        subprocess.run(["pandoc","RECUPERATION.md","-s","--metadata","lang=fr","-o","RECUPERATION.html"],cwd=root,check=True)
    recovery_page()
    navpath=root/"2_Methode/Indicateur/build_indicateur.py";t=navpath.read_text(encoding="utf-8-sig")
    if '"transport", "Transport positif"' not in t:
        entries=('("transport", "Transport positif", "1_Presentation/'+S78+'.html"), '
                 '("signe", "Signe global", "1_Presentation/'+S77+'.html"), ')
        t=t.replace("pages = [","pages = ["+entries,1)
    t=t.replace("data/v651_etat_recherche.json","data/v652_etat_recherche.json")
    t=t.replace('href = prefix + "1_Presentation/76_RECONSTRUIRE_LA_PISTE_GLOBALE_DE_WEIL.html"',
                'href = prefix + "1_Presentation/'+S78+'.html"')
    t=t.replace('data-current="v651"','data-current="v652"').replace("État courant V6.51.","État courant V6.52.")
    old="Les résultats datés de cette page conservent leur portée.</aside>"
    new='Les résultats datés conservent leur portée. <a href="'+"' + prefix + '"+'RECUPERATION.html">Récupération partielle des sources historiques</a>.</aside>'
    t=t.replace(old,new);navpath.write_text(t,encoding="utf-8")
    nav=mod("nav652",navpath);old=mod("active650",root/"2_Methode/Outils/build_v650.py")
    active=old.ACTIVE+["1_Presentation/75_RECUPERATION_TRANSPORT_ET_RH.html",
                       "1_Presentation/76_RECONSTRUIRE_LA_PISTE_GLOBALE_DE_WEIL.html"]
    assert len(active)==18
    for rel in active:
        path=root/rel;t=path.read_text(encoding="utf-8-sig");prefix="" if path.parent==root else "../"
        t=re.sub(r'<aside data-current="v65[012]".*?</aside>',"",t,flags=re.S)
        t=re.sub(r'<nav class=[\'"]topnav[\'"].*?</nav>',nav.topnav("",prefix),t,count=1,flags=re.S)
        if rel=="00_Carte_des_idees.html":t=t.replace("Version 6.51.","Version 6.52.")
        path.write_text(t,encoding="utf-8")
    for stem,key in [(S77,"signe"),(S78,"transport")]:
        before=P/(stem+"_nav.html")
        before.write_text(nav.topnav(key,"../")+
          '<p><a href="https://chatgpt.com/api/library/files/libfile_e12b21a3a190819196641d18ac05665a/download">ZIP courant du corpus récupéré</a>'+
          (' · <a href="'+stem+'.pdf">PDF</a> · <a href="'+stem+'.tex">LaTeX</a>' if stem==S78 else "")+"</p>")
        result=subprocess.run(["pandoc",stem+".md","-s","-f","markdown+tex_math_single_backslash",
          "--mathml","--embed-resources","--toc","--toc-depth=2","--css","v651_style.css",
          "--include-before-body",before.name,"-o",stem+".html"],cwd=P,capture_output=True,text=True)
        (D/(stem+"_html_build.log")).write_text(result.stderr)
        if result.returncode:raise RuntimeError(result.stderr)
    active+=["1_Presentation/"+S77+".html","1_Presentation/"+S78+".html"]
    write(D/"v652_pages_actives.json",dict(pages=active))
    missing,count,dynamic=check(root,active)
    rec["unavailable_links_before_annotation"]=missing;rec["active_pages"]=len(active)
    write(root/"RECUPERATION_2026_10_14.json",rec)
    if missing:
        note+="\n## Autres liens indisponibles dans les pages actives\n\n"
        note+="\n".join("- "+p for p in sorted({r["target"] for r in missing}))+"\n";recovery_page()
        for rel in active:
            path=root/rel;t=path.read_text();prefix="" if path.parent==root else "../"
            for row in [r for r in missing if r["page"]==rel]:
                for value in {row["href"],html.escape(row["href"],quote=True)}:
                    for quote in ['"',"'"]:
                        original="href="+quote+value+quote
                        replacement=('href='+quote+prefix+'RECUPERATION.html'+quote+
                          ' data-missing-target="'+html.escape(row["href"],quote=True)+'"'+
                          ' title="Fichier non récupéré : '+html.escape(row["target"],quote=True)+'"')
                        t=t.replace(original,replacement)
            path.write_text(t)
    remaining,count,dynamic=check(root,active)
    write(D/"v652_validation_liens.json",dict(active_pages=len(active),checked_local_targets=count,
      dynamic_template_targets_skipped=dynamic,unresolved_targets=remaining,
      unavailable_historical_targets_redirected=len(missing)))
    assert not remaining,remaining
    assert all((root/r).read_text().count('data-current="v652"')==1 for r in active)
    (root/"VERSION.txt").write_text("Programme Riemann — V6.52\n\n"+RESULT+
      "\n\nCorpus récupéré avec limites explicites ; voir RECUPERATION.md.\n")
    oldread=(root/"README.md").read_text(encoding="utf-8-sig")
    (root/"README.md").write_text("# Programme Riemann - V6.52\n\n"+RESULT+
      "\n\nOuvrir [le portail](00_PORTAIL.html), [la nouvelle note](1_Presentation/"+S78+
      ".html) ou [son PDF](1_Presentation/"+S78+".pdf).\n\n"
      "**Récupération historique partielle.** Voir [l’inventaire](RECUPERATION.html). "
      "Les nouvelles briques et leurs programmes sont dans3_Preuves_et_calculs/recherche78. "
      "Aucune preuve de RH n’est revendiquée.\n\n---\n\n"+oldread,encoding="utf-8-sig")
    print(json.dumps(dict(active_pages=len(active),local_targets_checked=count,historical_redirects=len(missing),
      global_sign_certified=False)))

if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("--corpus",type=Path,required=True)
    ap.add_argument("--work",type=Path,default=Path(__file__).resolve().parent)
    a=ap.parse_args();main(a.corpus,a.work)
