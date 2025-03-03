#include <functional>

template <typename Func>
void do_for_each(Func f) {}

template <typename Func, typename T, typename... Args>
void do_for_each(Func f, T& first, Args&... rest) {
    f(first);
    do_for_each(f, rest...);
}


template <typename T>
void print(T thing) {
    std::cout << thing << std::endl;
}
template <typename T, typename... Args>
void print(T first, Args... rest) {
    std::cout << first << " ";
    print(rest...);
}
