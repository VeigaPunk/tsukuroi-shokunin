/* Brute force the two universal words in GR1:
 *  (a) "the suffix counts only when at least one digit came before it"
 *  (b) "takes at most one suffix letter"
 * Functions are the pinned ones from harness.c.
 */
#define main harness_main
#include "harness.c"
#undef main

int main(void)
{
	const char alpha[] = "01xXKkaFf -9g\n";
	char s[6];
	int n = (int)strlen(alpha), L, i, j, k, m;
	long tried = 0, suffixed = 0, bad_a = 0, bad_b = 0;

	for (L = 1; L <= 4; L++) {
		int idx[4] = {0};
		long total = 1;
		for (i = 0; i < L; i++) total *= n;
		for (long c = 0; c < total; c++) {
			long t = c;
			for (i = 0; i < L; i++) { idx[i] = (int)(t % n); t /= n; }
			for (i = 0; i < L; i++) s[i] = alpha[idx[i]];
			s[L] = '\0';
			{
				char *e0, *ep;
				(void)simple_strtoull(s, &e0, 0);
				(void)memparse(s, &ep);
				tried++;
				if (ep > e0) {
					suffixed++;
					if (!(e0 > s)) { bad_a++; if (bad_a < 4) printf("A-VIOLATION %s\n", s[0]=='\n'?"\\n":s); }
					if (ep - e0 > 1) { bad_b++; if (bad_b < 4) printf("B-VIOLATION %s\n", s); }
				}
			}
		}
		(void)j; (void)k; (void)m;
	}
	printf("tried=%ld suffixed=%ld violations_a=%ld violations_b=%ld\n", tried, suffixed, bad_a, bad_b);
	return 0;
}
