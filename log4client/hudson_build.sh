cd $WORKSPACE/log4client
CWD=`pwd`
make env
export PATH=$CWD/ENV/bin:$PATH
make all
make runtests
make pylint > /dev/null 2>&1
make release
