!/bin/sh
echo Checking Docker..
if docker --version ; then 
	docker pull nerukaneo/ex_to_graph:v1
	curl https://raw.githubusercontent.com/nerukaadmin/Excel-to-Graph-Container/main/init-con --output init-con
	echo init Pulled.
	curl https://raw.githubusercontent.com/nerukaadmin/Excel-to-Graph-Container/main/ex_to_graph.py --output ex_to_graph.py
	echo ex_to_graph.py Pulled.
	mkdir -p OUT
	mkdir -p IN
	mkdir -p tmp
	mkdir -p TM
	chmod -R 777 OUT
	chmod -R 777 IN
	chmod -R 777 tmp
	chmod -R 777 TM
	touch ./TM/team_member_list.txt
	chmod 777 ./TM/team_member_list.txt
	echo Folder stucture completed...!
	echo creating run.sh
	cat init-con > run.sh
	rm init-con 
else
	echo install Docker..
	echo please visit https://docs.docker.com/engine/install/ubuntu/
fi