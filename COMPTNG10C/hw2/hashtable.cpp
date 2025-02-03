#include "hashtable.h"

size_t hash_code(const std::string& str) {
    size_t h = 0;
    for (size_t i = 0; i < str.length(); i++) {
        h = 31 * h + str[i];
    }
    return h;
}

HashTable::HashTable(size_t nbuckets) {
    for (size_t i = 0; i < nbuckets; i++) {
        buckets.push_back(nullptr);
    }
    current_size = 0;
}

size_t HashTable::count(const std::string& x) {
    size_t h = hash_code(x) % buckets.size();
    Node* current = buckets[h];
    while (current != nullptr) {
        if (current->data == x) {
            return 1;
        }
        current = current->next;
    }
    return 0;
}

void HashTable::insert(const std::string& x) {
    size_t h = hash_code(x) % buckets.size();
    Node* current = buckets[h];
    while (current != nullptr) {
        if (current->data == x) {
            return;
        }
        current = current->next;
    }
    Node* new_node = new Node;
    new_node->data = x;
    new_node->next = buckets[h];
    buckets[h] = new_node;
    ++current_size;
    load_factor = (float) current_size / buckets.size();
    grow_if_necessary();
}

void HashTable::erase(const std::string& x) {
    size_t h = hash_code(x) % buckets.size();
    Node* current = buckets[h];
    Node** prev = &buckets[h];
    while (current != nullptr) {
        if (current->data == x) {
            *prev = current->next;
            delete current;
            --current_size;
            load_factor = (float) current_size / buckets.size();
            return;
        }
        prev = &(current->next);
        current = current->next;
    }
}

size_t HashTable::size() const {
    return current_size;
}

size_t HashTable::buckets_size() const {
    return buckets.size();
}

// Grow if necessary, and also shrink if possible
void HashTable::grow_if_necessary() {
    load_factor = (float) current_size / buckets.size();
    size_t new_bucket_size = buckets.size();
    ///// // I can't get this solution to work, because if I shrink the hash table while
    ///// // iterating through it, the iterators become invalid!!! Not sure how to fix that
    ///// if (load_factor < 0.25) {
    /////     // Make integer division round up, to avoid ever making a hash table with zero buckets
    /////     new_bucket_size = (new_bucket_size + 1) / 2;
    ///// } else if (load_factor > 0.75) {
    /////     new_bucket_size *= 2;
    ///// } else {
    /////     return;
    ///// }
    if (load_factor <= 0.75) {
        return;
    } else {
        new_bucket_size *= 2;
    }
    HashTable new_hash_table = HashTable(new_bucket_size);
    for (auto it = this->begin(); !it.equals(this->end()); it.next()) {
        new_hash_table.insert(it.get());
    }
    buckets      = new_hash_table.buckets;
    current_size = new_hash_table.current_size;
    load_factor  = new_hash_table.load_factor;
}

Iterator HashTable::begin() const {
    Iterator iter;
    iter.current = nullptr;
    iter.bucket_index = -1;
    iter.container = this;
    iter.next();
    return iter;
}

Iterator HashTable::end() const {
    Iterator iter;
    iter.current = nullptr;
    iter.bucket_index = buckets.size();
    iter.container = this;
    return iter;
}

std::string Iterator::get() const {
    return current->data;
}

bool Iterator::equals(const Iterator& other) const {
    return current == other.current;
}

void Iterator::operator++() {
    next();
}

void Iterator::next() {
    if (current != nullptr) {
        current = current->next;
    }
    // Use != instead of < here because bucket_index is unsigned and it can be -1,
    // which is stored as a very large positive number
    while (current == nullptr && bucket_index != container->buckets.size()) {
        ++bucket_index;
        if (bucket_index < container->buckets.size()) {
            current = container->buckets[bucket_index];
        } else {
            current = nullptr;
        }
    }
}
