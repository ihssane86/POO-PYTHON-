from collections import deque
import datetime

class Livre:
    def _init_(self, titre, auteur, isbn):
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        self.date_ajout = datetime.date.today()
        self.disponible = True
        self.nb_emprunts = 0 

    def afficher_info(self):
        print(f"{self.titre} par {self.auteur} (ISBN: {self.isbn})")

    def emprunter(self):
        if self.disponible:
            self.disponible = False
            self.nb_emprunts += 1
            return True
        return False

    def retourner(self):
        self.disponible = True


class Utilisateur:
    def _init_(self, utilisateur_id, nom):
        self.id = utilisateur_id
        self.nom = nom
        self.livres_empruntes = {}  # ISBN -> date_emprunt
        self.historique_emprunts = []
        self.penalise = False
        self.retards = 0

    def emprunter_livre(self, bibliotheque, isbn):
        if len(self.livres_empruntes) >= 3:
            print("Limite de 3 livres atteinte.")
            return False
        if self.penalise:
            print("Utilisateur pénalisé pour retards.")
            return False
        return bibliotheque.emprunter_livre(self.id, isbn)

    def retourner_livre(self, bibliotheque, isbn):
        return bibliotheque.retourner_livre(self.id, isbn)
# permet de vérifier si un utilisateur a retardé dans le retour d'un livre.
#  Si l'utilisateur a retardé, la méthode met à jour l'état de l'utilisateur 
# et enregistre le retard.

    def check_retard(self):
        today = datetime.date.today()
        for isbn, date_emprunt in list(self.livres_empruntes.items()):
            delta = (today - date_emprunt).days
            if delta > 15:
                print(f"Retard détecté pour le livre {isbn}")
                self.retards += 1
                del self.livres_empruntes[isbn]
                if self.retards >= 3:
                    self.penalise = True
                    print(f"{self.nom} est désormais pénalisé.")


class Bibliotheque:
    def _init_(self, nom):
        self.nom = nom
        self.livres = {}  # ISBN -> Livre
        self.utilisateurs = {}  # ID -> Utilisateur
        self.reservations = {}  # ISBN -> deque(Utilisateurs)

    def reserver_livre(self, utilisateur_id, isbn):
        """Ajoute un utilisateur à la file d'attente d'un livre indisponible."""
        if utilisateur_id not in self.utilisateurs:
            print("Erreur : Utilisateur non trouvé.")
            return False
        if isbn not in self.livres:
            print("Erreur : Livre non trouvé.")
            return False

        utilisateur = self.utilisateurs[utilisateur_id]
        livre = self.livres[isbn]

        if not livre.disponible:
            if isbn not in self.reservations:
                self.reservations[isbn] = deque()

            # Vérifier si déjà réservé
            for u in self.reservations[isbn]:
                if u.id == utilisateur_id:
                    print("Vous avez déjà réservé ce livre.")
                    return False

            self.reservations[isbn].append(utilisateur)
            print(f"{utilisateur.nom} a été ajouté à la file d'attente pour '{livre.titre}'.")
            return True
        else:
            print("Ce livre est disponible. Vous pouvez l'emprunter directement.")
            return False

    def emprunter_livre(self, utilisateur_id, isbn):
        if utilisateur_id not in self.utilisateurs:
            print("Erreur : Utilisateur non trouvé.")
            return False
        if isbn not in self.livres:
            print("Erreur : Livre non trouvé.")
            return False

        utilisateur = self.utilisateurs[utilisateur_id]
        livre = self.livres[isbn]

        if not livre.disponible:
            print("Livre indisponible.")
            return False

        if livre.emprunter():
            utilisateur.livres_empruntes[livre.isbn] = datetime.date.today()
            utilisateur.historique_empruntes.append(livre.isbn)
            print(f"{utilisateur.nom} a emprunté '{livre.titre}'.")
            return True
        return False

    def retourner_livre(self, utilisateur_id, isbn):
        if utilisateur_id not in self.utilisateurs:
            print("Erreur : Utilisateur non trouvé.")
            return False
        if isbn not in self.livres:
            print("Erreur : Livre non trouvé.")
            return False

        utilisateur = self.utilisateurs[utilisateur_id]
        livre = self.livres[isbn]

        if isbn in utilisateur.livres_empruntes:
            livre.retourner()
            del utilisateur.livres_empruntes[isbn]
            print(f"{utilisateur.nom} a rendu '{livre.titre}'.")

            # Proposer aux réservataires
            if isbn in self.reservations and len(self.reservations[isbn]) > 0:
                next_user = self.reservations[isbn].popleft()
                print(f"Le livre '{livre.titre}' est maintenant réservé pour {next_user.nom}.")
                # Optionnel : notification automatique ou alerte
            return True
        print("Aucun emprunt trouvé.")
        return False
