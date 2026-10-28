import re
BASE_ASSIGN = re.compile(r'(?:^|[\s;])\w*base\w*=/tmp(?![\w/.-])')
for s in ['base=/tmp','local st_base=/tmp','base=/tmp/',"base='/tmp'",'st_base="/tmp"','ST_BASE_DIR=/tmp','base=${TMPDIR:-/tmp}','eval "base=/tmp"','(base=/tmp)','x=$(base=/tmp; echo)','base=/tmp;','base=/tmp ;;','base=/tmp\\','work=/tmp','st_dir=/tmp','base =/tmp','base=/tmp-x','base=/tmpfoo','export base=/tmp','base=$(echo /tmp)','base=//tmp','base=/tmp//','base=/tmp.','  base=/tmp # c']:
    print(f'{s!r:32} flagged={bool(BASE_ASSIGN.search(s))}')
