# Bibliothèque d'Arbres AVL en C

Une implémentation complète et optimisée d'arbres AVL (Adelson-Velsky et Landis) auto-équilibrés en C pur, avec gestion générique des données et mécanismes de rééquilibrage automatique.

## Installation et Configuration

### Prérequis

![C](https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white) ![CMake](https://img.shields.io/badge/CMake-064F8C?style=for-the-badge&logo=cmake&logoColor=white)

- GCC ou Clang
- CMake 3.0+
- Make

### Installation

1. **Clonez le dépôt**
```bash
git clone <votre-repo>
cd tree-avl
```

2. **Compilation**
```bash
mkdir build && cd build
cmake ..
make
```

3. **Exécution des tests**
```bash
make test
# ou directement
./test-tree-avl
```

4. **Installation système (optionnel)**
```bash
sudo make install
```

### Fichiers installés

```
/usr/local/lib/libtree-avl.so          # Bibliothèque partagée
/usr/local/include/tree-avl.h          # En-têtes publiques
/usr/local/share/pkgconfig/tree-avl.pc # Configuration pkg-config
/usr/local/cmake/TreeConfig.cmake      # Configuration CMake
```

## Utilisation

### Exemple basique

```c
#include <stdio.h>
#include <stdlib.h>
#include "tree-avl.h"

// Fonction de comparaison pour entiers
int compare_int(const void *a, const void *b) {
    return (*(int*)a - *(int*)b);
}

// Fonction d'affichage
void print_node(void *node_ptr, void *extra) {
    Tree node = (Tree)node_ptr;
    int value = *(int*)node->data;
    printf("Valeur: %d | Balance: %d\n", value, node->balance);
}

int main() {
    Tree root = NULL;
    int values[] = {50, 25, 75, 10, 30, 60, 80};
    
    // 🌱 Insertion
    printf("=== INSERTION ===\n");
    for (int i = 0; i < 7; i++) {
        tree_insert_avl(&root, &values[i], sizeof(int), compare_int);
        printf("Inséré: %d\n", values[i]);
    }
    
    // 📊 Parcours infixe (ordre croissant)
    printf("\n=== PARCOURS INFIXE ===\n");
    tree_in_order(root, print_node, NULL);
    
    // 📏 Statistiques
    printf("\n=== STATISTIQUES ===\n");
    printf("Hauteur: %zu\n", tree_height(root));
    printf("Taille: %zu nœuds\n", tree_size(root));
    
    // 🔍 Recherche
    int search_value = 30;
    void *found = tree_search(root, &search_value, compare_int);
    printf("\n=== RECHERCHE ===\n");
    printf("Valeur %d : %s\n", search_value, 
           found ? "trouvée ✓" : "non trouvée ✗");
    
    // 🗑️ Suppression
    printf("\n=== SUPPRESSION ===\n");
    int delete_value = 25;
    root = tree_delete_avl(root, &delete_value, compare_int, NULL);
    printf("Supprimé: %d\n", delete_value);
    
    printf("\nAprès suppression:\n");
    tree_in_order(root, print_node, NULL);
    
    // 🧹 Nettoyage
    tree_delete(root, NULL);
    
    return EXIT_SUCCESS;
}
```

### Compilation avec la bibliothèque

**Avec pkg-config (recommandé)**
```bash
gcc main.c $(pkg-config --cflags --libs tree-avl) -o main
```

**Manuelle**
```bash
gcc main.c -I/usr/local/include -L/usr/local/lib -ltree-avl -o main
```

**Avec CMake**
```cmake
find_package(Tree-avl REQUIRED)
target_link_libraries(mon_programme tree-avl)
```

### Structure du projet

```
tree-avl/
├── tree-avl.h              # En-têtes publiques
├── tree-avl.c              # Implémentation
├── test-tree-avl.c         # Suite de tests
├── min-max.h               # Macros MIN/MAX
├── CMakeLists.txt          # Configuration CMake
├── tree-avl.pc.in          # Template pkg-config
├── TreeConfig.cmake.in     # Template config CMake
└── README.md               # Documentation
```

## Architecture et Fonctionnalités

### Qu'est-ce qu'un arbre AVL ?

Un **arbre AVL** est un arbre binaire de recherche qui maintient automatiquement son équilibre. Pour chaque nœud, la différence de hauteur entre ses sous-arbres gauche et droit (appelée **facteur d'équilibre**) ne dépasse jamais 1.

**Avantages** :
- ✅ Complexité garantie O(log n) pour insertion/suppression/recherche
- ✅ Équilibrage automatique via rotations
- ✅ Performance prévisible même dans le pire cas

### Fonctionnalités principales

**Opérations AVL**
- ✅ Insertion avec rééquilibrage automatique
- ✅ Suppression préservant l'équilibre
- ✅ Recherche optimisée
- ✅ Support de types génériques via `void*`

**Parcours d'arbre**
- ✅ Préfixe (pré-order)
- ✅ Infixe (in-order) - tri croissant
- ✅ Postfixe (post-order)

**Mécanismes d'équilibrage**
- ✅ Rotation simple gauche (RR)
- ✅ Rotation simple droite (LL)
- ✅ Rotation double gauche-droite (LR)
- ✅ Rotation double droite-gauche (RL)

**Utilitaires**
- ✅ Calcul de hauteur
- ✅ Calcul de taille
- ✅ Navigation parent/enfant
- ✅ Tri de tableaux

### Structure de données

```c
struct _TreeNode {
    Tree left;      // Sous-arbre gauche
    Tree right;     // Sous-arbre droit
    Tree parent;    // Pointeur vers le parent
    int balance;    // Facteur d'équilibre (-1, 0, +1)
    char data[1];   // Données flexibles (struct hack)
};
```

Le **facteur d'équilibre** est calculé comme :
```
balance = hauteur(sous-arbre droit) - hauteur(sous-arbre gauche)
```

- `balance = -1` : Penché à gauche (OK)
- `balance = 0` : Parfaitement équilibré (OK)
- `balance = +1` : Penché à droite (OK)
- `|balance| > 1` : **DÉSÉQUILIBRÉ** → Rotation nécessaire

## API Complète

### Création et destruction

#### `Tree tree_new()`
Crée un nouvel arbre vide.
```c
Tree root = tree_new(); // Retourne NULL
```

#### `Tree tree_create(const void *data, size_t size)`
Crée un nouveau nœud avec les données fournies.
```c
int value = 42;
Tree node = tree_create(&value, sizeof(int));
```

#### `void tree_delete(Tree tree, void (*delete)(void*))`
Supprime récursivement tout l'arbre et libère la mémoire.
```c
tree_delete(root, NULL); // NULL si pas de libération personnalisée
```

### Opérations AVL

#### `bool tree_insert_avl(Tree *ptree, const void *data, int size, int (*compare)(...))`
Insère un élément dans l'arbre AVL avec rééquilibrage automatique.

**Paramètres** :
- `ptree` : Pointeur vers la racine
- `data` : Données à insérer
- `size` : Taille des données en octets
- `compare` : Fonction de comparaison retournant -1, 0, ou 1

**Retour** : `true` si succès, `false` en cas d'erreur d'allocation

```c
int value = 50;
tree_insert_avl(&root, &value, sizeof(int), compare_int);
```

#### `Tree tree_delete_avl(Tree root, const void *data, int (*compare)(...), void (*delete)(void*))`
Supprime un élément de l'arbre AVL avec rééquilibrage.

**Cas gérés** :
- Nœud sans enfant → Suppression simple
- Nœud avec un enfant → Remplacement par l'enfant
- Nœud avec deux enfants → Remplacement par le successeur in-order

```c
int value = 25;
root = tree_delete_avl(root, &value, compare_int, NULL);
```

#### `void *tree_search(Tree tree, const void *data, int (*compare)(...))`
Recherche un élément dans l'arbre.

**Retour** : Pointeur vers les données ou `NULL` si non trouvé

```c
int search = 30;
void *found = tree_search(root, &search, compare_int);
if (found) {
    printf("Trouvé: %d\n", *(int*)found);
}
```

### Fonctions d'équilibrage

#### `void tree_update_balance(Tree node)`
Met à jour le facteur d'équilibre d'un nœud basé sur les hauteurs de ses sous-arbres.

#### `Tree tree_balance(Tree node)`
Équilibre un nœud en effectuant les rotations nécessaires.

**Décisions de rotation** :
```c
if (balance > 1) {         // Déséquilibre à droite
    if (right->balance < 0) // Cas RL
        rotate_right(right);
    return rotate_left(root); // Cas RR ou RL corrigé
}
if (balance < -1) {        // Déséquilibre à gauche
    if (left->balance > 0)  // Cas LR
        rotate_left(left);
    return rotate_right(root); // Cas LL ou LR corrigé
}
```

#### `Tree rotate_left(Tree root)`
Effectue une rotation gauche (cas RR).

```
    A                B
     \              / \
      B     =>     A   C
       \
        C
```

#### `Tree rotate_right(Tree root)`
Effectue une rotation droite (cas LL).

```
      C            B
     /            / \
    B      =>    A   C
   /
  A
```

### Parcours d'arbre

#### `void tree_pre_order(Tree tree, void (*func)(void*, void*), void *extra_data)`
Parcours préfixe : **Nœud → Gauche → Droite**

```c
tree_pre_order(root, print_node, NULL);
```

#### `void tree_in_order(Tree tree, void (*func)(void*, void*), void *extra_data)`
Parcours infixe : **Gauche → Nœud → Droite** (ordre croissant pour ABR)

```c
tree_in_order(root, print_node, NULL);
```

#### `void tree_post_order(Tree tree, void (*func)(void*, void*), void *extra_data)`
Parcours postfixe : **Gauche → Droite → Nœud**

```c
tree_post_order(root, print_node, NULL);
```

### Accesseurs

#### `Tree tree_get_left(Tree tree)`
Retourne le sous-arbre gauche.

#### `Tree tree_get_right(Tree tree)`
Retourne le sous-arbre droit.

#### `void *tree_get_data(Tree tree)`
Retourne un pointeur vers les données du nœud.

#### `bool tree_set_left(Tree tree, Tree left)`
Définit le sous-arbre gauche.

#### `bool tree_set_right(Tree tree, Tree right)`
Définit le sous-arbre droit.

#### `bool tree_set_data(Tree tree, const void *data, size_t size)`
Copie de nouvelles données dans le nœud.

### Utilitaires

#### `size_t tree_height(Tree tree)`
Calcule la hauteur de l'arbre.

**Hauteur** : Longueur du plus long chemin de la racine à une feuille

```c
printf("Hauteur: %zu\n", tree_height(root));
```

#### `size_t tree_size(Tree tree)`
Calcule le nombre total de nœuds dans l'arbre.

```c
printf("Nombre de nœuds: %zu\n", tree_size(root));
```

#### `int tree_sort(void *array, size_t length, size_t size, int (*compare)(...))`
Trie un tableau en utilisant un arbre AVL.

**Algorithme** :
1. Insère tous les éléments dans un AVL
2. Parcours infixe pour récupérer les éléments triés
3. Libère l'arbre

**Complexité** : O(n log n)

```c
int numbers[] = {5, 2, 8, 1, 9, 3};
tree_sort(numbers, 6, sizeof(int), compare_int);
// numbers est maintenant trié: {1, 2, 3, 5, 8, 9}
```

## Exemples avancés

### Exemple avec structures personnalisées

```c
#include <string.h>
#include "tree-avl.h"

typedef struct {
    int id;
    char name[50];
    float score;
} Student;

int compare_students(const void *a, const void *b) {
    Student *s1 = (Student*)a;
    Student *s2 = (Student*)b;
    return s1->id - s2->id;
}

void print_student(void *node_ptr, void *extra) {
    Tree node = (Tree)node_ptr;
    Student *student = (Student*)node->data;
    printf("ID: %d | Nom: %s | Score: %.2f\n", 
           student->id, student->name, student->score);
}

void free_student(void *data) {
    // Libération personnalisée si nécessaire
    // Pour cet exemple, rien à faire
}

int main() {
    Tree students = NULL;
    
    Student s1 = {101, "Alice", 95.5};
    Student s2 = {103, "Bob", 87.0};
    Student s3 = {102, "Charlie", 92.3};
    
    tree_insert_avl(&students, &s1, sizeof(Student), compare_students);
    tree_insert_avl(&students, &s2, sizeof(Student), compare_students);
    tree_insert_avl(&students, &s3, sizeof(Student), compare_students);
    
    printf("Étudiants triés par ID:\n");
    tree_in_order(students, print_student, NULL);
    
    tree_delete(students, free_student);
    return 0;
}
```

### Exemple avec comptage de nœuds

```c
void count_nodes(void *node_ptr, void *counter) {
    (*(int*)counter)++;
}

int main() {
    Tree root = NULL;
    // ... insertions ...
    
    int count = 0;
    tree_in_order(root, count_nodes, &count);
    printf("Nombre de nœuds: %d\n", count);
    
    return 0;
}
```

### Exemple de recherche et modification

```c
int main() {
    Tree root = NULL;
    int values[] = {10, 20, 30, 40, 50};
    
    for (int i = 0; i < 5; i++) {
        tree_insert_avl(&root, &values[i], sizeof(int), compare_int);
    }
    
    // Recherche
    int search = 30;
    int *found = (int*)tree_search(root, &search, compare_int);
    
    if (found) {
        printf("Trouvé: %d\n", *found);
        
        // Modification (attention: ne doit pas changer l'ordre)
        // Pour changer la clé, il faut supprimer puis réinsérer
        root = tree_delete_avl(root, &search, compare_int, NULL);
        int new_value = 35;
        tree_insert_avl(&root, &new_value, sizeof(int), compare_int);
    }
    
    tree_delete(root, NULL);
    return 0;
}
```

## Mécanismes d'équilibrage expliqués

### Types de déséquilibres et rotations

| Cas | Condition | Rotation | Description |
|-----|-----------|----------|-------------|
| **LL** | `balance < -1` et `left->balance ≤ 0` | Simple droite | Sous-arbre gauche du fils gauche trop lourd |
| **RR** | `balance > +1` et `right->balance ≥ 0` | Simple gauche | Sous-arbre droit du fils droit trop lourd |
| **LR** | `balance < -1` et `left->balance > 0` | Gauche puis droite | Sous-arbre droit du fils gauche trop lourd |
| **RL** | `balance > +1` et `right->balance < 0` | Droite puis gauche | Sous-arbre gauche du fils droit trop lourd |

### Exemple de rotation simple gauche (RR)

**Avant** (déséquilibre à droite) :
```
    10 (balance = +2)
      \
       20 (balance = +1)
         \
          30
```

**Après** rotation gauche sur 10 :
```
       20 (balance = 0)
      /  \
    10    30
```

### Exemple de rotation double gauche-droite (LR)

**Avant** (déséquilibre mixte) :
```
      30 (balance = -2)
     /
   10 (balance = +1)
     \
      20
```

**Étape 1** : Rotation gauche sur 10
```
      30
     /
   20
   /
 10
```

**Étape 2** : Rotation droite sur 30
```
       20
      /  \
    10    30
```

## Complexité algorithmique

| Opération | Complexité moyenne | Complexité pire cas |
|-----------|-------------------|---------------------|
| **Insertion** | O(log n) | O(log n) |
| **Suppression** | O(log n) | O(log n) |
| **Recherche** | O(log n) | O(log n) |
| **Parcours** | O(n) | O(n) |
| **Hauteur** | O(n) | O(n) |
| **Taille** | O(n) | O(n) |

**Note** : Contrairement aux ABR classiques, les arbres AVL garantissent O(log n) même dans le pire cas grâce à l'équilibrage.

## Tests et validation

### Suite de tests

Le fichier `test-tree-avl.c` teste :

1. ✅ **Insertion** : Séquence {2, 4, 6, 8, 10, 12}
2. ✅ **Équilibrage** : Vérification des balances après insertion
3. ✅ **Parcours** : Pre-order, in-order, post-order
4. ✅ **Suppression** : Suppression de la valeur 6
5. ✅ **Rééquilibrage** : Vérification après suppression
6. ✅ **Libération** : Pas de fuites mémoire

### Exécution des tests

```bash
# Compilation et tests
cd build
make test

# Exécution directe avec sortie détaillée
./test-tree-avl
```

### Sortie attendue

```
l'arbre après insertion :
Tri pre-order :
Valeur du nœud : 8, valeur de la Balance : 0
Valeur du nœud : 4, valeur de la Balance : 0
Valeur du nœud : 2, valeur de la Balance : 0
Valeur du nœud : 6, valeur de la Balance : 0
Valeur du nœud : 10, valeur de la Balance : 0
Valeur du nœud : 12, valeur de la Balance : 0

Tri in-order :
Valeur du nœud : 2, valeur de la Balance : 0
Valeur du nœud : 4, valeur de la Balance : 0
Valeur du nœud : 6, valeur de la Balance : 0
Valeur du nœud : 8, valeur de la Balance : 0
Valeur du nœud : 10, valeur de la Balance : 0
Valeur du nœud : 12, valeur de la Balance : 0

l'arbre après suppression de 6 :
[... affichage similaire ...]
```

### Tests avec Valgrind (détection de fuites mémoire)

```bash
valgrind --leak-check=full --show-leak-kinds=all ./test-tree-avl
```

## Personnalisation

### Modification de la fonction de comparaison

Pour des types personnalisés :

```c
// Pour des chaînes de caractères
int compare_strings(const void *a, const void *b) {
    return strcmp((const char*)a, (const char*)b);
}

// Pour des structures complexes (tri multi-critères)
int compare_multi(const void *a, const void *b) {
    MyStruct *s1 = (MyStruct*)a;
    MyStruct *s2 = (MyStruct*)b;
    
    // Tri primaire par ID
    if (s1->id != s2->id)
        return s1->id - s2->id;
    
    // Tri secondaire par nom si IDs égaux
    return strcmp(s1->name, s2->name);
}
```

### Ajout de statistiques personnalisées

```c
typedef struct {
    int min;
    int max;
    long sum;
    int count;
} Stats;

void compute_stats(void *node_ptr, void *data) {
    Tree node = (Tree)node_ptr;
    Stats *stats = (Stats*)data;
    int value = *(int*)node->data;
    
    if (stats->count == 0) {
        stats->min = stats->max = value;
    } else {
        if (value < stats->min) stats->min = value;
        if (value > stats->max) stats->max = value;
    }
    stats->sum += value;
    stats->count++;
}

int main() {
    Tree root = NULL;
    // ... insertions ...
    
    Stats stats = {0, 0, 0, 0};
    tree_in_order(root, compute_stats, &stats);
    
    printf("Min: %d\n", stats.min);
    printf("Max: %d\n", stats.max);
    printf("Moyenne: %.2f\n", (double)stats.sum / stats.count);
    
    return 0;
}
```

## Dépannage

### Problèmes courants

**Erreur de compilation "undefined reference to tree_xxx"**
- Vérifiez que vous liez bien avec `-ltree-avl`
- Assurez-vous que la bibliothèque est installée : `sudo make install`
- Vérifiez le `LD_LIBRARY_PATH` si installation locale

```bash
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
```

**Erreur "tree-avl.h: No such file or directory"**
- Ajoutez le chemin des headers : `-I/usr/local/include`
- Ou utilisez pkg-config : `$(pkg-config --cflags tree-avl)`

**Segmentation fault lors de l'insertion**
- Vérifiez que vous passez un **pointeur** vers la racine : `&root`
- Assurez-vous que la fonction de comparaison est correcte
- Vérifiez que `size` correspond bien à la taille des données

**Balance incorrecte après opérations**
- C'est normal si vous modifiez manuellement l'arbre sans passer par les fonctions AVL
- Utilisez toujours `tree_insert_avl` et `tree_delete_avl`, pas les fonctions BSR classiques

**Fuites mémoire**
- Appelez toujours `tree_delete(root, NULL)` à la fin
- Si vos données contiennent des pointeurs, fournissez une fonction `delete` personnalisée

```c
void free_complex_data(void *data) {
    MyStruct *s = (MyStruct*)data;
    free(s->dynamic_field);
    // Ne pas free(s) car c'est fait par tree_delete
}

tree_delete(root, free_complex_data);
```

### Débogage avec GDB

```bash
# Compilation avec symboles de débogage
gcc -g main.c -ltree-avl -o main

# Lancement GDB
gdb ./main

# Commandes utiles GDB
(gdb) break tree_insert_avl
(gdb) run
(gdb) print *ptree
(gdb) print (*ptree)->balance
(gdb) backtrace
```

## Limitations connues

- ⚠️ **Taille des données** : La copie dans `tree_delete_avl` utilise `sizeof(root->data)` qui est toujours 1. Envisager de stocker la taille réelle dans la structure.
  
  **Solution temporaire** : Utiliser une taille fixe connue ou passer la taille en paramètre.

- ⚠️ **Thread-safety** : La bibliothèque n'est pas thread-safe. Pour un usage multi-thread :
  ```c
  pthread_mutex_t tree_mutex = PTHREAD_MUTEX_INITIALIZER;
  
  pthread_mutex_lock(&tree_mutex);
  tree_insert_avl(&root, data, size, compare);
  pthread_mutex_unlock(&tree_mutex);
  ```

- ⚠️ **Doublons** : Les valeurs égales sont insérées à droite par défaut (`cmp > 0`). Pour interdire les doublons, modifier `tree_insert_avl` :
  ```c
  if (cmp == 0) return false; // Rejeter les doublons
  ```

- ⚠️ **Mémoire** : L'allocation utilise le "struct hack" pour les données flexibles. Certains compilateurs stricts peuvent générer des warnings.

## Contexte académique

Ce projet a été réalisé dans le cadre du cours **"Structures de données - avancé"** (Semestre 5) pour approfondir la compréhension des arbres binaires de recherche auto-équilibrés.

### Objectifs pédagogiques

- 🎯 Comprendre les limitations des ABR classiques
- 🎯 Implémenter les rotations AVL (simples et doubles)
- 🎯 Maîtriser la récursivité en C
- 🎯 Gérer la mémoire dynamique et les pointeurs
- 🎯 Utiliser CMake pour créer une bibliothèque réutilisable
- 🎯 Écrire des tests unitaires

### Concepts abordés

- Arbres binaires de recherche (ABR)
- Facteur d'équilibre et hauteur
- Rotations simples et doubles
- Complexité algorithmique garantie
- Gestion générique avec `void*`
- Bibliothèques partagées en C

## Support

Pour toute question ou problème :

- 📧 Email : votre.email@example.com
- 🐛 Issues : [GitHub Issues](lien-vers-issues)
- 📚 Documentation : Ce README

## Ressources complémentaires

- 📖 [Wikipedia - Arbre AVL](https://fr.wikipedia.org/wiki/Arbre_AVL)
- 📖 [Visualisation interactive](https://www.cs.usfca.edu/~galles/visualization/AVLtree.html)
- 📖 [CMake Documentation](https://cmake.org/documentation/)
- 📖 Introduction to Algorithms (CLRS) - Chapitre sur les arbres AVL

---

⭐ **N'oubliez pas de star le projet s'il vous a été utile !**