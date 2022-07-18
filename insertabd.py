import psycopg2

con = psycopg2.connect(database="d336iu9egej1ot", user="cvofatnojoxawg", password="54c370f6f702d93001ddbf870a5c5fe58868f4b021db069f258ae5b1353e1552", host="ec2-54-86-224-85.compute-1.amazonaws.com", port = "5432")
cur = con.cursor() 
print("Conexión exitosa\n\n")

cur.execute('''CREATE EXTENSION postgis;''')
cur.execute('''CREATE EXTENSION fuzzystrmatch;''')
cur.execute('''CREATE EXTENSION postgis_topology;''')
cur.execute('''CREATE EXTENSION postgis_tiger_geocoder;''')

print("Extensiones creadas")

print("Crear tablas")



sql_file1 = open('pan_pais.sql','r', encoding="utf-8")
cur.execute(sql_file1.read())

sql_file2 = open('pan_adm1.sql','r', encoding="utf-8")
cur.execute(sql_file2.read())

sql_file6 = open('reciclajebaterias.sql','r', encoding="utf-8")
cur.execute(sql_file6.read())

sql_file7 = open('reciclajeaceite.sql','r', encoding="utf-8")
cur.execute(sql_file7.read())


print("Tablas creadas")
#cur.execute(''' ''')

con.close()