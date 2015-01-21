# Adjust Following Configurations
LOCAL_FOLDER='/tmp/xxx'
SRC_GIT_ADDRESS='xxx@xxx.git' # Make sure you setup ssh keys correctly
DST_GIT_ADDRESS='yyy@yyy.git' # Make sure you setup ssh keys correctly
# END

if [ ! -d $LOCAL_FOLDER ]; then
    NAME=$(basename $LOCAL_FOLDER)
    DIR=$(dirname $LOCAL_FOLDER)
    cd $DIR
    git clone --mirror $SRC_GIT_ADDRESS $NAME
    cd $NAME
    git remote set-url --push origin $DST_GIT_ADDRESS
fi

cd $LOCAL_FOLDER
git fetch -p origin
git push --mirror
