---
title: Projet 7 - Créez GrandPy Bot, le papy-robot
subtitle: Parcours OpenClassrooms - Développeur d'application Python
author:
  - 'Etudiant : Guillaume OJARDIAS'
  - 'Mentor : Erwan KERIBIN'
geometry: margin=1.5cm
---
# I. Contexte

Le but du projet est de créer un chatbot permettant à l'utilisateur de trouver l'adresse d'un lieu ainsi que d'avoir plus d'informations au sujet de ce lieu grâce à Wikipédia.

Le code source du projet est disponible à l'adresse suivante :
    => https://github.com/GuillaumeOj/YodaPy

L'application est déployée sur la plateforme Heroku à l'adresse suivante :
    => https://yoda-py.herokuapp.com/

Pour finir, les users stories utilisées pour l'élaboration de l'application sont disponibles ici :
    => https://trello.com/b/P17ksldE/yodapy

Le but de ce projet est de créer une application web tout en manipulant un certain nombre de connaissance :

- utilisation d'API,
- utilisation d'un framework (FLASK),
- utilisation du JavaScript (y compris AJAX),
- déploiement d'une application en ligne,
- réalisation d'une interface responsive (HTML5 + CSS3),
- mise en place de tests (module Pytest) pour un projet en mode TDD,
- et bien entendu utilisation du langage Python.

# II. Démarche

L'application suit le fonctionnement suivant.

1. L'utilisateur écrit un message, puis le soumet (touche `<Enter>` ou bouton `Envoyer`)
2. Un script JavaScript récupère le contenu du message, l'affiche dans un fil de discussion et l'envoi (en AJAX) à une page `/process` de l'application.
3. Sur la page `/process`, l'entrée utilisateur est envoyée à un `parser` qui va "normaliser" le message de la manière suivante :
    a. texte en minuscule, suppression des caractères accentués,
    b. séparation du texte en liste de phrase,
    c. répète la phrase contenant la question posée au bot,
    d. suppression des mots inutiles (stopwords),
    e. retour de la donnée
4. Une fois l'entrée utilisateur "parsé", celle-ci est envoyée à un module permettant la recherche de coordonnées géographique d'un lieu grâce à une recherche textuelle. Ici, le module fait appel à l'API fournie par [MapBox](https://www.mapbox.com/). Le module fait un choix de lieu (parmi la liste retournée par MapBox) en se basant sur l'indice `relevance` fourni par l'API et retourne les données sous forme de dictionnaire.
5. Les informations retournées par le module de recherche géographique, sont ensuite envoyées à un module permettant la recherche d'article sur la plateforme Wikipédia. Ce module va utiliser les coordonnées géographique du lieu pour faire une recherche Wikipédia grâce à l'API `GeoSearch` fournie par Wikipédia. Si un article existe, celui-ci est retournée à l'application toujours sous forme de dictionnaire.
6. Pour finir, l'application fait appel à un module appelé `Bot`permettant de retourner des phrases selon le contexte (adresse trouvée, article trouvé, demande non comprise, erreur grave, etc.)
7. Toute ces informations sont  retournées à la page principale sous forme de JSON.
8. Le script JavaScript reçoit le résultat de la requête AJAX et affiche dans le fil des messages sous forme de différents posts les informations retournées.

# III. Bilan du projet


