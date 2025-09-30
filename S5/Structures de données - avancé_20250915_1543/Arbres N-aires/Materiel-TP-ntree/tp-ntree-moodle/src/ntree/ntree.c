
#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include <assert.h>

#include <unistd.h>

#include "ntree.h"

#include "min-max.h"
//----------------------------------------
NTree ntree_new () {
    return NULL;
}

//----------------------------------------


NTree ntree_create (const void *data, size_t size, size_t arity) {
    NTree tree = (NTree) malloc (sizeof (NTree *) + sizeof (size_t) + size);
    if (tree) {
        tree->subtrees = (NTree *) malloc (arity * sizeof(NTree));
        if (tree->subtrees) {
            size_t i;

            for (i = 0; i < arity; i++)
                tree->subtrees[i] = NULL;
            tree->arity = arity;
            memcpy(tree->data, data, size);
        }
        else {
            free(tree);
            return 0;
        }
    }
    else
    {
        free(tree);
        tree = NULL;
    }

    return tree;
}
//----------------------------------------


void ntree_delete (NTree tree, void (*deletef) (void *)) {
    if (tree) {
        size_t i;

        for (i = 0; i < tree->arity; i++)
            ntree_delete(tree->subtrees[i], deletef);
        if (deletef)
            deletef(tree->data);
        
        free(tree->subtrees);
        free(tree);
    }
}


//----------------------------------------


void *ntree_get_data(NTree tree) {
    assert(tree);
    return tree->data;
}
//----------------------------------------


bool ntree_set_nth(NTree tree, NTree sub, size_t nth, void (*deletef) (void *)) {
 if (!tree) {
        return false; 
    }

    if (nth >= tree->arity) {
        NTree *new_subtrees = realloc(tree->subtrees, (nth + 1) * sizeof(NTree));
        if (!new_subtrees) {
            return false; 
        }
        
        for (size_t i = tree->arity; i <= nth; i++) {
            new_subtrees[i] = NULL;
        }

        tree->subtrees = new_subtrees;
        tree->arity = nth + 1;
    }

    if (tree->subtrees[nth]) {
        if (deletef) {
            ntree_delete(tree->subtrees[nth], deletef);
        }
    }

    tree->subtrees[nth] = sub; 
    return true; 
}

//----------------------------------------



bool ntree_set_data(NTree tree, const void *data, size_t size) {
    if(tree) {
        memcpy(tree->data, data, size);
        return true;
    }
    else
        return false;
}
//----------------------------------------

// profondeur maximale
size_t ntree_height(NTree tree) {
    if(tree) {
        size_t max_height = 0;
        for(size_t i = 0; i < tree->arity; i++) {
            max_height = MAX(max_height, ntree_height(tree->subtrees[i]));
        }
        return max_height + 1;
    }
    else
        return false;
}
//----------------------------------------

// nombres d'élements
size_t ntree_size(NTree tree) {
    if(tree){
        size_t size = 1;
        for(size_t i = 0; i < tree->arity; i++) {
            size += ntree_size(tree->subtrees[i]);
        }
        return size;
    }
    else
        return false;
}


//----------------------------------------

void ntree_pre_order(NTree tree, void (*func)(void *, void *), void *extra_data) {
    if (tree) {
        func(tree->data, extra_data);
        for (size_t i = 0; i < tree->arity; i++) {
            ntree_pre_order(tree->subtrees[i], func, extra_data);
        }
    }
}


//----------------------------------------

void ntree_post_order(NTree tree, void (*func)(void *, void *), void *extra_data) {
    if (tree) {
        for (size_t i = 0; i < tree->arity; i++) {
            ntree_post_order(tree->subtrees[i], func, extra_data);
        }
        func(tree->data, extra_data); 
    }
}



//----------------------------------------

void ntree_in_order(NTree tree, void (*func)(void *, void *), void *extra_data, size_t nth) {
    if (tree) {
        for (size_t i = 0; i < nth && i < tree->arity; i++) {
            ntree_in_order(tree->subtrees[i], func, extra_data, nth);
        }
        func(tree->data, extra_data); 
        for (size_t i = nth; i < tree->arity; i++) {
            ntree_in_order(tree->subtrees[i], func, extra_data, nth); 
        }
    }
}

//----------------------------------------

