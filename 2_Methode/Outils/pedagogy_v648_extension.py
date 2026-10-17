"""Extend the five-stage course with four operator-certificate concepts."""
import pedagogy_v647_extension
def extend(m):
    pedagogy_v647_extension.extend(m);old_lessons=m.lessons;old_tools=m.tool_uses
    def lessons():
        rows=old_lessons();e=m.entry
        additions=[
            e('cardinal_frame',3,'Repères et cadre cardinal','Des polynômes peuvent être décrits par leurs valeurs à des repères. Les poids de Gauss rendent leurs accords exactement calculables.','Un cardinal vaut1 à son repère et0 aux autres. Après division par la racine de son poids, les cardinaux forment des directions orthonormales.',r'\int l_i(x)l_j(x)\,dx=w_i\delta_{ij}','Traduire une tête polynomiale en coordonnées sans changer sa norme L².','Cette exactitude concerne les polynômes du degré prévu. Les nœuds et les poids doivent être certifiés.',('gram','support')),
            e('interpolation_error',3,'Interpolation et reste','L’interpolation construit une fonction qui passe exactement par les valeurs choisies. Le reste mesure ce qu’elle peut manquer entre les repères.','Même si deux courbes passent par les mêmes points, elles peuvent différer ailleurs. Ici une borne couvre cette différence partout.',r'\|r-I_Nr\|_2\le\varepsilon_N','Passer des valeurs finies aux ondes entières avec une erreur contrôlée.','Correspondre aux repères ne suffit pas. Le reste exige des dérivées et le domaine de la fonction.',('cardinal_frame','projection')),
            e('operator_error',4,'Erreur sur tous les tests','Une erreur opératoire borne le changement produit sur chaque fonction, pas seulement sur quelques valeurs de grille.','Si cette erreur vautδ, toutes les interactions omises entre tête et queue sont également bornées parδ.',r'\|B-\widetilde B_N\|\le\delta','Contrôler ensemble la norme de l’opérateur, sa queue et les sources croisées.','La norme et le domaine font partie du contrat. Pour B on utilise L² ; les formes non bornées gardent leurs propres exigences.',('common_operator','interpolation_error','errors')),
            e('minorant_sources',4,'Sources du minorant','Un minorant est une balance plus petite que la balance étudiée. Prouver son signe suffit ; ses attaches ne sont pourtant pas identiques à celles de la balance entière.','Les sources de A_U sont bornées par le mêmeδ que sa queue. La forme Q_W possède un supplément positif dont les sources demandent leur propre calcul.',r'\operatorname{Gram}(\rho_i)\preceq\delta^2I','Assembler la dette de Schur du minorant dans une base orthonormale.','Ne pas renommer ces sources en sources fortes de Q_W. Le signe se transporte, les sources exactes non.',('operator_error','schur'))]
        legends={
            'cardinal_frame':'l_i : cardinal du repèrei ; w_i : poids positif ; δ_ij :1 si i=j,0 sinon ; intégrale : accord de deux fonctions.',
            'interpolation_error':'r : onde projetée ; I_N : interpolation avecN repères ; ε_N : borne de la différence ; || ||₂ : norme L².',
            'operator_error':'B : opérateur commun entier ; B_N avec tilde : approximation finie ; δ : majorant de différence sur tous les tests.',
            'minorant_sources':'ρ_i : source croisée du minorant ; Gram : tableau des accords ; ≼ : domination des formes ; I : identité dans une base orthonormale.'}
        for r in additions:
            r['legend']=legends[r['id']]
            target='layers' if r['stage']==3 else 'inclusion'
            rows.insert(next(i for i,x in enumerate(rows) if x['id']==target),r)
        for r in rows:
            if r['id']=='common_operator':r['guard']='La norme est certifiée à S=1/2 en V648, après toutes les erreurs. L’extension multi-premiers et la couverture non bornée restent ouvertes.'
            if r['id']=='coercivity':r['example']='V648 prouve Q_W≥R/2000 pour tous les tests et0<S≤1/2. V647 garde sa borne plus forteR/100 sur les supportsS≤3/8.'
        for r in rows:
            for k in ('meaning','example','purpose','guard','legend'):
                r[k]=r.get(k,'').replace('repèresS','repères S').replace('supportsS','supports S').replace('forteR','forte R').replace('repèrei','repère i').replace('avecN','avec N').replace('vaut1','vaut 1').replace('et0','et 0').replace('vautδ','vaut δ')
        return rows
    def tools():
        rows=old_tools()
        for r in rows:
            if r['id']=='common_operator':
                r.update(implementation='common_operator_certificate.certify',input='S=1/2,80nœuds certifiés et90000cellules fréquentielles',output='Norme entière, erreurs, Q≥masse/250 et R/2000',
                    execution='Deux blocs de40 ; Bareiss exact ; marge massique>0,0047, tous tests.',status='certificat local exécuté',limit='Un seul premier ; sources du minorant B/A, distinctes des sources fortes de Q.')
        rows.extend([
            dict(id='gauss_frame',name='Cadre de Gauss et vecteurs encadrés',question='Les coordonnées finies représentent-elles les bonnes fonctions ?',implementation='common_operator_certificate.certify_gauss ; trig_interval',input='80racines Legendre, poids et ondes déjà projetées',output='Cadre orthonormal exact, restes et vecteurs pondérés encadrés',execution='Racines isolées en entiers ; sinus par polynômes intervalle ; erreur vectorielle<3·10⁻¹³.',status='preuve et intervalles',limit='La projection des moments et l’interpolation ne sont pas supposées commuter.',doors=['Tête praticable','Couplages']),
            dict(id='exact_ceiling',name='Plafond matriciel exact',question='La valeur propre flottante peut-elle devenir une borne ?',implementation='common_operator_certificate.validated_matrix_norm ; bareiss_spd',input='Matrice quantifiée symétrique et plafond candidat',output='Déterminants principaux exacts prouvant τI−M>0',execution='Deux blocs40×40 validés, plafonds1,63860 et1,48237.',status='algèbre exacte exécutée',limit='La matrice seule exige encore toutes les erreurs pour couvrir l’opérateur infini.',doors=['Tête praticable']),
            dict(id='minorant_assembly',name='Assembler tête, sources et queue',question='Une même erreur peut-elle certifier toutes les attaches ?',implementation='common_operator_certificate.assemble_minorant_contract',input='Plafond τ, erreur δ et constante positiveη',output='Queue positive, Gram source≤δ²I, dette de Schur et marge',execution='Marge de Schur paire>0,00473 ; dette<0,000009.',status='certificat du minorant',limit='Sources de A_U dans L² ; pas les sources fortes de la forme originale Q_W.',doors=['Couplages','Tête praticable','Couverture'])])
        import re
        for r in rows:
            for k in ('input','output','execution','limit'):r[k]=re.sub(r'(?<=[0-9])(?=[A-Za-zÀ-ÿ])|(?<=[A-Za-zÀ-ÿ])(?=[0-9])',' ',r[k])
        return rows
    m.lessons=lessons;m.tool_uses=tools
