import multiprocessing
import sqlite3
import pandas as pd
import hashlib
import matplotlib.pyplot as plt
import numpy as np

con = sqlite3.connect('database.db')
c = con.cursor()

''' Usamos por simplificación una lista (passwords.txt) con las contraseñas que hemos podido 
    descifrar previamente con https://crackstation.net/ '''

dataframe = pd.read_sql_query("SELECT username, phishingEmails, clicKedEmails, password FROM users", con)
filelist = open("passwords.txt").read().splitlines()


''' <--- Mostrar el numero de contrasenas comprometidas y contrasenas no comprometidas ---> '''
cont = 0
userList = []
for i in range(dataframe['password'].values.size):
    for line in filelist:
        if dataframe['password'].values[i] == hashlib.md5(line.encode('utf-8')).hexdigest():
            cont += 1
            userList.append(dataframe['username'].values[i]) # Lista con los usuarios con contraseña vulnerable

print("EL NUMERO DE CONTRASEÑAS COMPROMETIDAS SON: ", cont)

nTotal = int(dataframe['password'].count())
noCompromissed = nTotal - cont
print("EL NUMERO DE CONTRASEÑAS NO COMPROMETIDAS: ", noCompromissed)


''' <--- Mostrar los 10 usuarios mas criticos (un usuario critico es aquel usuario que tiene la contraseña debil y ademas tiene
         mayor probabilidad de pulsar en un correo de spam), representadas en un grafico de barras ---> '''
prob = []
for i in range(dataframe['username'].values.size):
    for j in range(len(userList)):
        if userList[j] == dataframe['username'].values[i]: # Comprueba si el usuario contenido en userlist coincide con los de la tabla
            if dataframe['phishingEmails'].values[i] == 0: # Evitamos division por 0.
                prob.append(0.0000000000000000)

            else: # Si el valor no es 0 calculamos la probabilidad
                prob.append(dataframe['clickedEmails'].values[i] / dataframe['phishingEmails'].values[i])

FinalList = []
for i in range(len(userList)):
    FinalList.append(str(prob[i]) + ':' + userList[i]) # Lista con la probabilidad que le corresponde a cada usuario


FinalList.sort(reverse=True) # Ordenamos la lista de mayor probabilidad a menor
listaFinal = FinalList[0:10] # Nos quedamos con los 10 primeros valores
criticUsers = []
probCriticUsers = []

for i in range(len(listaFinal)):
    criticUsers.append(listaFinal[i].split(":")[1]) # Dividimos la lista por el nombre de usuario
    probCriticUsers.append(listaFinal[i].split(":")[0]) # Dividimos la lista por la probabilidad del usuario

print("\n<--- TOP 10 USUARIOS CRITICOS --->")
for i in range(len(criticUsers)):
    print("USUARIO: " + criticUsers[i], "CON PROBABILIDAD DE: " + probCriticUsers[i])

''' CREACION DEL GRAFICO '''
reversedProbCriticUsers = list(reversed(probCriticUsers))
reversedCriticUsers = list(reversed(criticUsers))
indice = np.arange(len(criticUsers))
ancho = 0.35
plt.figure(1, [17, 5])
plt.bar(indice, reversedProbCriticUsers, width=ancho, color='cornflowerblue', label='default')
plt.xticks(indice, reversedCriticUsers)
plt.xlabel('Usuarios', fontsize=10)
plt.ylabel('Probabilidad de click', fontsize=10)
plt.title('TOP 10 USUARIOS CRITICOS', fontsize=10)
plt.show()


''' <--- Mostrar las 5 paginas web con que tienen mas politicas (cookies, proteccion de datos o aviso) desactualizadas,
         representadas en un grafico de barras segun las politicas --> '''

dfPolicies = pd.read_sql_query("SELECT url, cookies, warning, dataProtection FROM legal", con)
dfPolicies['result'] = dfPolicies['cookies'] + dfPolicies['warning'] + dfPolicies['dataProtection'] # Sumamos los valores de las columnas y lo guardamos en una llamada result
dfPolicies = dfPolicies.sort_values('result').head(5) # Ordenamos y sacamos las 5 primeras

print("\n<--- TOP 5 WEBS CON POLITICAS DESACTUALIZADAS --->")
print(dfPolicies)

''' CREACION DEL GRAFICO '''
indice = np.arange(len(dfPolicies))
ancho = 0.35
plt.figure (1, [17,5])
plt.bar(indice, dfPolicies['cookies'], width=ancho, color='mediumturquoise', label='default')
plt.bar(indice, dfPolicies['warning'], width=ancho, color='plum', label='default')
plt.bar(indice, dfPolicies['dataProtection'], width=ancho, color='mediumpurple', label='default')

plt.xticks(indice, dfPolicies['url'])
plt.xlabel('PAGINAS WEB', fontsize=10)
plt.title('TOP 5 WEBS CON POLITICAS DESACTUALIZADAS', fontsize=10)
plt.show()


''' <--- Mostrar la media de conexiones de usuarios con contraseña vulnerable, frente a los que no son vulnerables --> '''

'''vulnerableIPs = []
dfIPS = pd.read_sql_query("SELECT  user_id, ips FROM ips", con)
for i in range(len(userList)):
    for j in range(dfIPS['user_id'].values.size):
        if userList[i] == dfIPS['user_id'].values[j]:
            vulnerableIPs.append(dfIPS['ips'].values[j])

print("\n")
dfIPSv2 = pd.fillna(int(0)).to_numeric(pd.array(vulnerableIPs)).mean()
print(dfIPSv2)'''


''' <--- Mostrar segun el año de creacion las webs que cumplen todas las politicas de privacidad, frente a las que no
         cumplen la politica de privacidad ---> '''

dfPol = pd.read_sql_query("SELECT url, cookies, warning, dataProtection, creation FROM legal GROUP BY url", con)
dfPol['result'] = dfPol['cookies'] + dfPol['warning'] + dfPol['dataProtection'] # Sumamos las columnas

dfComply = dfPol[dfPol['result'] == 3] # Si todas las columnas estan a 1 cumple la politica (1 + 1 + 1)
print("\n <--- CUMPLE LAS POLITICAS --->")
print(dfComply)

''' CREACION DEL GRAFICO '''
indice = np.arange(len(dfComply))
ancho = 0.35
plt.figure(1, [14,5])
plt.bar(indice, dfComply['creation'], width=ancho, color='cornflowerblue', label='default')
plt.xticks(indice, dfComply['url'])
plt.ylim(1990, 2025)
plt.xlabel('PAGINAS WEB', fontsize=10)
plt.ylabel('AÑOS', fontsize=10)
plt.title('PAGINAS QUE CUMPLEN LAS POLITICAS', fontsize=10)
plt.show()


dfNoComply = dfPol[dfPol['result'] != 3] # Si no estan todas las columnas a 1 no cumple la politica
print("\n <--- NO CUMPLE LAS POLITICAS --->")
print(dfNoComply)

''' CREACION DEL GRAFICO '''
indice = np.arange(len(dfNoComply))
ancho = 0.35
plt.figure(1, [25,5])
plt.bar(indice, dfNoComply['creation'], width=ancho, color='cornflowerblue', label='default')
plt.xticks(indice, dfNoComply['url'])
plt.ylim(1990, 2025)
plt.xlabel('PAGINAS WEB', fontsize=10)
plt.ylabel('AÑOS', fontsize=10)
plt.title('PAGINAS QUE NO CUMPLEN LAS POLITICAS', fontsize=10)
plt.show()




