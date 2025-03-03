template <typename Iterator, typename Compare = std::less<>>
void selection_sort(Iterator first, Iterator last, Compare comp = Compare()) {
    for (Iterator i = first; i != last; i++) {
        Iterator min = i;
        for (Iterator j = i; j != last; j++) {
            if (comp(*j, *min)) {
                min = j;
            }
        }
        std::swap(*i, *min);
    }
}
