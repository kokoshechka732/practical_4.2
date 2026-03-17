#ifndef DEQUE_CPP_H
#define DEQUE_CPP_H

#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

typedef struct Node {
    int num;
    char text[10];
    struct Node* next;
} Node;

typedef struct Deque {
    Node* head;
    Node* tail;
    int size;
} Deque;

#ifdef __cplusplus
extern "C" {
#endif

    EXPORT Deque* deque_create();
    EXPORT void deque_destroy(Deque* d);
    EXPORT void deque_push_front(Deque* d, int num, const char* text);
    EXPORT void deque_push_back(Deque* d, int num, const char* text);
    EXPORT int deque_pop_front(Deque* d);
    EXPORT int deque_pop_back(Deque* d);
    EXPORT int deque_get_size(Deque* d);
    EXPORT int deque_is_empty(Deque* d);
    EXPORT char* deque_to_string(Deque* d);
    EXPORT void deque_free_string(char* str);
    EXPORT void deque_clear(Deque* d);

#ifdef __cplusplus
}
#endif

#endif