"""Compact common menu: four main pages, direct Bellman, grouped documents."""
from html import escape
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def render_nav(current='',prefix='',pages=None):
 if pages is None:pages=json.loads((ROOT/'2_Methode/Pilotage/pilotage_recherche.json').read_text())['primary_pages']
 items=[]
 for p in pages:
  active=' aria-current="page"' if p['id']==current else ''
  items.append(f'<a data-primary="{escape(p["id"])}" href="{escape(prefix+p["path"])}"{active}>{escape(p["label"])}</a>')
 items.append(f'<a data-tool-link="bellman" href="{prefix}1_Presentation/34_NAVIGATEUR_DE_RECHERCHE.html#bellman">Bellman</a>')
 docs=[('atlas','Atlas des décisions (62) : documents','1_Presentation/62_ATLAS_DES_DECISIONS_BELLMAN.html#documents'),
       ('matrice','Matrice visuelle des théories (44)','1_Presentation/44_MATRICE_DES_THEORIES.html'),
       ('references-pdf','Registre des sources : PDF existant','1_Presentation/42_REGISTRE_DES_SOURCES.pdf'),
       ('references','Références globales','1_Presentation/42_REGISTRE_DES_SOURCES.html'),
       ('figures','Figures et images','00_Liste_des_figures.html'),
       ('articles','Articles PDF / LaTeX','00_PORTAIL.html#articles'),
       ('dossiers','Catalogue : tous les fichiers et fiches','00_PORTAIL.html#documents')]
 dropdown='<details class="nav-documents" style="position:relative;border:0;margin:0;padding:0"><summary style="cursor:pointer;font:inherit;padding:0;color:inherit">Documents</summary><ul style="position:absolute;z-index:90;right:0;top:100%;min-width:225px;max-width:85vw;margin:8px 0 0;padding:10px 15px;list-style:none;border:1px solid var(--rule,#b9c7d3);border-radius:4px;background:var(--sheet,#fff);color:var(--ink,#14243a);box-shadow:0 4px 12px #0002">'
 for key,label,path in docs:dropdown+=f'<li style="padding:6px 0"><a data-resource="{key}" href="{escape(prefix+path)}">{escape(label)}</a></li>'
 dropdown+='</ul></details>';items.append(dropdown)
 return '<nav class="topnav" style="display:flex;flex-wrap:wrap;gap:8px 18px;align-items:baseline" aria-label="Pages et ressources du programme">'+''.join(items)+'</nav>'
