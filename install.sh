#!/bin/sh
echo Checking Docker..
if docker --version ; then 
	echo Docker installed..
else
	echo install Docker..
	echo please visit https://docs.docker.com/engine/install/ubuntu/
fi
curl https://raw.githubusercontent.com/nerukaadmin/Excel-to-Graph-Container/main/requirements.txt --output requirements.txt
echo requirements.txt Pulled.
curl https://raw.githubusercontent.com/nerukaadmin/Excel-to-Graph-Container/main/ex_to_graph.py --output ex_to_graph.py
echo ex_to_graph.py Pulled.
curl https://raw.githubusercontent.com/nerukaadmin/Excel-to-Graph-Container/main/Dockerfile --output Dockerfile
echo Dockerfile Pulled.
echo Cretaing DIR structure..!
mkdir -p  OUT
mkdir -p  IN
mkdir -p  tmp
chmod 777 -R OUT
chmod 777 -R IN
chmod 777 -R tmp
touch team_member_list.txt
chmod 777 team_member_list.txt
echo Installtion completed...!
echo Docker Image build.
docker build -t ex_to_graph:v1 .
echo creating run.sh
cat > run.sh <<EOF
#!/bin/sh
echo Pass argumrnt for script....
echo For all "a"
echo For team "t"
read input </dev/tty
docker run -v $(pwd):/excel ex_to_graph:v1 -e $input
chmod -R 777 ./OUT/
EOF