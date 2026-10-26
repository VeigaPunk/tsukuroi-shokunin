#include <stdio.h>
#include <string.h>
#include <alpm.h>
#include <alpm_list.h>
int main(int argc, char **argv){
	alpm_errno_t err = 0;
	alpm_handle_t *h = alpm_initialize("/", "/var/lib/pacman/", &err);
	if(!h){ fprintf(stderr,"init fail %d\n",(int)err); return 1; }
	int i=0;
	for(alpm_list_t *l = alpm_option_get_hookdirs(h); l; l = alpm_list_next(l))
		printf("%d: [%s]\n", ++i, (char*)l->data);
	if(argc>1 && strcmp(argv[1],"--add")==0)
		alpm_option_add_hookdir(h,"/etc/pacman.d/hooks/");
	if(argc>2){
		printf("-- after add_hookdir %s\n", argv[2]);
		alpm_option_add_hookdir(h, argv[2]);
		for(alpm_list_t *l = alpm_option_get_hookdirs(h); l; l = alpm_list_next(l))
			printf("%d: [%s]\n", ++i, (char*)l->data);
	}
	alpm_release(h);
	return 0;
}
