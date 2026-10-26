#include <stdio.h>
int alpm_pkg_vercmp(const char *a, const char *b);
int main(int argc, char *argv[]) {
	if(argc != 3) return 2;
	printf("%d\n", alpm_pkg_vercmp(argv[1], argv[2]));
	return 0;
}
