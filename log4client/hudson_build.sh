cd $WORKSPACE/log4client
CWD=`pwd`
COVERAGE=bin/coverage
TEST=bin/py.test

make env
export PATH=$CWD/ENV/bin:$PATH
make all

# HACK to make the hudson job fail if tests fail
sed -i -e 's/coverage.main()/sys.exit(coverage.main())/' bin/coverage
sed -i -e 's/pytest.main()/sys.exit(pytest.main())/' bin/py.test

$COVERAGE run $TEST -v --junitxml=unittests.xml tests
if [ $? -ne 0 ]; then
    echo "Error while running the tests, please check"
    exit -1
fi
$COVERAGE xml src/log4tailer/*.py
make pylint > /dev/null 2>&1
make release
make coberturasource

