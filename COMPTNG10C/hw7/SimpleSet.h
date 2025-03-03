template <typename T>
class simple_set {
public:
    simple_set() {}
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


template <typename T>
class simple_set<T*> {
public:
    simple_set() {}
    void insert(T* x) {
        if (!find(*x)) {
            data.push_back(x);
        }
    }
    size_t size() {
        return data.size();
    }
    bool find(T x) {
        for (T* item : data) {
            if (*item == x) {
                return true;
            }
        }
        return false;
    }
    void erase(T x) {
        for (auto iter = data.begin(); iter != data.end(); ++iter) {
            if (x == **iter) {
                data.erase(iter);
            }
        }
    }
private:
    std::vector<T*> data;
};


template <>
class simple_set<bool> {
public:
    simple_set() {}
    void insert(bool b) {
        if (b) {
            has_true = true;
        } else {
            has_false = true;
        }
    }
    void erase(bool b) {
        if (b) {
            has_true = false;
        } else {
            has_false = false;
        }
    }
    bool find(bool b) {
        return b && has_true || !b && has_false;
    }
    size_t size() {
        if (has_true && has_false) { return 2; }
        if (has_true || has_false) { return 1; }
        return 0;
    }
private:
    bool has_true = false;
    bool has_false = false;
};
