cd $WORKSPACE/log4client
CWD=`pwd`
COVERAGE=bin/coverage
TEST=bin/unittests
UNITTESTXML=unittests.xml

make all

# HACK to make the hudson job fail if tests fail
sed -i -e 's/coverage.main()/sys.exit(coverage.main())/' bin/coverage
#sed -i -e 's/pytest.main()/sys.exit(pytest.main())/' bin/py.test

$COVERAGE run --pylib --branch --source=src/log4tailer $TEST -v --with-xunit --xunit-file=$UNITTESTXML
cp tests/$UNITTESTXML .
if [ $? -ne 0 ]; then
    echo "Error while running the tests, please check"
    exit -1
fi
$COVERAGE xml 
make pylint > /dev/null 2>&1
make coberturasource
