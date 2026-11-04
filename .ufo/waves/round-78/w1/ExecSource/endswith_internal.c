sd_char* endswith_internal(const sd_char *s, const sd_char *suffix) {
        size_t sl, pl;

        assert(s);
        assert(suffix);

        sl = strlen(s);
        pl = strlen(suffix);

        if (pl == 0)
                return (sd_char*) s + sl;

        if (sl < pl)
                return NULL;

        if (!streq(s + sl - pl, suffix))
                return NULL;

        return (sd_char*) s + sl - pl;
}
