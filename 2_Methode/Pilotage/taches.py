#!/usr/bin/env python3
"""Fiches de tâche : répartir le travail entre l'auteur, des IA et des agents, de façon itérative.

La procédure est décrite dans CIBLAGE.md (même dossier). Aucune dépendance hors bibliothèque standard ;
aucun nom de modèle n'est supposé. Un acteur s'écrit « type:nom », avec type = auteur, ia ou agent
(exemples : auteur:vincent-noel, ia:modele-x, agent:calcul-1).

  python -B 2_Methode/Pilotage/taches.py etat
  python -B 2_Methode/Pilotage/taches.py ouvrir --par ACTEUR                  # fiches proposées par le ciblage (idempotent)
  python -B 2_Methode/Pilotage/taches.py creer --par ACTEUR --depuis f.json   # fiche manuelle, mêmes champs obligatoires
  python -B 2_Methode/Pilotage/taches.py fiche TAC-001 [--verification]       # consigne autonome à remettre à l'acteur
  python -B 2_Methode/Pilotage/taches.py assigner TAC-001 ACTEUR --par ACTEUR
  python -B 2_Methode/Pilotage/taches.py prevoir TAC-001 --par ACTEUR --texte "…"   # prévision écrite AVANT le travail
  python -B 2_Methode/Pilotage/taches.py deposer TAC-001 --par ACTEUR --statut-propose mesure [--equivalent-rh]
  python -B 2_Methode/Pilotage/taches.py verifier TAC-001 --par ACTEUR --verdict conforme|non_conforme --note "…"
  python -B 2_Methode/Pilotage/taches.py decider TAC-001 --par auteur:NOM --decision acceptee|rejetee|a_reprendre --note "…"
  python -B 2_Methode/Pilotage/taches.py integrer TAC-001 --par ACTEUR --pieces chemin1 chemin2 …
  python -B 2_Methode/Pilotage/taches.py abandonner TAC-001 --par auteur:NOM --note "…"
  python -B 2_Methode/Pilotage/taches.py controler
  python -B 2_Methode/Pilotage/taches.py boites                                # 2_Methode/Echanges/<acteur>/ : à produire, à vérifier

Règles appliquées par le programme (et non seulement décrites) :
  1. une fiche a, dès sa création, sa sortie attendue et son critère de rejet ;
  2. le producteur enregistre sa prévision avant de déposer ;
  3. le producteur n'écrit que dans 2_Methode/Depot/<ID>/ ; le dépôt est figé par empreintes ;
  4. si une entrée change, la fiche est périmée ;
  5. le vérificateur est un autre acteur que le producteur ;
  6. seul un acteur déclaré auteur accepte ou rejette ;
  7. chaque événement est ajouté au journal, chaîné par empreintes.
Ces règles organisent le travail ; elles ne vérifient pas une preuve et ne remplacent pas un contrôle d'accès.
Auteur : Vincent NOËL.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, importlib.util, json, re, sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REGISTRE = '2_Methode/Pilotage/taches.json'
JOURNAL = '2_Methode/Pilotage/journal_taches.json'
DEPOT = '2_Methode/Depot'
ECHANGES = '2_Methode/Echanges'
ACTEUR = re.compile(r'^(auteur|ia|agent):[a-z0-9][a-z0-9._-]{0,63}$')
FINAUX = {'integree', 'rejetee', 'abandonnee', 'perimee'}
GENRES = {'calcul', 'investigation', 'lier_instance', 'verification_temoin', 'bibliographie', 'formalisation', 'redaction'}
ROLES = {'coordinateur', 'explorateur', 'auditeur', 'bibliothecaire', 'numerique', 'formalisateur', 'rapporteur'}
STATUTS_SCIENTIFIQUES = ['demontre', 'classique', 'mesure', 'ouvert', 'partiel', 'conditionnel', 'obstacle', 'diagnostic', 'outil', 'refute']
TITRES_RAPPORT = ['## Prévision', '## Méthode', '## Résultat', '## Portée', '## Critère de rejet', '## Statut proposé']
OBLIGATOIRES = ['genre', 'role', 'titre', 'question', 'entrees', 'sortie_attendue', 'critere_rejet']
ANTI_CIRCULARITE = [
    "Tester l'énoncé sur Davenport–Heilbronn : s'il y fonctionne mot pour mot, il ne peut pas servir pour RH.",
    "Le confronter à l'analogue des corps de fonctions (RH connue) : une positivité sans image là-bas n'est pas une preuve.",
    "Aucune donnée qui injecte la réponse (zéros ou modes fabriqués puis retrouvés).",
    "Exiger un témoin négatif : la méthode doit détecter un défaut connu, au bon endroit.",
    "Signaler tout énoncé équivalent à RH : une équivalence n'est un progrès que si elle rend un outil nouveau accessible, à nommer.",
    "Toute constante numérique est donnée avec son erreur et ce qu'elle teste réellement.",
]


class Refus(Exception):
    pass


def maintenant():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def lire(root, rel, defaut):
    p = Path(root) / rel
    return json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else defaut


def ecrire(root, rel, obj):
    p = Path(root) / rel; tmp = p.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'); tmp.replace(p)


def acteur(a):
    if not a or not ACTEUR.match(a): raise Refus(f'Acteur invalide « {a} » : écrire type:nom avec type = auteur, ia ou agent.')
    return a


class Registre:
    def __init__(self, root=ROOT):
        self.root = Path(root)
        self.data = lire(self.root, REGISTRE, None)
        if self.data is None: raise Refus(f'{REGISTRE} absent.')
        self.journal = lire(self.root, JOURNAL, dict(schema='journal_taches_v1', evenements=[]))

    # ---------------------------------------------------------------- utilitaires
    def tache(self, ident):
        for t in self.data['taches']:
            if t['id'] == ident: return t
        raise Refus(f'Fiche inconnue : {ident}')

    def empreintes(self, chemins):
        return {c: (sha(self.root / c) if (self.root / c).is_file() else None) for c in chemins}

    def depot(self, t):
        return self.root / DEPOT / t['id']

    def empreintes_depot(self, t):
        d = self.depot(t)
        return {str(f.relative_to(self.root)): sha(f) for f in sorted(d.rglob('*'))
                if f.is_file() and 'verification' not in f.relative_to(d).parts[:1]}

    def evenement(self, par, tache, quoi, **details):
        ev = self.journal['evenements']
        prec = hashlib.sha256(json.dumps(ev[-1], ensure_ascii=False, sort_keys=True).encode()).hexdigest() if ev else None
        ev.append(dict(n=len(ev) + 1, le=maintenant(), par=par, tache=tache, evenement=quoi, details=details, empreinte_precedente=prec))

    def sauver(self):
        ecrire(self.root, REGISTRE, self.data); ecrire(self.root, JOURNAL, self.journal)

    def entrees_inchangees(self, t, par):
        actuelles = self.empreintes(list(t['entrees']))
        changees = [c for c, h in t['entrees'].items() if actuelles[c] != h]
        if changees:
            t['statut'] = 'perimee'
            self.evenement(par, t['id'], 'perimee', entrees_modifiees=changees); self.sauver()
            raise Refus(f"{t['id']} périmée : entrées modifiées depuis la création ({', '.join(changees)}). Ouvrir une nouvelle fiche.")

    def nouvel_id(self):
        n = max([int(t['id'][4:]) for t in self.data['taches']] or [0]) + 1
        return f'TAC-{n:03d}'

    # ---------------------------------------------------------------- création
    def creer(self, fiche, par, version=None):
        acteur(par)
        manque = [k for k in OBLIGATOIRES if not fiche.get(k)]
        if manque: raise Refus('Champs obligatoires manquants : ' + ', '.join(manque))
        if fiche['genre'] not in GENRES: raise Refus(f"Genre inconnu : {fiche['genre']}")
        if fiche['role'] not in ROLES: raise Refus(f"Rôle inconnu : {fiche['role']}")
        cle = fiche.get('cle') or 'manuel:' + hashlib.sha256(fiche['question'].encode()).hexdigest()[:12]
        anciennes = [t for t in self.data['taches'] if t['cle'] == cle]
        if any(t['statut'] not in FINAUX for t in anciennes): return None
        t = dict(id=self.nouvel_id(), cle=cle, cycle=len(anciennes) + 1, version=version or self.data.get('version'),
                 genre=fiche['genre'], role=fiche['role'], titre=fiche['titre'], question=fiche['question'],
                 objet=fiche.get('objet'), domaine=fiche.get('domaine'), entrees=self.empreintes(fiche['entrees']),
                 commande=fiche.get('commande'), sortie_attendue=fiche['sortie_attendue'], critere_rejet=fiche['critere_rejet'],
                 temoin=fiche.get('temoin'), budget=fiche.get('budget'), noeuds=fiche.get('noeuds', []),
                 creee_le=maintenant(), creee_par=par, statut='ouverte', assigne_a=None, previsions=[], depots=[],
                 verifications=[], decision=None, integration=None)
        absentes = [c for c, h in t['entrees'].items() if h is None]
        if absentes: raise Refus('Entrées absentes : ' + ', '.join(absentes))
        self.data['taches'].append(t); self.evenement(par, t['id'], 'creee', cle=cle, cycle=t['cycle'])
        return t

    def ouvrir(self, par):
        spec = importlib.util.spec_from_file_location('ciblage_taches', self.root / '2_Methode/Pilotage/ciblage.py')
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        rapport = m.analyse(self.root)
        crees = [t['id'] for f in rapport['fiches_proposees'] if (t := self.creer(f, par, rapport['version']))]
        self.sauver(); return crees

    # ---------------------------------------------------------------- cycle de vie
    def assigner(self, ident, qui, par):
        acteur(qui); acteur(par); t = self.tache(ident)
        if t['statut'] not in ('ouverte', 'assignee'): raise Refus(f"{ident} est « {t['statut']} » : réassignation impossible.")
        t['assigne_a'] = qui; t['statut'] = 'assignee'
        self.evenement(par, ident, 'assignee', a=qui); self.sauver()

    def prevoir(self, ident, par, texte):
        acteur(par); t = self.tache(ident)
        if par != t['assigne_a']: raise Refus(f"Seul l'acteur assigné ({t['assigne_a']}) écrit la prévision.")
        if t['statut'] not in ('assignee', 'a_reprendre'): raise Refus(f"{ident} est « {t['statut']} » : prévision impossible.")
        if not texte or len(texte.strip()) < 20: raise Refus('Prévision trop courte : dire ce qui est attendu et ce qui la réfuterait.')
        t['previsions'].append(dict(le=maintenant(), texte=texte.strip()))
        self.evenement(par, ident, 'prevision', texte=texte.strip()); self.sauver()

    def deposer(self, ident, par, statut_propose, equivalent_rh=False):
        acteur(par); t = self.tache(ident)
        if par != t['assigne_a']: raise Refus(f"Seul l'acteur assigné ({t['assigne_a']}) dépose.")
        if t['statut'] not in ('assignee', 'a_reprendre'): raise Refus(f"{ident} est « {t['statut']} » : dépôt impossible.")
        if not t['previsions']: raise Refus('Aucune prévision enregistrée : la prévision précède le travail (taches.py prevoir).')
        if statut_propose not in STATUTS_SCIENTIFIQUES: raise Refus('Statut proposé hors vocabulaire : ' + ', '.join(STATUTS_SCIENTIFIQUES))
        self.entrees_inchangees(t, par)
        rapport = self.depot(t) / 'RAPPORT.md'
        if not rapport.is_file(): raise Refus(f'{rapport.relative_to(self.root)} absent.')
        texte = rapport.read_text(encoding='utf-8-sig')
        manque = [h for h in TITRES_RAPPORT if h not in texte]
        if manque: raise Refus('RAPPORT.md incomplet, sections manquantes : ' + ', '.join(manque))
        fichiers = self.empreintes_depot(t)
        t['depots'].append(dict(le=maintenant(), par=par, fichiers=fichiers, statut_propose=statut_propose, equivalent_rh=bool(equivalent_rh)))
        t['statut'] = 'deposee'
        self.evenement(par, ident, 'deposee', fichiers=fichiers, statut_propose=statut_propose, equivalent_rh=bool(equivalent_rh)); self.sauver()

    def retirer(self, ident, par, motif):
        """Le producteur retire son dépôt tant qu'aucun vérificateur ne l'a jugé : déposée → à reprendre.
        Le motif cite le fil de discussion. Le dépôt retiré reste au journal ; le suivant sera de nouveau figé."""
        acteur(par); t = self.tache(ident)
        if t['statut'] != 'deposee': raise Refus(f"{ident} est « {t['statut']} » : retrait seulement d'un dépôt non encore vérifié.")
        if par != t['depots'][-1]['par']: raise Refus('Seul le producteur du dépôt le retire.')
        if not motif or len(motif.strip()) < 20: raise Refus('Motif trop court : dire ce qui manque et citer le fil de discussion.')
        t['statut'] = 'a_reprendre'
        self.evenement(par, ident, 'retiree', motif=motif.strip()); self.sauver()

    def verifier(self, ident, par, verdict, note):
        acteur(par); t = self.tache(ident)
        if t['statut'] != 'deposee': raise Refus(f"{ident} est « {t['statut']} » : rien à vérifier.")
        producteurs = {d['par'] for d in t['depots']}
        if par in producteurs: raise Refus('Le vérificateur doit être un autre acteur que le producteur.')
        if verdict not in ('conforme', 'non_conforme'): raise Refus('Verdict : conforme ou non_conforme.')
        if not note or len(note.strip()) < 20: raise Refus('Note de vérification trop courte : dire ce qui a été rejoué et confronté.')
        self.entrees_inchangees(t, par)
        if self.empreintes_depot(t) != t['depots'][-1]['fichiers']: raise Refus('Dépôt modifié après son enregistrement : redéposer avant vérification.')
        v = self.depot(t) / 'verification' / 'VERIFICATION.md'
        if not v.is_file(): raise Refus(f'{v.relative_to(self.root)} absent : le vérificateur y écrit sa liste de contrôle.')
        t['verifications'].append(dict(le=maintenant(), par=par, verdict=verdict, note=note.strip(), fichier=sha(v)))
        t['statut'] = 'verifiee' if verdict == 'conforme' else 'a_reprendre'
        self.evenement(par, ident, 'verifiee', verdict=verdict, note=note.strip()); self.sauver()

    def decider(self, ident, par, decision, note):
        acteur(par); t = self.tache(ident)
        if par not in self.data['auteurs']: raise Refus('Seul un acteur déclaré auteur décide (taches.json, « auteurs »).')
        if decision == 'acceptee' and t['statut'] != 'verifiee': raise Refus('Acceptation seulement après une vérification conforme.')
        if decision == 'a_reprendre' and t['statut'] != 'verifiee': raise Refus('Renvoi seulement depuis « verifiee ».')
        if decision == 'rejetee' and t['statut'] in FINAUX: raise Refus(f"{ident} est déjà « {t['statut']} ».")
        if decision not in ('acceptee', 'rejetee', 'a_reprendre'): raise Refus('Décision : acceptee, rejetee ou a_reprendre.')
        if decision == 'acceptee': self.entrees_inchangees(t, par)
        t['decision'] = dict(le=maintenant(), par=par, decision=decision, note=note or '')
        t['statut'] = decision
        self.evenement(par, ident, 'decision', decision=decision, note=note or ''); self.sauver()

    def integrer(self, ident, par, pieces):
        acteur(par); t = self.tache(ident)
        if t['statut'] != 'acceptee': raise Refus('Intégration seulement après acceptation par l’auteur.')
        if not pieces: raise Refus('Nommer les pièces du corpus qui portent le résultat (document, données, bilan).')
        hors = [p for p in pieces if not (self.root / p).is_file() or p.startswith(DEPOT)]
        if hors: raise Refus('Pièces absentes ou restées dans le dépôt : ' + ', '.join(hors))
        t['integration'] = dict(le=maintenant(), par=par, pieces=self.empreintes(pieces)); t['statut'] = 'integree'
        self.evenement(par, ident, 'integree', pieces=t['integration']['pieces']); self.sauver()

    def abandonner(self, ident, par, note):
        acteur(par); t = self.tache(ident)
        if par not in self.data['auteurs']: raise Refus('Seul un acteur déclaré auteur abandonne une fiche.')
        if t['statut'] in FINAUX: raise Refus(f"{ident} est déjà « {t['statut']} ».")
        t['statut'] = 'abandonnee'; t['decision'] = dict(le=maintenant(), par=par, decision='abandonnee', note=note or '')
        self.evenement(par, ident, 'abandonnee', note=note or ''); self.sauver()

    # ---------------------------------------------------------------- boîtes aux lettres
    def boites(self):
        """Écrit 2_Methode/Echanges/<acteur>/ : A_FAIRE.md et une consigne par fiche (produire ou vérifier).
        Régénéré entièrement à chaque appel ; ne modifie pas le registre."""
        import shutil
        racine = self.root / ECHANGES
        acteurs = sorted({t['assigne_a'] for t in self.data['taches'] if t['assigne_a']} | {d['par'] for t in self.data['taches'] for d in t['depots']})
        acteurs = [a for a in acteurs if not a.startswith('auteur:')]
        for d in racine.glob('*'):
            if d.is_dir(): shutil.rmtree(d)
        racine.mkdir(parents=True, exist_ok=True)
        resume = {}
        for a in acteurs:
            d = racine / a.replace(':', '_'); d.mkdir()
            produire = [t for t in self.data['taches'] if t['assigne_a'] == a and t['statut'] in ('assignee', 'a_reprendre')]
            verifier = [t for t in self.data['taches'] if t['statut'] == 'deposee' and a not in {x['par'] for x in t['depots']}]
            L = ['\ufeff# Boîte de ' + a, '', f"*Générée par `taches.py boites` le {maintenant()}. Ne pas modifier : la source est le registre des fiches.*", '']
            L += ['## À produire', ''] + ([f"- **{t['id']}** — {t['titre']} ({'prévision déjà enregistrée' if t['previsions'] else 'commencer par la prévision'}) → `{t['id']}_produire.md`" for t in produire] or ['- rien'])
            L += ['', '## À vérifier (dépôts d\'un autre acteur)', ''] + ([f"- **{t['id']}** — {t['titre']} → `{t['id']}_verifier.md` ; pièces dans `2_Methode/Depot/{t['id']}/`" for t in verifier] or ['- rien'])
            fils = [t['id'] for t in produire + verifier]
            L += ['', '## Fils de discussion', '', 'Lire le fil d\'une fiche en entier avant de la reprendre, et y répondre à chaque point soulevé.', '']
            L += [f"- {i} : https://github.com/Vppnoel/riemann/issues?q={i}" for i in fils] or ['- aucun']
            L += ['', '## Règles (GITHUB.md, § 4)', '',
                  '- Commandes `taches.py` : directement sur `main`, un commit par commande.',
                  '- Tout le reste passe par une branche et une pull request : `tac-xxx` pour produire, `tac-xxx-verif` pour vérifier.',
                  '- Un changement de méthode (tests, tolérances, contrôles, règles, scripts de vérification, registres, indicateur) est fusionné par l\'auteur seul, après son accord écrit dans la pull request.',
                  '- Signer sous son propre nom ; si l\'outil écrit sous le compte de l\'auteur, commencer le message du commit par son identifiant d\'acteur. Jamais `--par auteur:…`.',
                  '- Une discussion ne décide rien : ce qui est convenu est inscrit par une commande de fiche.',
                  '', 'Rendre le travail selon `2_Methode/Pilotage/CIBLAGE.md` (ou `TARGETING_EN.md`). Un acteur sans droit d\'écriture rend ses fichiers à l\'auteur, qui les dépose.', '']
            (d / 'A_FAIRE.md').write_text('\n'.join(L), encoding='utf-8')
            for t in produire: (d / f"{t['id']}_produire.md").write_text('\ufeff' + self.fiche(t['id']).replace('VOTRE_ID', a), encoding='utf-8')
            for t in verifier: (d / f"{t['id']}_verifier.md").write_text('\ufeff' + self.fiche(t['id'], verification=True).replace('VOTRE_ID', a), encoding='utf-8')
            resume[a] = dict(produire=[t['id'] for t in produire], verifier=[t['id'] for t in verifier])
        (racine / 'README.md').write_text('\ufeff# Échanges entre acteurs\n\nUne boîte par acteur (IA ou agent) : `A_FAIRE.md` liste ce qu\'il doit produire et vérifier, avec une consigne autonome par fiche. Régénéré par `python -B 2_Methode/Pilotage/taches.py boites` après chaque opération sur les fiches. Procédure : `2_Methode/Pilotage/CIBLAGE.md`.\n', encoding='utf-8')
        return resume

    # ---------------------------------------------------------------- lecture
    def controler(self):
        err = []
        ids = [t['id'] for t in self.data['taches']]
        if len(set(ids)) != len(ids): err.append('identifiants dupliqués')
        prec = None
        for e in self.journal['evenements']:
            if e['empreinte_precedente'] != prec: err.append(f"journal : chaîne rompue à l'événement {e['n']}")
            if e['tache'] not in ids: err.append(f"journal : fiche inconnue {e['tache']}")
            prec = hashlib.sha256(json.dumps(e, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        for t in self.data['taches']:
            for k in OBLIGATOIRES:
                if not t.get(k): err.append(f"{t['id']} : champ {k} vide")
            prod = {d['par'] for d in t['depots']}
            if any(v['par'] in prod for v in t['verifications']): err.append(f"{t['id']} : vérifié par son producteur")
            if t['depots'] and not t['previsions']: err.append(f"{t['id']} : dépôt sans prévision")
            if t['depots'] and t['previsions'] and t['previsions'][0]['le'] > t['depots'][0]['le']: err.append(f"{t['id']} : prévision postérieure au dépôt")
            if t['statut'] in ('acceptee', 'integree') and not (t['decision'] and t['decision']['par'] in self.data['auteurs']): err.append(f"{t['id']} : acceptée sans décision d'auteur")
            if t['statut'] in ('deposee', 'verifiee', 'acceptee') and self.empreintes_depot(t) != t['depots'][-1]['fichiers']:
                err.append(f"{t['id']} : dépôt modifié après enregistrement")
        return err

    def etat(self):
        par_statut = {}
        for t in self.data['taches']: par_statut.setdefault(t['statut'], []).append(t)
        return par_statut

    def fiche(self, ident, verification=False):
        t = self.tache(ident); d = self.data
        L = [f"# {t['id']} — {t['titre']}", '',
             f"*Programme Riemann {t['version']} · genre : {t['genre']} · rôle : {t['role']} · cycle {t['cycle']} · statut : {t['statut']}*", '',
             '## Contexte', '',
             "Corpus de recherche sur l'hypothèse de Riemann (RH). RH n'est pas démontrée et ne doit pas être présentée comme telle. "
             "Lire d'abord `README.md` (« À lire d'abord »), puis `2_Methode/Pilotage/CIBLAGE.md`. Méthode : prévision écrite avant, témoins contraires, portée explicite.", '']
        if not verification:
            L += ['## Question', '', t['question'], '']
        else:
            L += ['## Énoncé à vérifier', '', t['question'], '',
                  "*Relecture à l'aveugle : l'identité du producteur n'est pas donnée. Lire les pièces et les données avant la conclusion du rapport.*", '']
        L += ['## Entrées (empreintes SHA-256 au moment de la création)', ''] + [f"- `{c}` — `{(h or 'absent')[:16]}…`" for c, h in t['entrees'].items()] + ['']
        if t.get('objet') or t.get('domaine'): L += [f"**Objet :** {t.get('objet') or '—'} · **Domaine :** {t.get('domaine') or '—'}", '']
        if t.get('commande'): L += ['## Commande bornée', '', '```sh', t['commande'], '```', '']
        L += ['## Sortie attendue', '', t['sortie_attendue'], '', '## Critère de rejet (écrit avant)', '', t['critere_rejet'], '']
        if t.get('temoin'): L += ['## Témoin', '', t['temoin'], '']
        if t.get('budget'): L += [f"**Budget déclaré :** {t['budget']}", '']
        L += ['## Contrôles anti-circularité', ''] + ['- ' + x for x in ANTI_CIRCULARITE] + ['']
        if not verification:
            L += ['## Ce que vous devez faire', '',
                  f"1. Avant tout calcul ou raisonnement : `python -B 2_Methode/Pilotage/taches.py prevoir {t['id']} --par VOTRE_ID --texte \"…\"` (ce que vous attendez, et ce qui vous donnerait tort).",
                  f"2. N'écrire que dans `{DEPOT}/{t['id']}/`. Aucun autre fichier du corpus n'est modifié.",
                  f"3. Y déposer `RAPPORT.md` avec les sections : {', '.join(h[3:] for h in TITRES_RAPPORT)} ; plus les programmes, données et journaux utiles.",
                  f"4. `python -B 2_Methode/Pilotage/taches.py deposer {t['id']} --par VOTRE_ID --statut-propose STATUT` (statut parmi : {', '.join(STATUTS_SCIENTIFIQUES)} ; ajouter `--equivalent-rh` si l'énoncé obtenu entraîne RH).",
                  '5. Ne rien affirmer au-delà de la portée établie ; un échec documenté est un résultat.', '']
        else:
            dep = t['depots'][-1] if t['depots'] else None
            L += ['## Pièces déposées', ''] + ([f"- `{c}`" for c in dep['fichiers']] if dep else ['- (aucun dépôt)']) + ['']
            if dep: L += [f"**Statut proposé :** {dep['statut_propose']} · **Équivalent à RH déclaré :** {'oui' if dep['equivalent_rh'] else 'non'}", '']
            L += ['## Ce que vous devez faire', '',
                  '1. Rejouer ce qui peut l’être (programmes, calculs) et confronter le résultat au critère de rejet écrit avant.',
                  '2. Appliquer les contrôles anti-circularité ci-dessus ; chercher circularités, équivalences à RH déguisées, erreurs de signe, hypothèses cachées.',
                  "3. Vérifier que la portée annoncée n'excède pas ce qui est établi, et que le statut proposé est le bon.",
                  f"4. Écrire `{DEPOT}/{t['id']}/verification/VERIFICATION.md` (ce qui a été rejoué, ce qui ne l'a pas été, écarts).",
                  f"5. `python -B 2_Methode/Pilotage/taches.py verifier {t['id']} --par VOTRE_ID --verdict conforme|non_conforme --note \"…\"`. Vous ne pouvez pas être le producteur.", '']
        L += ["*La décision (acceptée, rejetée, à reprendre) appartient à l'auteur. L'intégration au corpus suit ensuite le protocole du pilotage : prévision conservée, preuve et portée, bilan, indicateur réexaminé.*", '']
        return '\n'.join(L)


def main(argv=None):
    p = argparse.ArgumentParser(description='Fiches de tâche du Programme Riemann (voir CIBLAGE.md).')
    p.add_argument('--racine', default=str(ROOT), help=argparse.SUPPRESS)
    sub = p.add_subparsers(dest='cmd', required=True)
    sub.add_parser('etat'); sub.add_parser('controler'); sub.add_parser('boites')
    s = sub.add_parser('ouvrir'); s.add_argument('--par', required=True)
    s = sub.add_parser('creer'); s.add_argument('--par', required=True); s.add_argument('--depuis', required=True)
    s = sub.add_parser('fiche'); s.add_argument('id'); s.add_argument('--verification', action='store_true')
    s = sub.add_parser('assigner'); s.add_argument('id'); s.add_argument('acteur'); s.add_argument('--par', required=True)
    s = sub.add_parser('prevoir'); s.add_argument('id'); s.add_argument('--par', required=True); s.add_argument('--texte', required=True)
    s = sub.add_parser('deposer'); s.add_argument('id'); s.add_argument('--par', required=True); s.add_argument('--statut-propose', required=True); s.add_argument('--equivalent-rh', action='store_true')
    s = sub.add_parser('retirer'); s.add_argument('id'); s.add_argument('--par', required=True); s.add_argument('--motif', required=True)
    s = sub.add_parser('verifier'); s.add_argument('id'); s.add_argument('--par', required=True); s.add_argument('--verdict', required=True); s.add_argument('--note', required=True)
    s = sub.add_parser('decider'); s.add_argument('id'); s.add_argument('--par', required=True); s.add_argument('--decision', required=True); s.add_argument('--note', default='')
    s = sub.add_parser('integrer'); s.add_argument('id'); s.add_argument('--par', required=True); s.add_argument('--pieces', nargs='+', required=True)
    s = sub.add_parser('abandonner'); s.add_argument('id'); s.add_argument('--par', required=True); s.add_argument('--note', default='')
    a = p.parse_args(argv)
    try:
        r = Registre(a.racine)
        if a.cmd == 'etat':
            for st, ts in sorted(r.etat().items()):
                print(f'{st} ({len(ts)})')
                for t in ts: print(f"  {t['id']}  {t['genre']:<13} {t['assigne_a'] or '—':<24} {t['titre']}")
            if not r.data['taches']: print('Aucune fiche. Lancer : taches.py ouvrir --par ACTEUR')
        elif a.cmd == 'controler':
            err = r.controler(); print(json.dumps(dict(fiches=len(r.data['taches']), evenements=len(r.journal['evenements']), erreurs=err), ensure_ascii=False, indent=2))
            return 1 if err else 0
        elif a.cmd == 'boites': print(json.dumps(r.boites(), ensure_ascii=False, indent=1))
        elif a.cmd == 'ouvrir': print(json.dumps(dict(creees=r.ouvrir(a.par)), ensure_ascii=False))
        elif a.cmd == 'creer':
            t = r.creer(json.loads(Path(a.depuis).read_text(encoding='utf-8-sig')), a.par); r.sauver()
            print(t['id'] if t else 'Fiche déjà ouverte pour cette clé ; rien créé.')
        elif a.cmd == 'fiche': print(r.fiche(a.id, a.verification))
        elif a.cmd == 'assigner': r.assigner(a.id, a.acteur, a.par)
        elif a.cmd == 'prevoir': r.prevoir(a.id, a.par, a.texte)
        elif a.cmd == 'deposer': r.deposer(a.id, a.par, a.statut_propose, a.equivalent_rh)
        elif a.cmd == 'retirer': r.retirer(a.id, a.par, a.motif)
        elif a.cmd == 'verifier': r.verifier(a.id, a.par, a.verdict, a.note)
        elif a.cmd == 'decider': r.decider(a.id, a.par, a.decision, a.note)
        elif a.cmd == 'integrer': r.integrer(a.id, a.par, a.pieces)
        elif a.cmd == 'abandonner': r.abandonner(a.id, a.par, a.note)
    except Refus as e:
        print('Refusé : ' + str(e), file=sys.stderr); return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
