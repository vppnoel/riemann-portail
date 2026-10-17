"""Check all local targets and shared navigation on the fifteen active pages."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
ROOT=Path(__file__).resolve().parents[2]
ACTIVE=['00_PORTAIL.html','00_Carte_des_idees.html','00_Liste_des_figures.html']+[
 '1_Presentation/'+x for x in ['31_INDICATEUR_D_AVANCEMENT.html','34_NAVIGATEUR_DE_RECHERCHE.html','44_MATRICE_DES_THEORIES.html','62_ATLAS_DES_DECISIONS_BELLMAN.html',
 '65_GRAPHE_DES_PASSAGES.html','66_GRAPHE_DES_CERTIFICATS.html','67_GRAPHE_DES_PONTS.html','69_LANGUE_DES_PASSAGES.html','70_PONT_ARITHMETIQUE.html','71_LEGO_REUTILISABLE.html','72_CONCENTRATION_PROJETEE.html','73_OPERATEUR_COMMUN.html']]
class Parser(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.nav=[];self.in_nav=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='nav' and 'topnav' in a.get('class','').split():self.in_nav=True
        for key in ['href','src']:
            if a.get(key):self.links.append(a[key])
        if self.in_nav and tag=='a':self.nav.append(a.get('href',''))
    def handle_endtag(self,tag):
        if tag=='nav':self.in_nav=False
def main():
    count=0;nav_base=None
    for rel in ACTIVE:
        p=ROOT/rel;parser=Parser();parser.feed(p.read_text(encoding='utf-8-sig'))
        assert parser.nav,rel
        nav=[str((p.parent/unquote(urlsplit(u).path)).resolve().relative_to(ROOT)) for u in parser.nav]
        if nav_base is None:nav_base=nav
        assert nav==nav_base,(rel,nav,nav_base)
        for u in parser.links:
            v=urlsplit(u)
            if v.scheme or v.netloc or not v.path:continue
            target=(p.parent/unquote(v.path)).resolve();assert target.exists(),(rel,u);count+=1
    out=dict(active_pages=len(ACTIVE),local_targets_checked=count,broken_targets=0,common_navigation=True,
        scope='static targets + shared navigation; no browser layout validation')
    print(json.dumps(out,ensure_ascii=False))
    (ROOT/'3_Preuves_et_calculs/data/v648_interface_validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
