/* C2-26 harness: EX6 (NeedsTargets stdin feed) from pinned source.
 *
 * _alpm_hook_feed_targets and _alpm_strlist_dedup below are copied VERBATIM
 * (byte-identical, checked by diff) from
 *   .ufo/waves/round-40/frozen/src/hook.c:469-505
 * which FETCH.txt pins to pacman 54d9411, sha256
 *   99f1044badd36f83bb781d9d59409b0cdff0f26e1aa95ebd88d0f25f776b199a
 *
 * alpm_list_remove_item is copied VERBATIM from upstream
 *   lib/libalpm/alpm_list.c@54d9411 (fetched 2026-10-26,
 *   sha256 3bb690c42eaef06e6bd2d512aadb47a61e14ab231a802d0abadb89285ece0ba3).
 *
 * Per assignment alpm_list_msort is replaced with qsort + strcmp over the
 * node data pointers (msort_repl). alpm_list_t is a minimal stand-in with the
 * real layout (next, prev, data) and the real head->prev == tail invariant.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>

typedef struct _alpm_list_t {
	struct _alpm_list_t *next, *prev;
	void *data;
} alpm_list_t;

/* ---------------------------------------------------------------- stand-in */
/* verbatim from lib/libalpm/alpm_list.c@54d9411 */
alpm_list_t *alpm_list_remove_item(alpm_list_t *haystack,
		alpm_list_t *item)
{
	if(haystack == NULL || item == NULL) {
		return haystack;
	}

	if(item == haystack) {
		/* Special case: removing the head node which has a back reference to
		 * the tail node */
		haystack = item->next;
		if(haystack) {
			haystack->prev = item->prev;
		}
		item->prev = NULL;
	} else if(item == haystack->prev) {
		/* Special case: removing the tail node, so we need to fix the back
		 * reference on the head node. We also know tail != head. */
		if(item->prev) {
			/* i->next should always be null */
			item->prev->next = item->next;
			haystack->prev = item->prev;
			item->prev = NULL;
		}
	} else {
		/* Normal case, non-head and non-tail node */
		if(item->next) {
			item->next->prev = item->prev;
		}
		if(item->prev) {
			item->prev->next = item->next;
		}
	}

	return haystack;
}

static int cmp_ptr(const void *a, const void *b)
{
	return strcmp(*(char *const *)a, *(char *const *)b);
}

/* replacement for alpm_list_msort(list, n, (alpm_list_fn_cmp)strcmp):
 * sorts by data with strcmp, keeping node linkage intact */
static alpm_list_t *msort_repl(alpm_list_t *list, size_t n)
{
	alpm_list_t *it;
	char **arr;
	size_t i;

	if(!list || n < 2) {
		return list;
	}
	arr = malloc(n * sizeof *arr);
	if(!arr) {
		abort();
	}
	for(it = list, i = 0; it && i < n; it = it->next) {
		arr[i++] = it->data;
	}
	qsort(arr, i, sizeof *arr, cmp_ptr);
	for(it = list, i = 0; it && i < n; it = it->next, i++) {
		it->data = arr[i];
	}
	free(arr);
	return list;
}

/* list constructor helpers (head->prev is the tail, as in alpm) */
static alpm_list_t *append(alpm_list_t *head, char *s)
{
	alpm_list_t *node = calloc(1, sizeof *node);
	if(!node) {
		abort();
	}
	node->data = s;
	if(!head) {
		node->prev = node; /* head->prev == tail */
		return node;
	}
	node->prev = head->prev;
	head->prev->next = node;
	head->prev = node;
	return head;
}

static size_t count(alpm_list_t *list)
{
	size_t n = 0;
	for(; list; list = list->next) {
		n++;
	}
	return n;
}

/* ---------------------------------------------------- verbatim hook.c code */
static ssize_t _alpm_hook_feed_targets(char *buf, ssize_t needed, alpm_list_t **pos)
{
	size_t remaining = needed, written = 0;;
	size_t len;

	while(*pos && (len = strlen((*pos)->data)) + 1 <= remaining) {
		memcpy(buf, (*pos)->data, len);
		buf[len++] = '\n';
		*pos = (*pos)->next;
		buf += len;
		remaining -= len;
		written += len;
	}

	if(*pos && remaining) {
		memcpy(buf, (*pos)->data, remaining);
		(*pos)->data = (char*) (*pos)->data + remaining;
		written += remaining;
	}

	return written;
}

