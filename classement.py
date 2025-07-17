import json
import pandas as pd
import time
import os
import sys
from matplotlib import pyplot as plt
import random

FICHIER_JSON = "EstimationRichesse.json"

# Fonctions de style alternatives
def kinche_style():
    """Style d'affichage amélioré"""
    print("\033[95m" + "="*60)
    print("\033[95m⚡ \033[1mWealthScan - Système d'Évaluation Financière\033[0m \033[95m⚡")
    print("="*60 + "\033[0m")

def matrix_rain(lines=5):
    """Effet visuel de pluie matricielle"""
    chars = "01"
    for _ in range(lines):
        print(' '.join(random.choice(chars) for _ in range(50)))
        time.sleep(0.1)

# Fonctions graphiques alternatives
def afficher_progression_richesse(score):
    """Affiche la progression de richesse"""
    print("\n\033[92mProgression financière:\033[0m")
    progression = min(100, int(score / 1000))
    bar = "▓" * (progression // 2) + "░" * (50 - progression // 2)
    print(f"[{bar}] {progression}%")
    
    if progression < 30:
        print("Phase: Débutant - Focus sur l'accumulation")
    elif progression < 70:
        print("Phase: Croissance - Investissements stratégiques")
    else:
        print("Phase: Maîtrise - Préservation du capital")

def afficher_graphique(values, labels):
    """Affiche un graphique en barres"""
    plt.figure(figsize=(10, 5))
    colors = ['#4CAF50', '#2196F3', '#9C27B0', '#FF9800']
    plt.bar(labels, values, color=colors)
    plt.title('Composition de la richesse')
    plt.ylabel('Valeur ($)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# Fonctions de menu alternatives
def afficher_menu(options, title="Menu"):
    """Affiche un menu interactif"""
    kinche_style()
    print(f"\n\033[1m{title}\033[0m")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    while True:
        try:
            choix = int(input("\n\033[94mVotre choix: \033[0m"))
            if 1 <= choix <= len(options):
                return options[choix-1]
            print("\033[91mChoix invalide. Veuillez réessayer.\033[0m")
        except ValueError:
            print("\033[91mVeuillez entrer un nombre.\033[0m")

def input_user(prompt, hidden=False):
    """Gère l'entrée utilisateur"""
    if hidden:
        import getpass
        return getpass.getpass(prompt)
    return input(prompt)

def clear_screen():
    """Efface l'écran de la console"""
    os.system('cls' if os.name == 'nt' else 'clear')

# =============================================
# Le reste du code original avec adaptations
# =============================================

def charger_donnees():
    try:
        with open(FICHIER_JSON, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("\033[91mCorruption du fichier! Création d'une nouvelle base...\033[0m")
        return []

def enregistrer_donnees(donnees):
    with open(FICHIER_JSON, "w") as f:
        json.dump(donnees, f, indent=4)

def calculer_score(profil):
    return (profil["revenus"] * 0.5 + 
            profil["actifs"] * 0.7 + 
            profil["investissements"] * 1.2) - profil["dettes"] * 0.9

def classer_profils(donnees):
    for profil in donnees:
        profil["score"] = calculer_score(profil)
    return sorted(donnees, key=lambda x: x["score"], reverse=True)

def afficher_trophee(rang):
    if rang == 1:
        print("\033[93m" + """
          .-=========-.
          \\'-=======-'/
          _|   .=.   |_
         ((|  {{GOLD}}  |))
          \\|   /|\\   |/
           \\__ '`' __/
             _`) (`_
           _/_______\\_
          /___________\\
        """ + "\033[0m")
    elif rang <= 3:
        print("\n\033[90m🥈 SILVER MEDAL\033[0m")
    elif rang <= 5:
        print("\n\033[33m🥉 BRONZE STAR\033[0m")

def afficher_resultats(nom, donnees_tries):
    clear_screen()
    matrix_rain(lines=3)
    
    df = pd.DataFrame(donnees_tries)
    df["rang"] = df["score"].rank(ascending=False, method="min").astype(int)
    utilisateur = df[df["nom"].str.lower() == nom.lower()]
    
    if utilisateur.empty:
        print(f"\n🔍 Aucun profil trouvé pour {nom}.")
        time.sleep(1.5)
        return

    utilisateur = utilisateur.iloc[0]
    kinche_style()
    
    # Affichage stylé
    print(f"\n\033[96m⚡ {'='*40} ⚡\033[0m")
    print(f"\033[1m👤 NOM:\033[0m {utilisateur['nom']}")
    print(f"\033[1m🏆 RANG:\033[0m {utilisateur['rang']}/{len(df)}")
    print(f"\033[1m💎 SCORE:\033[0m {utilisateur['score']:,} points")
    print(f"\033[96m⚡ {'='*40} ⚡\033[0m")
    
    # Détails financiers
    print("\n\033[94m📊 BREAKDOWN:\033[0m")
    print(f"| Revenus:       ${utilisateur['revenus']:>12,}")
    print(f"| Actifs:        ${utilisateur['actifs']:>12,}")
    print(f"| Investissements: ${utilisateur['investissements']:>8,}")
    print(f"| Dettes:        ${utilisateur['dettes']:>12,}")
    print("└" + "─"*38)
    
    afficher_trophee(utilisateur["rang"])
    message_motivant(utilisateur["rang"])
    
    # Graphique
    afficher_graphique(
        values=[
            utilisateur['revenus'],
            utilisateur['actifs'],
            utilisateur['investissements'],
            -utilisateur['dettes']
        ],
        labels=['Revenus', 'Actifs', 'Investissements', 'Dettes']
    )
    
    # Progression
    afficher_progression_richesse(utilisateur["score"])
    
    # Conseil
    print("\n\033[95m💡 CONSEIL STRATÉGIQUE:\033[0m")
    if utilisateur['dettes'] > utilisateur['revenus']:
        print("→ Priorité #1: Réduction des dettes (consolider vos crédits)")
    elif utilisateur['investissements'] < utilisateur['actifs']/2:
        print("→ Opportunité: Augmentez vos investissements productifs")
    else:
        print("→ Stratégie: Diversifiez votre portefeuille d'actifs")

def message_motivant(rang):
    print("\n\033[92m🔥 DIAGNOSTIC:\033[0m")
    if rang == 1:
        print("| Statut: MAÎTRE DE L'ÉCONOMIE")
        print("| Message: Votre empire inspire les générations futures")
    elif rang <= 3:
        print("| Statut: VISIONNAIRE FINANCIER")
        print("| Message: Votre ascension est irrésistible")
    elif rang <= 10:
        print("| Statut: STRATÈGE PROMETTEUR")
        print("| Message: Votre discipline porte ses fruits")
    else:
        print("| Statut: AMBITIEUX EN MARCHE")
        print("| Message: Chaque maître a commencé comme apprenti")

def animer_chargement(phrase, duree=2):
    print(f"\n{phrase}", end='', flush=True)
    for _ in range(5):
        print('.', end='', flush=True)
        time.sleep(duree/5)
    print()

def ajouter_utilisateur():
    clear_screen()
    print("\033[1m\033[95m" + "="*40)
    print("CRÉATION DE NOUVEAU PROFIL FINANCIER")
    print("="*40 + "\033[0m")
    
    nom = input_user("\n🔤 Nom complet: ")
    
    # Validation des entrées
    while True:
        try:
            revenus = int(input_user("💰 Revenus annuels ($): "))
            actifs = int(input_user("🏦 Actifs totaux ($): "))
            dettes = int(input_user("💳 Dettes totales ($): "))
            investissements = int(input_user("📈 Investissements actifs ($): "))
            break
        except ValueError:
            print("\033[91mErreur: Veuillez entrer des nombres valides\033[0m")
    
    donnees = charger_donnees()
    donnees.append({
        "nom": nom,
        "revenus": revenus,
        "actifs": actifs,
        "dettes": dettes,
        "investissements": investissements
    })
    enregistrer_donnees(donnees)
    
    animer_chargement("Cryptage des données financières")
    print(f"\n✅ {nom} ajouté avec succès !")
    time.sleep(1.5)

def afficher_classement(donnees):
    clear_screen()
    print("\033[1m\033[95m" + "="*40)
    print("CLASSEMENT DES FINANCIERS")
    print("="*40 + "\033[0m")
    
    top = donnees[:10]
    print(f"\n🏆 TOP {len(top)}\n")
    print(f"{'Rang':<5} {'Nom':<20} {'Score':<15} {'Statut':<10}")
    print("-"*50)
    
    for i, profil in enumerate(top, 1):
        statut = "👑" if i == 1 else "🚀" if i <= 3 else "⭐"
        print(f"{i:<5} {profil['nom']:<20} {profil['score']:<15,.0f} {statut:<10}")
    
    # Vérifier position utilisateur
    if len(donnees) > 10:
        print("\nℹ️ Votre position: Au-delà du top 10")
    
    input_user("\nAppuyez sur Entrée pour continuer...")

def lancer_interface():
    while True:
        clear_screen()
        matrix_rain(lines=2)
        print("\033[1m\033[36m" + "="*40)
        print("PORTAL FINANCIER AI")
        print("="*40 + "\033[0m")
        
        choix = afficher_menu([
            "🔍 Scanner un profil", 
            "✨ Créer nouveau profil",
            "🏆 Voir le classement",
            "🚪 Quitter"
        ], title="MENU PRINCIPAL")
        
        if choix == "🔍 Scanner un profil":
            nom = input_user("\n🔎 Nom à rechercher: ")
            donnees = charger_donnees()
            if not donnees:
                print("\033[93mAucun profil existant. Créez d'abord un profil.\033[0m")
                time.sleep(1.5)
                continue
                
            donnees_tries = classer_profils(donnees)
            afficher_resultats(nom, donnees_tries)
            
        elif choix == "✨ Créer nouveau profil":
            ajouter_utilisateur()
            
        elif choix == "🏆 Voir le classement":
            donnees = charger_donnees()
            if not donnees:
                print("\033[93mAucun profil existant. Créez d'abord un profil.\033[0m")
                time.sleep(1.5)
                continue
                
            donnees_tries = classer_profils(donnees)
            afficher_classement(donnees_tries)
            
        else:
            print("\n\033[92mFermeture du système. À votre succès futur!\033[0m")
            break

if __name__ == "__main__":
    # Initialisation
    print("\033[95mConnexion au système financier...\033[0m")
    time.sleep(1)
    lancer_interface()