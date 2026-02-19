# Part Program Analyzer

## Auteurs
**Dolci Marco** & **Toussaint Guillaume**

## Description
Ce projet a pour objectif de fournir une application capable d'analyser un programme de machine-outil (G-Code) afin d'extraire et de mettre en évidence des données pertinentes pour anticiper le comportement de la machine.  
Parmi les fonctionnalités proposées :

- Estimation du **temps de fabrication** de la pièce.
- Calcul du **temps d'usinage** et de la **distance parcourue** par chaque outil pour anticiper son remplacement avant rupture.
- Visualisation des **trajectoires des outils**.
- Et plus encore...

## Statut du projet
Ce projet constitue une première version et est destiné à évoluer au fil du temps avec de nouvelles fonctionnalités et améliorations.

## Aide et Ressources
La majeure partie du projet a été développée en appliquant les compétences acquises au cours de notre formation ainsi que par notre expérience personnelle. 
Toutefois, nous avons utilisé ChatGPT pour nous assister sur certains aspects spécifiques du projet, notamment :
- L'élaboration de certaines formules mathématiques.
- L'exploration des propriétés et fonctionnalités de Tkinter.
- La génération des expressions régulières (Regex).

## Installation et utilisation
### Prérequis
- Python 3
- Bibliothèques nécessaires (requirements.txt`)

### Installation
1. Clonez le dépôt :
   ```bash
   git clone https://github.com/mwdolci/CAS-IDD_Python_Project_PartProgramAnalyzer.git
   ```
2. Accédez au répertoire du projet :
   ```bash
   cd CAS-IDD_Python_Project_PartProgramAnalyzer
   ```
3. Créez un environnement virtuel :
   ```bash
   python -m venv venv
   ```
   ou 
   ```bash
   py -m venv venv
   ```
4. Activez l'environnement virtuel :
   ```bash
   source venv/Scripts/activate 
   ```
5. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

### Utilisation
Exécutez le script principal :
```bash
python main.py
```

Pour tester l'application, il est possible d'utiliser les programmes G-Codes (.anc) et solide 3D (.stl) se trouvant dans le répertoire "data_testing".

### Manipulateur du viewer 3D:

Différentes touches permettent d'exécuter des fcontions spécifiques:
- "Space" → masquer/afficher la pièce.
- "Escape" → masquer/afficher toutes les trajectoires.
- "Up" et "Down" → défiliement des trajectoires rapide et travail par outil.