#include <iostream>
using namespace std;

int gcd(int a, int b) {
    while (b) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int modinv(int a, int n) {
    int x = 0, x1 = 1;
    int y = 1, y1 = 0;
    int b = n;
    while (b) {
        int quot = a / b;
        int temp = b;
        b = a % b;
        a = temp;
        temp = x;
        x = x1 - quot * x;
        x1 = temp;
        temp = y;
        y = y1 - quot * y;
        y1 = temp;
    }
    return (x1 % n + n) % n;
}

void inverse_pairs(int n) {
    cout << "Additive Inverse Pairs: ";
    for (int i = 0; i < n; i++) {
        cout << "(" << i << ", " << (-i + n) % n << ") ";
    }
    cout << endl;

    cout << "Multiplicative Inverse Pairs: ";
    for (int i = 1; i < n; i++) {
        if (gcd(i, n) == 1) {
            int x = modinv(i, n);
            cout << "(" << i << ", " << x << ") ";
        }
    }
    cout << endl;
}

int main() {
    inverse_pairs(10);
    return 0;
}
