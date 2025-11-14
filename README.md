# SoftDesk

SoftDesk est une application back-end développée avec Django REST Framework. Elle propose une API REST sécurisée par JWT, destinée aux entreprises pour faciliter la gestion collaborative de projets. Elle permet de créer et gérer des projets, d'y associer des utilisateurs, de suivre les problèmes (issues) et d'échanger grâce à des commentaires.

---

## Prérequis

* **Python** 3.12+
* **Git**
* **Poetry** 2.x
* **SQLite** (fourni avec Python)

---

## Installation et configuration

### 1. Cloner le dépôt

```bash
git clone https://github.com/LsFbr/OC_Project10_SoftDesk.git
cd OC_Project10_SoftDesk
```

### 2. Configurer Poetry et installer les dépendances

```bash
poetry config virtualenvs.in-project true --local
poetry install
```

Cette commande :
* Configure Poetry pour créer l'environnement virtuel dans le dossier `.venv/` à la racine du projet
* Installe toutes les dépendances définies dans `pyproject.toml` et `poetry.lock`

### 3. Utiliser l'environnement virtuel

Vous avez deux options :

**Option A : Utiliser `poetry run` (recommandé - plus simple)**
```bash
poetry run python manage.py <commande>
```

Avec `poetry run`, vous n'avez **pas besoin** d'activer manuellement l'environnement virtuel. Poetry détecte et utilise automatiquement l'environnement virtuel du projet.

**Option B : Activer le shell Poetry (pour des sessions interactives)**
```bash
poetry shell
```

Après cette commande, vous pouvez exécuter les commandes directement sans `poetry run`.

### 4. Appliquer les migrations de base de données

```bash
poetry run python manage.py migrate
```

### 5. (Optionnel) Créer un superutilisateur

Pour accéder à l'interface d'administration Django :

```bash
poetry run python manage.py createsuperuser
```

### 6. Démarrer le serveur de développement

```bash
poetry run python manage.py runserver
```

L'API sera accessible à l'adresse : `http://127.0.0.1:8000/`

---

## Commandes utiles

### Gestion des migrations

```bash
# Créer de nouvelles migrations
poetry run python manage.py makemigrations

# Appliquer les migrations
poetry run python manage.py migrate

# Voir l'état des migrations
poetry run python manage.py showmigrations
```


---

## Documentation de l'API

La documentation complète de l'API est disponible à l'adresse suivante : `https://documenter.getpostman.com/view/36688365/2sB3WvNJjN`
