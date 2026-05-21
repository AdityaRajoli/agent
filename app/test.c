#include <stdio.h>

int find_max(int a, int b, int c) {
    if (a >= b && a >= c)
        return a;
    else if (b >= c)
        return b;
    else
        return c;
}

int main() {
    printf("%d\n", find_max(10, 5, 3));
    printf("%d\n", find_max(3, 9, 1));
    printf("%d\n", find_max(2, 4, 7));
    return 0;
}

