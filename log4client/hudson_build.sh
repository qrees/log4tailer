cd $WORKSPACE/log4client
CWD=`pwd`
make env
export PATH=$CWD/ENV/bin:$PATH
make all

# HACK to make the hudson job fail if tests fail
sed -i -e 's/coverage.main()/sys.exit(coverage.main())/' bin/coverage

make runtests

# abort job if tests failed
if [ $? -ne 0 ]; then
    echo "Error while running the tests, please check"
    exit -1
fi

make pylint > /dev/null 2>&1
make release
make coberturasource

