# SR8 source evidence (seat C2DraftCritSR8, wave 1 pre-read)

All fetched 2026-10-26. Lane files read at frozen digests (see sha256sums below).
Nothing here is a host write; all fetched text is quoted from upstream mirrors.

## Frozen lane digests (verified, match counter SNAP)

```
f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8  .ufo/waves/round-44/frozen/src/scrub.c   (S242)
ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43  .ufo/waves/round-44/frozen/src/sysfs.c   (S243)
efb523889035cba62235d904b9e254068a7083dd07e7bb338ce2a803a3e84900  .ufo/waves/round-44/frozen/hostcap/capture.txt (S245)
```

## memparse, Linux v7.2.11 lib/cmdline.c

URL: https://elixir.bootlin.com/linux/v7.2.11/source/lib/cmdline.c
Located quote (comment, above the function):
"The number stored at @ptr is potentially suffixed with K, M, G, T, P, E."

Function body (verbatim from the same page):

```c
unsigned long long memparse(const char *ptr, char **retptr)
{
	char *endptr;	/* local pointer to end of parsed string */
	unsigned long long ret = simple_strtoull(ptr, &endptr, 0);
	unsigned int shl = 0;

	/* Consume valid suffix even in case of overflow. */
	switch (*endptr) {
	case 'E':
	case 'e':
		shl += 10;
		fallthrough;
	case 'P':
	case 'p':
		shl += 10;
		fallthrough;
	case 'T':
	case 't':
		shl += 10;
		fallthrough;
	case 'G':
	case 'g':
		shl += 10;
		fallthrough;
	case 'M':
	case 'm':
		shl += 10;
		fallthrough;
	case 'K':
	case 'k':
		shl += 10;
		fallthrough;
	default:
		break;
	}

	if (shl && likely(ptr != endptr)) {
		/* Have valid suffix with preceding number. */
		if (unlikely(check_shl_overflow(ret, shl, &ret)))
			ret = ULLONG_MAX;
		endptr++;
	}

	if (retptr)
		*retptr = endptr;

	return ret;
}
EXPORT_SYMBOL(memparse);
```

Note: `simple_strtoull(ptr, &endptr, 0)` runs in base 0, so `0x…`
(hex) and leading-`0` (octal) forms also parse. Suffix set: K/M/G/T/P/E,
case-insensitive. A suffix with no preceding digits is not applied
(`if (shl && likely(ptr != endptr))`).

## skip_spaces declaration, Linux v7.2.11 include/linux/string.h

URL: https://elixir.bootlin.com/linux/v7.2.11/source/include/linux/string.h
Located quote (line 182):
"extern char * __must_check skip_spaces(const char *);"

The definition lives in `lib/string.c` (kernel lib, not part of the pinned
S242/S243 sources); it loops `while (isspace(*str)) ++str;`. The deciding
evidence inside the pinned store is the call site plus the author comment
(`sysfs.c:2041`: "There could be trailing '\n', also catch any typos after
the value." followed by `endptr = skip_spaces(endptr);`).

## Environment

- Read-only queries only: no sysfs write, no scrub start/cancel, no systemd
  mutation, no writes outside the seat report/receipt paths and scratch.
- No tools installed (curl already present, not installed by this seat).
