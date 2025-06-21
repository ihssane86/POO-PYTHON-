def afficher_statistiques(self):
        """Affiche les statistiques clés de la bibliothèque."""
        print("\n📊 Statistiques de la bibliothèque")
        
        # Top 5 des livres les plus empruntés
        top_livres = sorted(self.livres.values(), key=lambda x: x.nb_emprunts, reverse=True)
        print("\n📚 Livres les plus empruntés :")
        for i, livre in enumerate(top_livres[:5], 1):
            print(f"{i}. {livre.titre} par {livre.auteur} - Emprunts : {livre.nb_emprunts}")

        # Nombre total d’emprunts actifs
        total_actifs = sum(len(u.livres_empruntes) for u in self.utilisateurs.values())
        print(f"\n📦 Nombre d’emprunts en cours : {total_actifs}")

        # Utilisateurs pénalisés
        penalises = [u for u in self.utilisateurs.values() if u.penalise]
        print(f"\n⚠ Utilisateurs pénalisés ({len(penalises)}) :")
        for user in penalises:
            print(f"- {user.nom}")
