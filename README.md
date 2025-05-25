# Espoir Sportif de Chorbane - Application Web

Application web complète pour l'Espoir Sportif de Chorbane, une équipe de football tunisienne. Cette application centralise toutes les informations pertinentes pour l'équipe, les joueurs, le staff et les supporters, et facilite la gestion administrative et sportive.

## Fonctionnalités

### Module Public (Accès Ouvert)

- **Page d'Accueil** : Actualités récentes, prochain match, galerie photo/vidéo, informations de contact
- **Actualités** : Liste chronologique des articles et annonces avec recherche
- **Calendrier des Matchs** : Affichage des matchs passés et à venir avec filtrage
- **Classement** : Affichage dynamique du classement actuel de l'équipe
- **Équipe** : Liste des joueurs et du staff avec fiches détaillées
- **Partenaires** : Liste des partenaires du club avec leurs logos et liens

### Module Administration (Accès Authentifié)

- **Authentification** : Système de connexion sécurisé avec gestion des rôles
- **Gestion des Actualités** : Interface CRUD avec éditeur de texte riche
- **Gestion des Matchs** : Ajout/modification/suppression de matchs et saisie des statistiques
- **Gestion des Joueurs** : Interface CRUD pour les joueurs et leurs fiches
- **Gestion du Staff** : Interface CRUD pour les membres du staff
- **Gestion des Statistiques** : Génération automatique des statistiques individuelles et collectives
- **Gestion des Utilisateurs** : Interface pour la gestion des comptes et des rôles

## Technologies Utilisées

### Frontend
- Angular 16+
- Bootstrap 5
- Bootstrap Icons
- RxJS

### Backend
- Python Flask
- SQLAlchemy
- Flask-JWT-Extended
- Marshmallow

### Base de Données
- PostgreSQL

## Installation

### Prérequis
- Node.js et npm
- Python 3.8+
- PostgreSQL

### Installation du Frontend
```bash
make install-frontend
```

### Installation du Backend
```bash
make install-backend
```

### Configuration de la Base de Données
Modifiez le fichier `backend/config.py` pour configurer la connexion à PostgreSQL.

### Initialisation de la Base de Données
```bash
make migrate-db
```

### Génération de Données de Test
```bash
make seed-data
```

## Démarrage de l'Application

### Démarrer l'Application Complète
```bash
make run
```

### Démarrer Uniquement le Frontend
```bash
make run-frontend
```

### Démarrer Uniquement le Backend
```bash
make run-backend
```

## Structure du Projet

### Frontend
```
frontend/
├── src/
│   ├── app/
│   │   ├── player.model.ts
│   │   ├── player.service.ts
│   │   ├── players.component.ts
│   │   ├── app.module.ts
│   │   ├── app.component.ts
│   │   ├── app-routing.module.ts
│   │   └── home/
│   │       └── home.component.ts
│   ├── environments/
│   │   └── environment.ts
│   ├── index.html
│   └── main.ts
└── package.json
```

### Backend
```
backend/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── schemas.py
├── config.py
├── main.py
├── requirements.txt
└── seed_data.py
```

## Licence
Ce projet est sous licence MIT.