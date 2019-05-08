# p14_Dejaegher_Elemva
code source du projet p14


Usage
Voici le fonctionnement final de notre projet, en partant du principe que le matériel utilisé est similaire au notre (manette et shield raspberry notamment) :

Réglages et pré-requis

*Il est tout d'abord nécessaire de télécharger les prérequis sur le raspberry (et sur le PC en cas de non-utilisation de Google Colab)
*Connecter les moteurs au shield et effectuer les réglages nécessaires. Il est notamment indispensable de déterminer la plage d'angle d'utilisation des (servo)moteurs : angle min et angle max. Ceci peut être fait à l'aide de <code>servotest.py</code>. 
*Il faut désormais régler la camera, c'est à dire son inclinaison, sa hauteur (de manière à voir correctement le circuit) et enfin déterminer si elle est droite ou à l'envers.
*Adapter le fichier constantes.py en fonctions des résultats précédents.

Utilisation (mode 3 directions)

*Connecter en ssh la raspberry. L'utilisation d'un écran est également possible mais moins pratique.
*Allumer la manette et lancer sur la raspberry le programme suivant en précisant un délais, 0.1 par exemple.
 python3 manual_drive.py <délais de capture en secondes>
*Mettre en marche la voiture, il faut alors activer la capture d'images et réaliser plusieurs tours de piste.
*(optionnel)Pour assurer la qualité du dataset, il est possible d'insister dans les passages difficiles en réalisant plusieurs passages. Egalement on peut ensuite supprimer les images mal labialisée en les contrôlant.
*De préférence sur Google Colab (jupyter également possible, avec un PC puissant), lancer le code <code>traitement.ipynb</code> et uploader le dataset. Suivre ensuite les différentes étapes sur ce code (les fonctions se lancent par "bloc", par simple pression sur l'icone exécuter, une par une et dans l'ordre. 
*Télécharger le modèle au format .h5 ainsi obtenu et le mettre sur la raspberry dans le même répertoire que les autres fonctions.
*Poser la voiture sur la piste et executer le code d'auto-pilotage en précisant le modèle. Le modèle met une trentaine de secondes à charger.
 python3 auto_drive.py <nom du modèle>
*Si tout s'est bien passé la voiture suit désormais la piste toute seule !
