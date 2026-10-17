"""Three bridges added after the existing forty progressive lessons."""
import pedagogy_v648_extension
def extend(m):
    pedagogy_v648_extension.extend(m);base=m.lessons;tools=m.tool_uses
    def lessons():
        rows=base();e=m.entry
        specs=[
            ('prime_phase',2,'Phase et puissance','Une phase indique où en est une oscillation dans son cycle. Répéter un déplacement répète aussi sa phase.','Le déplacement de 4 est deux fois celui de 2. Sa phase vaut le carré de celle de 2, mais son poids utilise toujours log 2.',r'z_{p^m}=z_p^m,\qquad z_p=e^{it\log p}','Garder la relation entre un premier et ses puissances dans le coût conjoint.','Les phases ne sont pas des tirages indépendants. Une compression dans une boîte peut couper les déplacements.',('prime','fourier'),'z : phase complexe de module 1 ; p : premier ; m : nombre de répétitions ; t : fréquence.'),
            ('edge_multiplicity',3,'Compter les attaches locales','Une attache relie deux bandes. Quand une zone appartient aux deux bandes, elle porte deux contributions.','À S=0,7, les bandes du premier 2 se recouvrent au centre : compter une seule fois cette zone manquerait une contribution.',r'D_q=c_q(\mathbf1_{\rm gauche}+\mathbf1_{\rm droite})','Additionner toutes les factures premières en conservant leurs lieux et recouvrements.','Le symbole 1 vaut 1 dans une bande et 0 ailleurs. La somme des deux symboles peut valoir 2.',('edge','prime'),'D_q : densité locale d’attaches ; c_q : poids positif ; les deux indicatrices comptent séparément.'),
            ('joint_payment',4,'Payer ensemble avec une énergie','On compare la facture de toutes les attaches au coût d’énergie déjà imposé à chaque endroit. On prend le plus grand rapport.','À S=1, le rapport joint est inférieur à 0,796. Additionner les rapports séparés donnerait plus de 1,24.',r'|Q_{\rm pr}|\le\alpha\mathcal E,\qquad\alpha=\sup D/V','Conserver une réserve d’énergie et contrôler le nouveau premier près de son seuil.','Ce paiement ne prouve pas le signe de Q : la masse soustraite reste à payer. Une borne relative en énergie n’est pas une petite norme L².',('edge_multiplicity','boundary','energy'),'alpha : plus grand rapport ; D : facture locale ; V : coût minimal local ; E : énergie.')]
        for id,stage,name,meaning,example,latex,purpose,guard,prereqs,legend in specs:
            r=e(id,stage,name,meaning,example,latex,purpose,guard,prereqs);r['legend']=legend
            target='gram' if stage==2 else ('matrix_positive' if stage==3 else 'inclusion')
            rows.insert(next(i for i,x in enumerate(rows) if x['id']==target),r)
        for r in rows:
            if r['id']=='joint_cost':r.update(name='Coût conjoint',meaning='L’énergie et les phases des premiers sont gardées dans une seule règle, pour la même fonction.',guard='V649 établit le coût multi-premiers exact. Sa positivité ne prouve pas celle de la forme après soustraction de la masse.')
        return rows
    def uses():
        r=tools()
        r.extend([
            dict(id='multi_phase',name='Phases et puissances liées',question='Quels termes premiers sont actifs et quelles phases partagent-ils ?',implementation='multi_prime_compensation.active_powers ; joint_multiplier',input='Support rationnel, fréquences, intervalles log et coefficients',output='Liste des puissances, coût conjoint et budgets de dérivées',execution='2, 3 puis 4 correctement distingués ; seuils ambigus refusés.',status='identité et intervalles',limit='Le coût positif b ne garantit pas le signe de b−C.',doors=['Arithmétique']),
            dict(id='joint_edge',name='Paiement des bandes conjointes',question='Peut-on payer tous les premiers sans réutiliser la même énergie ?',implementation='multi_prime_compensation.joint_edge_payment',input='Bandes avec multiplicité, potentiel V et support',output='Supremum D/V encadré par segments exacts',execution='Sept supports exécutés ; S=1 : alpha<0,796 contre somme séparée>1,24.',status='paiement relatif certifié',limit='Alpha encadre une enveloppe suffisante, pas la norme optimale ni le signe complet de Q.',doors=['Arithmétique','Couplages','Couverture']),
            dict(id='threshold_transport',name='Petite dette au nouveau seuil',question='Une bande étroite produit-elle une petite perturbation ?',implementation='multi_prime_compensation.joint_edge_payment(..., only_q=[3])',input='Excès de support après le seuil d’un nouveau terme',output='Dette relative à E et R tendant vers zéro',execution='Cinq approches du seuil de 3 exécutées ; décroissance logarithmique.',status='lemme et borne relative',limit='Le saut L² demeure. Transporter la forme de base et les moments entre supports reste nécessaire.',doors=['Couplages','Couverture'])])
        return r
    m.lessons=lessons;m.tool_uses=uses
