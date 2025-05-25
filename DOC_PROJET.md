# Documentation technique - Espoir Sportif de Chorbane

## 1. Installation et setup

- `make install-frontend` : installe les dépendances Angular
- `make install-backend` : crée l'environnement virtuel Python et installe les dépendances Flask
- `make migrate-db` : initialise et applique les migrations PostgreSQL
- `make seed-data` : injecte 30 joueurs, 15 équipes, 20 matchs fictifs avec Faker
- `make run` : lance simultanément le front (Angular) et le back (Flask)

## 2. Structure des dossiers

- `frontend/` :
  - `src/app/players.component.ts` : composant standalone Angular pour la gestion des joueurs
  - `src/app/player.service.ts` : service Angular pour consommer l'API Flask
  - `src/app/player.model.ts` : interface TypeScript Joueur
- `backend/` :
  - `app/models.py` : modèles SQLAlchemy (Player, Team, Match)
  - `app/routes.py` : endpoints Flask REST (CRUD joueurs)
  - `app/schemas.py` : schémas Marshmallow
  - `seed_data.py` : génération de données fictives
  - `config.py` : configuration PostgreSQL

## 3. Endpoints API principaux

- `GET /players` : liste des joueurs
- `POST /players` : ajouter un joueur
- `PUT /players/<id>` : modifier un joueur
- `DELETE /players/<id>` : supprimer un joueur

## 4. Tests

- Frontend :
  - `ng test` (dans `frontend`) pour lancer les tests unitaires Angular
- Backend :
  - À compléter (Pytest recommandé)

## 5. Processus de développement

1. Modifier les modèles dans `backend/app/models.py` si besoin
2. Appliquer les migrations : `make migrate-db`
3. Générer des données : `make seed-data`
4. Développer les composants Angular dans `frontend/src/app/`
5. Lancer le projet : `make run`

## 6. Astuces

- Pour changer la connexion PostgreSQL, modifier `backend/config.py`
- Pour ajouter d'autres modules (staff, matchs, etc.), suivre l'exemple du module joueurs
- Pour toute question, voir le README ou contacter l'équipe

---

Documentation générée automatiquement.