static alpm_list_t *_alpm_strlist_dedup(alpm_list_t *list)
{
	alpm_list_t *i = list;
	while(i) {
		alpm_list_t *next = i->next;
		while(next && strcmp(i->data, next->data) == 0) {
			list = alpm_list_remove_item(list, next);
			free(next);
			next = i->next;
		}
		i = next;
	}
	return list;
}

/* ------------------------------------------------------------- test driver */
static char *esc(const char *s, size_t n)
{
	static char *out;
	static size_t cap;
	size_t i, o = 0;

	if(cap < n * 4 + 64) {
		cap = n * 4 + 64;
		out = realloc(out, cap);
		if(!out) {
			abort();
		}
	}
	for(i = 0; i < n; i++) {
		unsigned char c = (unsigned char)s[i];
		if(c == '\n') {
			out[o++] = '\\';
			out[o++] = 'n';
		} else if(c >= 32 && c < 127) {
			out[o++] = (char)c;
		} else {
			o += (size_t)sprintf(out + o, "\\x%02x", c);
		}
	}
	out[o] = '\0';
	return out;
}

static void check_stream(const char *what, const char *s, size_t n)
{
	size_t i, lines = 0;
	int sorted = 1, dedup = 1, prev_seen = 0;
	const char *lstart = s, *prev = NULL;
	size_t prevlen = 0;

	for(i = 0; i < n; i++) {
		if(s[i] != '\n') {
			continue;
		}
		lines++;
		size_t llen = (size_t)(s + i - lstart);
		if(prev) {
			int c = strncmp(prev, lstart, prevlen < llen ? prevlen : llen);
			if(c == 0 && prevlen != llen) {
				c = prevlen < llen ? -1 : 1;
			}
			if(c > 0) {
				sorted = 0;
			}
			if(c == 0) {
				dedup = 0;
			}
		}
		prev = lstart;
		prevlen = llen;
		prev_seen = 1;
		lstart = s + i + 1;
	}
	printf("  %s: bytes=%zu lines=%zu sorted=%s dedup=%s last_byte_newline=%s trailing_garbage=%zu\n",
			what, n, lines, sorted ? "yes" : "NO", dedup ? "yes" : "NO",
			(n && s[n - 1] == '\n') ? "yes" : "NO", n - (size_t)(lstart - s));
	(void)prev_seen;
}

/* loop exactly as _alpm_chroot_write_to_child + run_chroot do: the callback is
 * called only when the buffer is empty; its whole return value is written. */
static char *feed(alpm_list_t **posp, size_t bufsize, const char *label,
		size_t *out_len, int *calls_out)
{
	alpm_list_t *pos = *posp;
	char *buf = malloc(bufsize);
	char *stream = calloc(1, 1);
	size_t total = 0;
	int call = 0;

	printf("%s (buf=%zu)\n", label, bufsize);
	if(!buf || !stream) {
		abort();
	}
	for(;;) {
		ssize_t n = _alpm_hook_feed_targets(buf, (ssize_t)bufsize, &pos);
		if(n == 0) {
			printf("  call %d: n=0 -> loop ends, pipe closed\n", call);
			break;
		}
		if(n < 0 || (size_t)n > bufsize) {
			printf("  call %d: INVALID n=%zd\n", call, n);
			break;
		}
		stream = realloc(stream, total + (size_t)n + 1);
		if(!stream) {
			abort();
		}
		memcpy(stream + total, buf, (size_t)n);
		total += (size_t)n;
		stream[total] = '\0';
		printf("  call %d: n=%zd chunk=\"%s\" ends_with_newline=%s\n", call, n,
				esc(buf, (size_t)n),
				buf[n - 1] == '\n' ? "yes" : "NO");
		call++;
		if(call > 4096) {
			printf("  RUNAWAY\n");
			break;
		}
	}
	printf("  STREAM(%zu bytes)=\"%s\"\n", total, esc(stream, total));
	check_stream("checks", stream, total);
	if(out_len) {
		*out_len = total;
	}
	if(calls_out) {
		*calls_out = call;
	}
	*posp = pos;
	free(buf);
	return stream;
}

