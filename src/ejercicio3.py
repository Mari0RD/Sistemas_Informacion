import sqlite3
import pandas as pd

con = sqlite3.connect('database.db')
c = con.cursor()

''' <--------------------------------------------------------- AGRUPACIÓN POR PERMISOS ---------------------------------------------------------> '''
''' Numero de observaciones '''
dataframe = pd.read_sql_query("SELECT phishingEmails FROM users GROUP BY username", con)

print("<--- PERMISOS DE ADMINISTRADOR (1) --->")
dfAdminPhishing = pd.read_sql_query("SELECT phishingEmails FROM users WHERE users.permissions = 1 GROUP BY username", con)
emailPhising = int(dfAdminPhishing.sum())
print("Numero de observaciones: ", emailPhising)


''' Numero de valores ausentes '''
missing = 0
for index, row in dataframe.iterrows():
    if row['phishingEmails'] == 'None':
        missing = missing + 1

print("Numero de valores ausentes: ", missing)


''' MEDIANA (.median()) '''
median = int(dfAdminPhishing.median())
print ("Mediana: ", median)

''' MEDIA (.mean())) '''
avarage = float(dfAdminPhishing.mean())
print ("Media: ", avarage)

''' VARIANZA (.var())) '''
variance = float(dfAdminPhishing.var())
print ("Varianza: ", variance)

''' MIN (.min())) '''
min = int(dfAdminPhishing.min())
print("Minimo: ", min)

''' MAX (.max()) '''
max = int(dfAdminPhishing.max())
print ("Maximo: ", max)


print ("\n<--- PERMISOS DE USUARIO (0) --->")
dfUserPhishing = pd.read_sql_query("SELECT phishingEmails FROM users WHERE users.permissions = 0 GROUP BY username", con)
emailPhising = int(dfUserPhishing.sum())
print("Numero de observaciones: ", emailPhising)

''' Numero de valores ausentes '''
missing = 0
for index, row in dataframe.iterrows():
    if row['phishingEmails'] == 'None':
        missing = missing + 1

print("Numero de valores ausentes: ", missing)

''' MEDIANA (.median())) '''
median = int(dfUserPhishing.median())
print ("Mediana: ", median)

''' MEDIA (.mean())) '''
avarage = float(dfUserPhishing.mean())
print ("Media: ", avarage)

''' VARIANZA (.var())) '''
variance = float(dfUserPhishing.var())
print ("Varianza: ", variance)

''' MIN (.min())) '''
min = int(dfUserPhishing.min())
print("Minimo: ", min)

''' MAX (.max()) '''
max = int(dfUserPhishing.max())
print ("Maximo: ", max)


''' <--------------------------------------------------------- AGRUPACIÓN POR NUMERO DE CORREOS ---------------------------------------------------------> '''
print("\n<--- CANTIDAD DE CORREOS MAYOR O IGUAL A 200 --->")
df200_OrMoreMail = pd.read_sql_query("SELECT phishingEmails FROM users WHERE users.totalEmails >= 200 GROUP BY username", con)
emailPhising = int(df200_OrMoreMail.sum())
print("Numero de observaciones: ", emailPhising)

''' Numero de valores ausentes '''
missing = 0
for index, row in dataframe.iterrows():
    if row['phishingEmails'] == 'None':
        missing = missing + 1

print("Numero de valores ausentes: ", missing)

''' MEDIANA (.median())) '''
median = float(df200_OrMoreMail.median())
print ("Mediana: ", median)

''' MEDIA (.mean())) '''
avarage = float(df200_OrMoreMail.mean())
print ("Media: ", avarage)

''' VARIANZA (.var())) '''
variance = float(df200_OrMoreMail.var())
print ("Varianza: ", variance)

''' MIN (.min())) '''
min = int(df200_OrMoreMail.min())
print("Minimo: ", min)

''' MAX (.max()) '''
max = int(df200_OrMoreMail.max())
print ("Maximo: ", max)


print ("\n<--- CANTIDAD CORREOS MENOR A 200 --->")
df200_lessMail = pd.read_sql_query("SELECT phishingEmails FROM users WHERE users.totalEmails < 200 GROUP BY username", con)
emailPhising = int(df200_lessMail.sum())
print("Numero de observaciones: ", emailPhising)

''' Numero de valores ausentes '''
missing = 0
for index, row in dataframe.iterrows():
    if row['phishingEmails'] == 'None':
        missing = missing + 1

print("Numero de valores ausentes: ", missing)

''' MEDIANA (.median())) '''
median = int(df200_lessMail.median())
print ("Mediana: ", median)

''' MEDIA (.mean())) '''
avarage = float(df200_lessMail.mean())
print ("Media: ", avarage)

''' VARIANZA (.var())) '''
variance = float(df200_lessMail.var())
print ("Varianza: ", variance)

''' MIN (.min()) '''
min = int(df200_lessMail.min())
print("Minimo: ", min)

''' MAX (.max()) '''
max = int(df200_lessMail.max())
print ("Maximo: ", max)