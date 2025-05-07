#  Création d'un site web sur la météo

##  Description
Ce projet est un site web interactif fournissant des prévisions météo complètes, intégrant un backend de machine learning pour des prédictions personnalisées et des fonctionnalités avancées d'information environnementale.

---

##  Technologies utilisées

- **API en Python avec Machine Learning**
- **Backend en PHP**
- **Frontend en HTML / CSS / JavaScript**

---

##  Fonctionnalités principales

- **Prévisions sur 15 jours** : Affichage complet de la météo pour les 15 jours à venir.
- **Santé et environnement** : Données sur la qualité de l'air, niveaux de pollen et pollution.
- **Données historiques** : Courbes d'évolution de la température et des précipitations pour les dernières 24 heures.
- **Géolocalisation automatique** : Possibilité d'obtenir les prévisions en fonction de la position actuelle de l'utilisateur, avec option de modification manuelle.

---

##  Ergonomie et design

- **Structuration de l'information** : Les indicateurs principaux (matin, après-midi, soir) sont mis en avant pour une meilleure lisibilité.
- **Ergonomie de l'interface** : Minimisation des boutons et éléments supplémentaires pour une lecture optimisée.
- **Interface épurée** : Simplicité et intuitivité centrées sur les informations principales.

---

##  Weather App Trello

- **lien Trello**: https://trello.com/b/Z9J4CJE4/weather-app

##  Lancement du projet

1. **Changer le compte pour phpmyadmin**
    ![Logo du projet](./assets/logo.png)

2. **Avoir les données de la machine learning** :
   ```bash
   cd weather-app/API || python marchlearn.py

3. **Lancement du site** :
   ```bash
   cd weather-app/API || python api.py
