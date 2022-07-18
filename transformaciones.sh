#Díaz-Gómez	, Marie 		marie.diaz-gomez@utp.ac.pa
#Martinez	, Margareth 	margareth.martinez@utp.ac.pa
#Zeledón	, Diana 		diana.zeledon@utp.ac.pa

#Este código transforma de shp file a sql para poder insertarlo a la base de datos
echo "INICIANDO CONVERSIÓN DE SHP A SQL" 
shp2pgsql -i -s 4326 -W "UTF8" pan_adm0.shp pan_pais > pan_pais.sql
shp2pgsql -i -s 4326 -W "UTF8" pan_adm1.shp pan_adm1 > pan_adm1.sql
shp2pgsql -i -s 4326 -W "UTF8" pan_adm2.shp pan_adm2 > pan_adm2.sql
shp2pgsql -i -s 4326 -W "UTF8" pan_adm3.shp pan_adm3 > pan_adm3.sql
shp2pgsql -i -s 4326 -W "UTF8" pan_roads.shp pan_roads > pan_roads.sql
shp2pgsql -i -s 4326 -W "UTF8" reciclajeaceite.shp reciclajeaceite > reciclajeaceite.sql
shp2pgsql -i -s 4326 -W "UTF8" reciclajebaterias.shp reciclajebaterias > reciclajebaterias.sql
echo "FINALIZADO" 

