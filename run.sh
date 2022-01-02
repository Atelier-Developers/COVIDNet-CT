build=$1
mode=$2
sudo rm -rf multiprocess_metrics/*.db
#export DISPLAY="$(grep nameserver /etc/resolv.conf | sed 's/nameserver //'):0"
if [ "$build" = "build" ];
then
docker-compose -f docker-compose.dev.yml -f docker-compose.yml up --build -d
fi
if [ "$mode" = "infer" ];
then
docker-compose -f docker-compose.dev.yml -f docker-compose.yml exec aphrodite ./interface/interface
else
docker-compose -f docker-compose.dev.yml -f docker-compose.yml exec aphrodite bash
fi