static alpm_list_t *fixture(char **v, size_t n)
{
	alpm_list_t *l = NULL;
	size_t i;
	for(i = 0; i < n; i++) {
		l = append(l, v[i]);
	}
	return l;
}

static void dump_list(const char *what, alpm_list_t *l)
{
	printf("%s: [", what);
	for(; l; l = l->next) {
		printf("\"%s\"%s", (char *)l->data, l->next ? ", " : "");
	}
	printf("]\n");
}

int main(void)
{
	/* duplicates from two triggers, unsorted input, mixed depths */
	char *raw[] = {"usr/lib/firmware/b", "etc/pacman.conf", "usr/lib/firmware/b",
			"usr/bin/pacman", "etc/pacman.conf", "usr/share/doc/x",
			"etc/pacman.conf", "usr/bin/pacman-db-upgrade"};
	size_t nraw = sizeof raw / sizeof raw[0];
	alpm_list_t *l;
	char *s4096, *s16, *s16b;
	size_t n4096, n16, n16b;
	int calls4096, calls16, calls16b;

	/* T0: sort + dedup only, no feed */
	l = fixture(raw, nraw);
	printf("T0 sort+dedup: input n=%zu\n", count(l));
	l = msort_repl(l, count(l));
	dump_list("  after msort_repl", l);
	l = _alpm_strlist_dedup(l);
	dump_list("  after _alpm_strlist_dedup", l);
	printf("  head->prev==tail=%s\n", (l && l->prev && l->prev->next == NULL) ? "yes" : "NO");

	/* T1: 4096-byte buffer (real run_chroot buffer is LINE_MAX=2048, util.c:706) */
	l = fixture(raw, nraw);
	l = msort_repl(l, count(l));
	l = _alpm_strlist_dedup(l);
	s4096 = feed(&l, 4096, "T1 feed 4096-byte buffer", &n4096, &calls4096);
	free(s4096);

	/* T2: same logical matches through a 16-byte buffer */
	l = fixture(raw, nraw);
	l = msort_repl(l, count(l));
	l = _alpm_strlist_dedup(l);
	s16 = feed(&l, 16, "T2 feed 16-byte buffer", &n16, &calls16);

	/* T3: 16-byte buffer with a long final target so the partial-write branch
	 * (:483-487) fires on the last list node */
	{
		char *tail[] = {"etc/pacman.conf", "usr/bin/pacman",
				"usr/share/doc/pacman/hooks/verylongtargetname.txt"};
		size_t ntail = sizeof tail / sizeof tail[0];
		alpm_list_t *l3 = fixture(tail, ntail);
		l3 = msort_repl(l3, count(l3));
		l3 = _alpm_strlist_dedup(l3);
		s16b = feed(&l3, 16, "T3 16-byte buffer, long tail target", &n16b, &calls16b);
		free(s16b);
	}

	/* T4: single target whose length exactly fills a 16-byte buffer */
	{
		char *one[] = {"0123456789abcdef"}; /* 16 chars: 16+1 > 16 */
		alpm_list_t *l4 = fixture(one, 1);
		size_t n4;
		int c4;
		char *s4 = feed(&l4, 16, "T4 single 16-char target, 16-byte buffer", &n4, &c4);
		free(s4);
	}

	/* T5: empty match list -> callback returns 0 immediately */
	{
		alpm_list_t *l5 = NULL;
		size_t n5;
		int c5;
		char *s5 = feed(&l5, 16, "T5 empty list", &n5, &c5);
		free(s5);
	}

	/* T7: the partial branch advances (*pos)->data, so the list node no longer
	 * points at the start of its string. hook.c frees only the nodes
	 * (alpm_list_free, hook.c:81) and re-parses hooks per run, so this is not
	 * an invalid free; it does make the list non-idempotent. */
	{
		char *one[] = {"0123456789abcdefghij"}; /* 20 chars, 16-byte buffer */
		alpm_list_t *l7 = fixture(one, 1);
		alpm_list_t *head7;
		char *orig;
		l7 = msort_repl(l7, count(l7));
		l7 = _alpm_strlist_dedup(l7);
		head7 = l7;
		orig = (char *)head7->data;
		size_t n7;
		int c7;
		char *s7 = feed(&l7, 16, "T7 partial branch mutates node data pointer", &n7, &c7);
		printf("T7 node->data after partial: \"%s\" (orig \"%s\", advanced %td bytes)\n",
				(char *)head7->data, orig, (char *)head7->data - orig);
		/* re-feed the same head node from the beginning (what a second
		 * invocation over the same list would send) */
		{
			alpm_list_t *pos = head7;
			char buf[16];
			char again[64];
			size_t got = 0;
			ssize_t n;
			while((n = _alpm_hook_feed_targets(buf, 16, &pos)) > 0) {
				memcpy(again + got, buf, (size_t)n);
				got += (size_t)n;
			}
			again[got] = '\0';
			printf("T7 re-feed same list from head: \"%s\" (%zu bytes, first run was %zu)\n",
					esc(again, got), got, n7);
		}
		free(s7);
	}

	/* T8: real production buffer LINE_MAX=2048 (util.c:706) with a realistic
	 * many-match hook: >2048 bytes of targets, so the partial branch fires at
	 * every buffer boundary. */
	{
		static char paths[60][64];
		char *many[60];
		int i;
		alpm_list_t *l8 = NULL;
		size_t n8;
		int c8;
		char *s8;

		for(i = 0; i < 60; i++) {
			snprintf(paths[i], sizeof paths[i],
					"usr/lib/python3.13/site-packages/pkg%02d/module%02d.py", i % 7, i);
			many[i] = paths[i];
		}
		/* add duplicates from a second trigger */
		l8 = fixture(many, 60);
		for(i = 0; i < 20; i++) {
			l8 = append(l8, many[i]);
		}
		printf("T8 input n=%zu\n", count(l8));
		l8 = msort_repl(l8, count(l8));
		l8 = _alpm_strlist_dedup(l8);
		{
			size_t total = 0;
			alpm_list_t *it;
			for(it = l8; it; it = it->next) {
				total += strlen((char *)it->data) + 1;
			}
			printf("T8 input n=%zu total_target_bytes=%zu (LINE_MAX buffer=2048)\n",
					count(l8), total);
		}
		s8 = feed(&l8, 2048, "T8 production LINE_MAX=2048 buffer", &n8, &c8);
		(void)s8;
	}

	/* T9: strcmp ordering is bytewise (no locale collation) and prefixes are
	 * distinct targets, not duplicates. */
	{
		char *casev[] = {"etc/Z", "etc/a", "usr/bin/foo", "usr/bin/foo-bar",
				"etc/a", "usr/bin/Foo"};
		alpm_list_t *l9 = fixture(casev, sizeof casev / sizeof casev[0]);
		size_t n9;
		int c9;
		char *s9;
		l9 = msort_repl(l9, count(l9));
		l9 = _alpm_strlist_dedup(l9);
		s9 = feed(&l9, 4096, "T9 bytewise strcmp order, prefix vs exact", &n9, &c9);
		free(s9);
	}

	/* cross-buffer equality */
	{
		alpm_list_t *la = fixture(raw, nraw);
		alpm_list_t *lb = fixture(raw, nraw);
		size_t na, nb;
		int ca, cb;
		char *sa, *sb;
		la = msort_repl(la, count(la));
		la = _alpm_strlist_dedup(la);
		lb = msort_repl(lb, count(lb));
		lb = _alpm_strlist_dedup(lb);
		sa = feed(&la, 4096, "T6a 4096", &na, &ca);
		sb = feed(&lb, 16, "T6b 16", &nb, &cb);
		printf("T6 stream equality across buffers: %s (4096 n=%zu calls=%d, 16 n=%zu calls=%d)\n",
				(na == nb && memcmp(sa, sb, na) == 0) ? "IDENTICAL" : "DIFFER",
				na, ca, nb, cb);
		free(sa);
		free(sb);
	}

	(void)s16;
	(void)s16b;
	(void)n4096;
	(void)n16;
	(void)n16b;
	(void)calls4096;
	(void)calls16;
	(void)calls16b;
	return 0;
}
