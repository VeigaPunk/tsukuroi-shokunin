/* Driver: print alpm_pkg_vercmp(a,b) for argv pairs, tab separated. */
#include <stdio.h>
int SYMEXPORT alpm_pkg_vercmp(const char *a, const char *b);
int main(int argc, char **argv)
{
	int i;
	for (i = 1; i + 1 < argc; i += 2)
		printf("%s\t%s\t%d\n", argv[i], argv[i + 1],
				alpm_pkg_vercmp(argv[i], argv[i + 1]));
	return 0;
}
