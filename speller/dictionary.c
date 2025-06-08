#include "dictionary.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

const unsigned int N = 10000;
node *table[N];
unsigned int word_count = 0;

unsigned int hash(const char *word)
{
    unsigned long hash = 5381;
    int c;
    while ((c = *word++))
    {
        hash = ((hash << 5) + hash) + tolower(c);
    }
    return hash % N;
}

bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    char word[LENGTH + 1];
    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            fclose(file);
            return false;
        }

        strcpy(n->word, word);

        unsigned int index = hash(word);
        n->next = table[index];
        table[index] = n;
        word_count++;
    }

    fclose(file);
    return true;
}

bool check(const char *word)
{
    char lower[LENGTH + 1];
    int len = strlen(word);
    for (int i = 0; i < len; i++)
    {
        lower[i] = tolower(word[i]);
    }
    lower[len] = '\0';

    unsigned int index = hash(lower);
    node *cursor = table[index];
    while (cursor != NULL)
    {
        if (strcmp(cursor->word, lower) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

unsigned int size(void)
{
    return word_count;
}

bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
