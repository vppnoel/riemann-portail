"""Four progressive concepts and three tools added to the curated course."""
def extend(module):
    original=module.lessons
    def lessons():
        rows=original();new=[]
        e=module.entry
        r=e('joint_cost',2,'Coût conjoint','Une oscillation coûte de l’énergie. Le premier2 ajoute un coût qui dépend de sa phase : on garde les deux dans une seule règle.','Deux oscillations de même taille peuvent réagir différemment au déplacement log2. Le cosinus garde cette différence.',r'b(t)=a(t)+2w_2(1-\cos(t\log2))','Conserver la compensation entre les déplacements premiers et l’énergie.','Ici un seul premier agit. Le régime de support est vérifié avant le calcul.',('Q','fourier'));r['legend']='a : coût énergétique ; b : coût conjoint ; t : fréquence ; w₂ : poids du premier2 ; cos : accord de phase.';new.append(r)
        r=e('sublevel',3,'Sous-niveau de coût','On rassemble toutes les fréquences dont le coût est plus petit qu’un seuil. Le rassemblement peut avoir plusieurs morceaux.','Avec un coût qui monte puis redescend, une fréquence plus grande peut entrer à nouveau. On garde ces morceaux au lieu de remplir toute la bande.',r'\Omega_u=\{t>0:b(t)<u\}','Regarder les zones où la masse pourrait éviter de payer un coût élevé.','Une cellule incertaine est incluse : agrandir ce rassemblement rend la borne prudente.',('joint_cost','concentration'));r['legend']='Ω, oméga : ensemble de fréquences ; u : seuil de coût ; < : strictement inférieur.';new.append(r)
        r=e('schatten2',3,'Interactions entre fréquences','Chaque fréquence projetée peut ressembler à une autre. La somme des carrés de ces accords borne la plus forte concentration.','La trace additionne toutes les forces. Schatten2 prend la racine de leurs carrés : les directions faibles pèsent moins.',r'\|K\|\le\sqrt{\operatorname{tr}(K^2)}\le\operatorname{tr}K','Certifier une concentration plus précise et franchir le support 3/8.','Ces inégalités exigent un opérateur positif. Les erreurs du noyau et des intégrales restent nécessaires.',('sublevel','gram'));r['legend']='K : opérateur de concentration ; ||K|| : force maximale ; tr : somme des forces ; K² : appliquer deux fois.';new.append(r)
        r=e('common_operator',4,'Un même test dans toutes les couches','On assemble les opérateurs de toutes les couches avant de chercher la direction la plus forte. La fonction ne change plus d’une couche à l’autre.','Deux couches ont chacune une direction forte, mais ces directions sont perpendiculaires. Leur somme peut avoir une force 1 alors que la somme des forces vaut 2.',r'B_U=\int_0^U K_u\,du,\qquad\|B_U\|\le\int_0^U\|K_u\|\,du','Construire ensemble une tête structurée et les sources des couplages à certifier.','Le calcul positif à S=1/2 reste exploratoire : il faut une erreur de norme sur tout l’espace.',('schatten2','layers','errors'));r['legend']='B_U : opérateur commun ; U : plafond de coût ; K_u : concentration au niveau u ; intégrale : assembler les couches.';new.append(r)
        # Stable stages keep the elementary notions first and all prerequisites earlier.
        for r in new:
            if r['id']=='joint_cost':index=next(i for i,x in enumerate(rows) if x['id']=='gram')
            elif r['id']=='sublevel':index=next(i for i,x in enumerate(rows) if x['id']=='layers')
            elif r['id']=='schatten2':index=next(i for i,x in enumerate(rows) if x['id']=='layers')
            else:index=next(i for i,x in enumerate(rows) if x['id']=='inclusion')
            rows.insert(index,r)
        for r in rows:
            if r['id']=='coercivity':r['example']='Le certificat V647 prouve Q_W≥R/100 pour tous les tests et tous les supports 0<S≤3/8. La version V646 reste une autre preuve locale.'
        return rows
    module.lessons=lessons
    original_tools=module.tool_uses
    def tools():
        rows=original_tools()
        for r in rows:
            if r['id'] in ('layers','boundary','assembly','rounded'):r['execution']='V646, preuve historique conservée : '+r['execution']
        rows.extend([
            dict(id='projected_hs',name='Concentration projetée avec erreurs',question='Les accords entre fréquences peuvent-ils certifier le signe ?',implementation='projected_concentration.certify',input='Port S=3/8, maillages rationnels, Gram,160bits et64bits fixes',output='Concentrations par couches puis Q≥masse/12 et R/100',execution='2000cellules ;970retenues au dernierniveau ;470935paires parparité ;marge massique>0,0858.',status='certificat sur tous les tests',limit='Famille bornée et un seul premier ; la couverture globale reste ouverte.',doors=['Arithmétique','Tête praticable','Couverture']),
            dict(id='common_operator',name='Opérateur commun et compression',question='Peut-on garder le même test et construire une tête utile ?',implementation='v647_operator_diagnostic.py ; projected_concentration.head_tail_norm_bound',input='Multiplicateur conjoint, projection et toutes les couches',output='Opérateur commun ; borne de bloc sous hypothèses tête/queue/sources',execution='Deux résolutions exécutées. S=1/2 : marge de Nyström+0,005903, non certifiée.',status='lemme et diagnostic',limit='Les trois bornes tête,queue,couplage ne sont pas encore certifiées pour ce support.',doors=['Tête praticable','Couplages','Couverture']),
            dict(id='cell_errors',name='Cellules et erreurs de second ordre',question='Comment garantir des sous-niveaux discontinus sans deviner leurs racines ?',implementation='projected_concentration.validate_grid ; certify',input='Bornes de b sur chaque cellule et dérivées du noyau',output='Sur-ensembles certifiés et erreurs des milieux en O(h²)',execution='Queue exclue par a(40)>7,2224 ; erreurs ajoutées avant la racineSchatten2.',status='preuve et intervalles',limit='La précision de la grille seule ne constitue pas une garantie.',doors=['Arithmétique','Tête praticable'])])
        # Spaces are part of pedagogy: display numbers and names as readable prose.
        for r in rows:
            for key in ('input','output','execution','limit'):
                import re
                r[key]=re.sub(r'(?<=[0-9])(?=[A-Za-zÀ-ÿ])|(?<=[A-Za-zÀ-ÿ])(?=[0-9])',' ',r[key])
        return rows
    module.tool_uses=tools
