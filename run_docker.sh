if [[ $# != 2 ]]; then
  echo "This script/docker runs the author crawler from the specified point"
  echo "Help: $0 <datadir> <startnumber to crawl>"
  exit 1
else
  DATA_DIR="$1"
  NUM_POINTS="$2"
fi
docker build -t tsg .


mkdir "$DATA_DIR" 2> /dev/null
docker run -v "$DATA_DIR":/root/tsgdata tsg tsg_crawl author --startnumber "$NUM_POINTS"
