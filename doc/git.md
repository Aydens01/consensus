# Git

## Installation

Pour récupérer le projet sur le github en local :
```sh
$ git clone https://github.com/Aydens01/consensus.git
```
Cela va créer un dossier *consensus* contenant l'intégralité du projet.

## Mise à jour en local

Il y a deux cas :

* Vous possédez des modifications en local que vous souhaitez conserver
* Vous ne possédez pas de modifications en local ou ne souhaitez pas le conserver.

*Note : je conseille d'utiliser les commandes du premier cas car elles permettent d'éviter les mauvaises surprises.*

### Premier cas

```sh
# Si vous ne vous trouvez pas dans le dossier du projet
$ cd consensus
# Sauvegarde des modifications du projet locales (celle-ci disparaîtront mais ce n'est que provisoire)
$ git stash
# Récupération des dernières modifications
$ git pull origin master
# Récupération de la sauvegarde précédemment faîte
$ git stash pop
``` 

Il est possible que git à la suite de cette opération vous informe qu'il y a des conflits dans certains de vos fichiers. Il suffira de résoudre manuellement les conflits.

### Second cas

Pour mettre à jour le dossier *consensus* en local, il suffit d'exécuter la commande : 
```sh
# Si vous ne vous trouvez pas dans le dossier du projet
$ cd consensus
# Récupération des dernières modifications
$ git pull origin master
``` 

## Mise à jour du projet sur github

Après avoir modifié le projet en local, vous voudrez certainement mettre la nouvelle version en ligne. Pour cela, il suffira d'effectuer les commandes suivantes : 
```sh
# Si vous ne vous trouvez pas dans le dossier du projet 
$ cd consensu
$ git add .
$ git commit
```
Vous arriverez alors sur l'éditeur vi où vous pourrez mettre votre message de commit. (Ce message est important car il permet aux autres de savoir ce que vous avez changé/ajouté/supprimé sur le projet).

*Rappel pour utiliser vi :*
* Pour passer en mode écriture tapez : **i**.
* Pour sortir du mode écriture : **Echap** (nécessaire pour quitter taper les commandes suivantes)
* Pour sortir de l'éditeur et enregistrer ce qu'on a écris : **:wq**

Après avoir fermé l'éditeur vi, il suffira d'envoyer tout ça en ligne :
```sh
$ git push origin master
```