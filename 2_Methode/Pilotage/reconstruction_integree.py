"""Current integration page; preserved reconstruction files remain historical originals of the new supplement."""
from pathlib import Path
import html,json,importlib.util
ROOT=Path(__file__).resolve().parents[2]
def build():
    base='3_Preuves_et_calculs/reconstruction_v651_20261015/'
    result=json.loads((ROOT/base/'v651_pistes_globales_resultats_RECONSTRUITS.json').read_text())
    spec=importlib.util.spec_from_file_location('integration_navigation',ROOT/'2_Methode/Pilotage/navigation.py')
    nav=importlib.util.module_from_spec(spec);spec.loader.exec_module(nav)
    esc=lambda s:html.escape(str(s),quote=True)
    link=lambda p,t:'<a href="../'+esc(p)+'">'+esc(t)+'</a>'
    rows=''.join('<tr><th>'+str(x['S'])+'</th><td>'+esc(x['upper_bound_on_Q_A_over_mass']['midpoint_display_only'])+'</td><td>'+('Troncature négative' if x['negative_certified'] else 'Inconclusif')+'</td></tr>' for x in result['fixed_prime_truncation_witnesses'])
    items=''.join('<li>'+link(str(p.relative_to(ROOT)),p.name)+'</li>' for p in sorted((ROOT/base).rglob('*')) if p.is_file())
    css=(ROOT/'2_Methode/Pilotage/style_claude.css').read_text()
    text='<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Reconstruction V6.51 intégrée — V6.58</title><style>'+css+'.sheet>*{min-width:0}.tablewrap{overflow:auto}li,a{overflow-wrap:anywhere}</style></head><body><main class="wrap">'+nav.render_nav('', '../')+'<header class="head"><div class="eyebrow">Programme Riemann · V6.58 · intégration du 15 octobre 2026</div><h1>La reconstruction V6.51 est dans le corpus global</h1><p class="lede">Programme, journal calculé, notice, sources et ZIP du complément sont réunis avec les autres travaux.</p></header>'
    text+='<section class="sheet"><h2>Accès direct</h2><p>'+link(base+'v651_verifier_pistes_globales_RECONSTRUIT.py','Programme reconstruit')+' · '+link(base+'v651_pistes_globales_resultats_RECONSTRUITS.json','Journal calculé')+' · '+link('4_Exports/V651_RECONSTRUCTION_DOCUMENTEE_20261015.zip','Complément complet inclus')+'</p><p>'+link('00_PORTAIL.html?recherche=reconstruction_v651#documents','Retrouver tous ces fichiers dans le catalogue')+' · '+link('00_Carte_des_idees.html#node=IDE-051','Fiche du signe global')+'</p></section>'
    text+='<section class="sheet"><h2>Résultats des contrôles</h2><div class="tablewrap"><table><thead><tr><th>S</th><th>Majorant de la troncature fixe Q_A / masse</th><th>Conclusion</th></tr></thead><tbody>'+rows+'</tbody></table></div><p>Valeurs indicatives ; les bornes rationnelles exactes sont dans le journal. Ce calcul omet les autres puissances premières actives et ne donne pas le signe de la forme complète de Weil.</p><p>Les trois minorants d’enveloppe du document76 sont également retrouvés. Le calcul rationnel, le recoupement mpmath et la reproduction à l’identique après extraction sont conservés.</p></section>'
    text+='<section class="sheet"><h2>Statut et provenance</h2><p>Les deux contrôles ont été reconstruits ; les originaux manquants ne sont pas déclarés retrouvés. La loi globale de signe et RH restent ouvertes. Les revues parallèles ont été interrompues ; aucune double relecture indépendante achevée n’est revendiquée.</p><p>Les mentions « paquet séparé » et « ZIP global inchangé » présentes dans les fichiers conservés décrivent leur création antérieure. Ils sont désormais intégrés dans cette livraison globale. Leurs octets et leur journal initial sont conservés.</p><p>'+link('INTEGRATION_GLOBALE_20261015.json','Inventaire de conservation des archives et de cette intégration')+'</p></section>'
    text+='<section class="sheet"><h2>Toutes les pièces intégrées</h2><ul>'+items+'</ul></section><footer>Vincent P. P. NOËL · V6.58 · documents et identifiants conservés.</footer></main></body></html>'
    (ROOT/'1_Presentation/RECONSTRUCTION_V651_INTEGREE.html').write_text(text)
