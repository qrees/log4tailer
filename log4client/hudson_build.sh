cd $WORKSPACE/log4client
CWD=`pwd`
make env
export PATH=$CWD/ENV/bin:$PATH
easy_install coverage
make all
make runtests
make pylint > /dev/null 2>&1
make release

