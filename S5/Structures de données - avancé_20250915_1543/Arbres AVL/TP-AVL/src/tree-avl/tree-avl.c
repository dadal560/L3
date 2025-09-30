

#include <string.h>
#include "tree-avl.h"
#include <stdbool.h>
#include "min-max.h"

/*--------------------------------------------------------------------*/
Tree
tree_new ()
{
  return NULL;
}

void tree_delete (Tree tree, void (*delete) (void *))
{
  if (tree)
    {
      tree_delete (tree->left, delete);
      tree_delete (tree->right, delete);
      if (delete)
        delete (tree->data);
      free (tree);
    }
}

Tree tree_create(const void *data, size_t size) {
    // Allocation mémoire pour le nœud et les données
    Tree tree = (Tree)malloc(sizeof(struct _TreeNode) - sizeof(char) + size);
    if (tree) {
        tree->left = NULL;  // Pas de sous-arbre gauche
        tree->right = NULL; // Pas de sous-arbre droit
        tree->parent = NULL; // Pas de parent
        tree->balance = 0;   // Balance initiale de 0
        memcpy(tree->data, data, size);  // Copie les données dans le nœud
    }
    return tree;
}

Tree
tree_get_left (Tree tree)
{
  if (tree)
    return tree->left;
  else
    return NULL;
}

Tree
tree_get_right (Tree tree)
{
  if (tree)
    return tree->right;
  else
    return NULL;
}

void *
tree_get_data (Tree tree)
{
  if (tree)
    return tree->data;
  else
    return NULL;
}

bool
tree_set_left (Tree tree, Tree left)
{
  if (tree)
    {
      tree->left = left;
      return true;
    }
  else
    return false;
}

bool
tree_set_right (Tree tree, Tree right)
{
  if (tree)
    {
      tree->right = right;
      return true;
    }
  else
    return false;
}

bool
tree_set_data (Tree tree, const void *data, size_t
size)
{
  if (tree)
    {
      memcpy (tree->data, data, size);
      return true;
    }
  else
    return false;
}

void
tree_pre_order (Tree tree,
                void (*func) (void *, void *),
                void *extra_data)
{
  if (tree)
    {
      func (tree, extra_data);
      tree_pre_order (tree->left, func, extra_data);
      tree_pre_order (tree->right, func, extra_data);
    }
}


void
tree_in_order (Tree tree,
               void (*func) (void *, void *),
               void *extra_data)
{
  if (tree)
    {
      tree_in_order (tree->left, func, extra_data);
      func (tree, extra_data);
      tree_in_order (tree->right, func, extra_data);
    }
}

void
tree_post_order (Tree tree,
                 void (*func) (void *, void *),
                 void *extra_data)
{
  if (tree)
    {
      tree_post_order (tree->left, func, extra_data);
      tree_post_order (tree->right, func, extra_data);
      func (tree, extra_data);
    }
}

size_t
tree_height (Tree tree)
{
  if (tree)
    return 1 + MAX (tree_height (tree->left),
tree_height (tree->right));
  else
    return 0;
}

size_t
tree_size (Tree tree)
{
  if (tree)
    return 1 + tree_size (tree->left) + tree_size
(tree->right);
  else
    return 0;
}

bool
tree_insert_sorted (Tree * ptree,
                    const void *data,
                    size_t size,
                    int (*compare) (const void *, const
void *))
{
  if (*ptree)
    {
      switch (compare (data, (*ptree)->data))
        {
        case -1:
          return tree_insert_sorted (&(*ptree)->left,
data, size, compare);
        default:
          return tree_insert_sorted (&(*ptree)->right,
data, size, compare);
        }
    }
  else
    {
      Tree new = tree_create (data, size);
      if (new)
        {
          *ptree = new;
          return true;
        }
      else
        return false;
    }

}

void *
tree_search (Tree tree,
             const void *data,
             int (*compare) (const void *, const void
*))
{
  if (tree)
    {
      switch (compare (data, tree->data))
        {
        case -1:
          return tree_search (tree->left, data, compare);
        case 0:
          return tree->data;
        case 1:
          return tree_search (tree->right, data, compare);
        default:
            return NULL; // RAJOUTE CAR WARNING !!!
        }
    }
  else
    return NULL;
}

static void
set (void *data,void *array)
{
  static size_t size;
  static size_t offset;

  if (data)
    {
      memcpy (array + offset, data, size);
      offset += size;
    }
  else
    {
      offset = 0;
      size = *(size_t *) array;
    }
}

