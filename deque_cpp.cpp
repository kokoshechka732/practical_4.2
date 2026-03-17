#include "deque_cpp.h"
#include <cstdlib>
#include <cstring>
#include <cstdio>

EXPORT Deque* deque_create() {
    Deque* d = (Deque*)malloc(sizeof(Deque));
    if (d == NULL) return NULL;
    memset(d, 0, sizeof(Deque));
    d->head = NULL;
    d->tail = NULL;
    d->size = 0;
    return d;
}

EXPORT void deque_destroy(Deque* d) {
    if (d == NULL) return;
    Node* cur = d->head;
    while (cur != NULL) {
        Node* temp = cur;
        cur = cur->next;
        free(temp);
    }
    free(d);
}

EXPORT void deque_push_front(Deque* d, int num, const char* text) {
    if (d == NULL) return;
    Node* n = (Node*)malloc(sizeof(Node));
    if (n == NULL) return;
    memset(n, 0, sizeof(Node));
    n->num = num;
    strncpy(n->text, text, 9);
    n->text[9] = '\0';
    n->next = d->head;
    d->head = n;
    if (d->tail == NULL) {
        d->tail = n;
    }
    d->size++;
}

EXPORT void deque_push_back(Deque* d, int num, const char* text) {
    if (d == NULL) return;
    Node* n = (Node*)malloc(sizeof(Node));
    if (n == NULL) return;
    memset(n, 0, sizeof(Node));
    n->num = num;
    strncpy(n->text, text, 9);
    n->text[9] = '\0';
    n->next = NULL;
    if (d->tail != NULL) {
        d->tail->next = n;
        d->tail = n;
    }
    else {
        d->head = d->tail = n;
    }
    d->size++;
}

EXPORT int deque_pop_front(Deque* d) {
    if (d == NULL || d->head == NULL) return 0;
    Node* temp = d->head;
    d->head = d->head->next;
    free(temp);
    if (d->head == NULL) {
        d->tail = NULL;
    }
    d->size--;
    return 1;
}

EXPORT int deque_pop_back(Deque* d) {
    if (d == NULL || d->head == NULL) return 0;
    if (d->head == d->tail) {
        free(d->head);
        d->head = d->tail = NULL;
        d->size--;
        return 1;
    }
    Node* cur = d->head;
    while (cur->next != d->tail) {
        cur = cur->next;
    }
    free(d->tail);
    d->tail = cur;
    d->tail->next = NULL;
    d->size--;
    return 1;
}

EXPORT int deque_get_size(Deque* d) {
    if (d == NULL) return 0;
    return d->size;
}

EXPORT int deque_is_empty(Deque* d) {
    if (d == NULL) return 1;
    return d->head == NULL ? 1 : 0;
}

EXPORT char* deque_to_string(Deque* d) {
    if (d == NULL || d->size == 0) {
        char* empty = (char*)malloc(1);
        if (empty) empty[0] = '\0';
        return empty;
    }
    char* buf = (char*)malloc(d->size * 100 + 1);
    if (buf == NULL) return NULL;
    buf[0] = '\0';
    char line[100];
    Node* cur = d->head;
    int index = 0;
    while (cur != NULL) {
        sprintf(line, "[%d] (%d, '%s')\n", index, cur->num, cur->text);
        strcat(buf, line);
        cur = cur->next;
        index++;
    }
    return buf;
}

EXPORT void deque_free_string(char* str) {
    if (str != NULL) {
        free(str);
    }
}

EXPORT void deque_clear(Deque* d) {
    if (d == NULL) return;
    while (d->head != NULL) {
        deque_pop_front(d);
    }
}