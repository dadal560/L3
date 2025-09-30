#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include "tree-avl.h"

int compare_int(const void *a, const void *b) {
    return (*(int *)a - *(int *)b);
}

void print_noeud(void *a, void *b) {
    if (!a) return;
    Tree node = (Tree)a;
    int val = *(int *)node->data;
    printf("Valeur du nœud : %d, valeur de la Balance : %d\n", val, node->balance);
}

void testArbreAvl(void){
    int valeur_noeuds[] = {2, 4, 6, 8, 10, 12};
    Tree racine = NULL;

    // Insertion des valeurs dans l'arbre AVL
    for (int i = 0; i < 6; i++) {
        tree_insert_avl(&racine, &valeur_noeuds[i], sizeof(int), compare_int);
    }


    // Affichage des parcours après les insertions
    printf("l'arbre après insertion :\n");
    printf("Tri pre-order :\n");
    tree_pre_order(racine, print_noeud, NULL);

    printf("Tri in-order :\n");
    tree_in_order(racine, print_noeud, NULL);
    printf("Tri post-order :\n");
    tree_post_order(racine, print_noeud, NULL);

    // Suppression d'une valeur
    int val_to_delete = 6;
    racine = tree_delete_avl(racine, &val_to_delete, compare_int, NULL);
    printf("l'arbre après suppression de %d :\n", val_to_delete);
    printf("Tri pre-order :\n");
    tree_pre_order(racine, print_noeud, NULL);
    printf("Tri post-order :\n");
    tree_post_order(racine, print_noeud, NULL);
    printf("Tri in-order :\n");
    tree_in_order(racine, print_noeud, NULL);
    // Libération de la mémoire
    tree_delete(racine, NULL);
}



int main(){

    testArbreAvl();
    return EXIT_SUCCESS;
}
