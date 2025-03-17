template <typename T>
struct remove_pointers<T> {
    using type = T;
};
template <typename T>
struct remove_pointers<T*> {
    using type = T;
};

template <typename T>
remove_pointers<T>::type dereference(T x) {
    while (std::is_pointer(x)) {
        return dereference(*x);
    }
}

template <typename T>
class ls_set {
public:
    ls_set() {}
    void insert(T x) {
        if (!find(x)) {
            data.push_back(x);
        }
    }
    size_t size() {
        return data.size();
    }
    bool find(T x) {
        for (T& item : data) {
            if (item == x) {
                return true;
            }
        }
        return false;
    }
    void erase(T x) {
        for (auto iter = data.begin(); iter != data.end(); ++iter) {
            if (x == *iter) {
                data.erase(iter);
                return;
            }
        }
    }
private:
    std::vector<T> data;
};
