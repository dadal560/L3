# Arbres AVL - Bibliothèque C

Implémentation d'une bibliothèque d'arbres AVL (arbres binaires de recherche auto-équilibrés) en C.

## Description

Un arbre AVL est un arbre binaire de recherche qui maintient automatiquement son équilibre après chaque insertion ou suppression. 


## Compilation

### Avec CMake

```bash
mkdir debug
cd debug
cmake ../../src/tree-avl/ -DCMAKE_INSTALL_PREFIX=../tmp -DCMAKE_BUILD_TYPE=Debug
make
```

### Installation de la bibliothèque

```bash
make install
```

### Exécution des tests

```bash
./test-tree-avl
```


## Équilibrage AVL

L'arbre maintient un facteur d'équilibre pour chaque nœud :
- **Balance = hauteur(droite) - hauteur(gauche)**
- Balance acceptable : -1, 0 ou 1
- Si |balance| > 1 : rotation nécessaire

## Tests

Le programme `test-tree-avl` teste :
- Insertion de plusieurs valeurs (entiers et chaînes)
- Affichage des parcours
- Recherche d'éléments
- Suppression et rééquilibrage
- Visualisation de la structure
