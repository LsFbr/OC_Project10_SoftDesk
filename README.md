# SoftDesk

SoftDesk est une application back-end développée avec Django REST Framework. Elle propose une API REST sécurisée par JWT, destinée aux entreprises pour faciliter la gestion collaborative de projets. Elle permet de créer et gérer des projets, d’y associer des utilisateurs, de suivre les problèmes (issues) et d’échanger grâce à des commentaires.

---
# Déploiement

## Prérequis

* **Python** 3.11+
* **Git**
* **Poetry** 2.x
* **SQLite** (fourni avec Python)

---

## 0. Placez-vous dans le répertoire où vous souhaitez cloner le projet

```bash
cd chemin/vers/le/repertoire
```

## 1) Cloner le dépôt

```bash
git clone https://github.com/LsFbr/OC_Project10_SoftDesk.git
cd OC_Project10_SoftDesk
```



## 2) Créer l’environnement virtuel **dans le projet** et installer les dépendances

```bash
poetry config virtualenvs.in-project true --local
poetry install
```

* Crée `.venv/` à la racine et installe les paquets définis dans `pyproject.toml` / `poetry.lock`.



## 3) Démarrer le serveur de développement

```bash
poetry run python manage.py runserver
```

Accès : `http://127.0.0.1:8000/`

---