int
tree_sort (void *array,
           size_t length,
           size_t size,
           int (*compare) (const void *, const void *))
{
  size_t i;
  Tree tree = tree_new ();
  void *pointer;

  pointer = array;
  for (i = 0; i < length; i++)
    {
      if (tree_insert_sorted (&tree, pointer, size,
compare))
        pointer += size;
      else
        {
          tree_delete (tree, NULL);
          return false;
        }
    }
  set (NULL, &size);
  tree_in_order (tree, set, array);
  tree_delete (tree, NULL);
  return true;
}

//Fonctions AVL

bool tree_insert_avl(Tree *ptree, const void *data, int size, int (*compare)(const void *, const void *)) {
    if (*ptree == NULL) {
        Tree new_node = tree_create(data, size);
        if (new_node == NULL) {
            return false;
        }
        *ptree = new_node;
        return true;
    }

    int cmp = compare(data, (*ptree)->data);
    if (cmp < 0) {
        if (!tree_insert_avl(&(*ptree)->left, data, size, compare)) {
            return false;
        }
        if ((*ptree)->left) (*ptree)->left->parent = *ptree;
    } else if (cmp > 0) {
        if (!tree_insert_avl(&(*ptree)->right, data, size, compare)) {
            return false;
        }
        if ((*ptree)->right) (*ptree)->right->parent = *ptree;
    }

    tree_update_balance(*ptree);
    *ptree = tree_balance(*ptree);

    return true;
}

Tree
tree_delete_avl(Tree root,
                  const void *data,
                  int (*compare) (const void *, const void *),
                  void (*delete) (void *))
{
    if (root == NULL) {
        return root; // Élément non trouvé
    }

    int cmp = compare(data, root->data);
    if (cmp < 0) {
        root->left = tree_delete_avl(root->left, data, compare, delete);
        if (root->left) root->left->parent = root;
    } else if (cmp > 0) {
        root->right = tree_delete_avl(root->right, data, compare, delete);
        if (root->right) root->right->parent = root;
    } else {
        // Nœud trouvé
        if (delete) {
            delete(root->data);
        }

        if (root->left == NULL || root->right == NULL) {
            Tree temp = root->left ? root->left : root->right;
            if (temp == NULL) {
                // Pas d'enfant
                free(root);
                return NULL;
            } else {
                // Un enfant
                temp->parent = root->parent;
                free(root);
                return temp;
            }
        } else {
            // Deux enfants : trouver le successeur inorder
            Tree successor = root->right;
            while (successor->left != NULL) {
                successor = successor->left;
            }
            memcpy(root->data, successor->data, sizeof(root->data)); // Copier les données du successeur
            root->right = tree_delete_avl(root->right, successor->data, compare, delete);
            if (root->right) root->right->parent = root;
        }
    }

    tree_update_balance(root);
    return tree_balance(root);
}


// Met à jour la balance d'un nœud après insertion/suppression
void tree_update_balance(Tree node) {
    if (node) {
        int left_height = node->left ? tree_height(node->left) : 0;
        int right_height = node->right ? tree_height(node->right) : 0;
        node->balance = right_height - left_height;  // Calcul de la balance
    }
}

// Équilibrer un nœud après insertion/suppression
Tree tree_balance(Tree root) {
    if (root->balance > 1) {  // Si la balance est supérieure à 1, rotation gauche nécessaire
        if (root->right && root->right->balance < 0) {  // Si le sous-arbre droit est déséquilibré vers la gauche
            root->right = rotate_right(root->right);  // Rotation droite du sous-arbre droit
        }
        return rotate_left(root);  // Rotation gauche
    } else if (root->balance < -1) {  // Si la balance est inférieure à -1, rotation droite nécessaire
        if (root->left && root->left->balance > 0) {  // Si le sous-arbre gauche est déséquilibré vers la droite
            root->left = rotate_left(root->left);  // Rotation gauche du sous-arbre gauche
        }
        return rotate_right(root);  // Rotation droite
    }
    return root;
}

// Rotation gauche autour d'un nœud
Tree rotate_left(Tree root) {
    if (!root || !root->right) {
        return root;
    }
    Tree new_root = root->right;
    root->right = new_root->left;

    if (new_root->left) {
        new_root->left->parent = root;
    }
    new_root->parent = root->parent;
    new_root->left = root;
    root->parent = new_root;

    tree_update_balance(root);
    tree_update_balance(new_root);

    return new_root;
}

// Rotation droite autour d'un nœud
Tree rotate_right(Tree root) {
    if (!root || !root->left) {
        return root;
    }
    Tree new_root = root->left;
    root->left = new_root->right;

    if (new_root->right) {
        new_root->right->parent = root;
    }
    new_root->parent = root->parent;
    new_root->right = root;
    root->parent = new_root;

    tree_update_balance(root);
    tree_update_balance(new_root);

    return new_root;
}