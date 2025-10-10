#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "tree-avl.h"

// Fonction de comparaison pour des entiers
int compare_int(const void *a, const void *b) {
    return (*(int *)a - *(int *)b);
}

// Affichage d’un nœud )
void print_noeud(void *a, void *b) {
    if (!a) return;
    Tree node = (Tree)a;
    int val = *(int *)node->data;
    printf("Valeur du nœud : %-3d | Balance : %d\n", val, node->balance);
}

// Affichage visuel de l’arbre (indentation = profondeur)
void print_tree(Tree node, int level) {
    if (!node) return;
    print_tree(node->right, level + 1);

    // indentation pour mieux visualiser la hiérarchie
    for (int i = 0; i < level; i++) printf("    ");
    printf("%d (bal=%d)\n", *(int *)node->data, node->balance);

    print_tree(node->left, level + 1);
}

void testArbreAvl(void) {
    int valeur_noeuds[] = {2, 4, 6, 8, 10, 12};
    Tree racine = NULL;

    // Insertion des valeurs dans l'arbre AVL
    for (int i = 0; i < 6; i++) {
        tree_insert_avl(&racine, &valeur_noeuds[i], sizeof(int), compare_int);
    }

    printf("Arbre après insertion (PostFixe): \n");
    tree_post_order(racine, print_noeud, NULL);

    printf("\nStructure de l'arbre: \n");
    print_tree(racine, 0);

    // Suppression d’une valeur
    int val_to_delete = 6;
    racine = tree_delete_avl(racine, &val_to_delete, compare_int, NULL);

    // Affichage après suppression
    printf("\nArbre après suppression de %d (PostFixe): \n", val_to_delete);
    tree_post_order(racine, print_noeud, NULL);

    printf("\nStructure de l'arbre après suppression: \n");
    print_tree(racine, 0);

    tree_insert_avl(&racine, &valeur_noeuds[2], sizeof(int), compare_int); // Réinsertion de 6
    printf("\nArbre après réinsertion de %d (PostFixe): \n", valeur_noeuds[2]);
    tree_post_order(racine, print_noeud, NULL);

    int val_to_search = 10;
    Tree found = tree_search_avl(racine, &val_to_search, compare_int);
    if (found) {
        printf("\nValeur %d trouvée dans l'arbre.\n", val_to_search);
    } else {
        printf("\nValeur %d non trouvée dans l'arbre.\n", val_to_search);
    }

    int val_not_found = 7;
    found = tree_search_avl(racine, &val_not_found, compare_int);
    if (found) {
        printf("\nValeur %d trouvée dans l'arbre.\n", val_not_found);
    } else {
        printf("\nValeur %d non trouvée dans l'arbre.\n", val_not_found);
    }
    // Libération mémoire
    tree_delete(racine, NULL);
}

int main(void) {
    testArbreAvl();
    return EXIT_SUCCESS;
}
