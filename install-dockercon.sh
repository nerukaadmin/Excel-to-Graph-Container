!/bin/sh
echo Checking Docker..
if docker --version ; then 
	docker pull nerukaneo/ex_to_graph:v1
	curl https://raw.githubusercontent.com/nerukaadmin/Excel-to-Graph-Container/main/init-con --output init
	echo init Pulled.
	mkdir -p  OUT
	mkdir -p  IN
	mkdir -p  tmp
	chmod  -R 777 OUT
	chmod  -R 777 IN
	chmod  -R 777 tmp
	touch team_member_list.txt
	chmod 777 team_member_list.txt
	echo Folder stucture completed...!
	echo creating run.sh
	cat init-con > run.sh
	rm init-con 
else
	echo install Docker..
	echo please visit https://docs.docker.com/engine/install/ubuntu/
fi