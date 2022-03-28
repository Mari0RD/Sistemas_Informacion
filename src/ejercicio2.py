import sqlite3
import pandas as pd

con = sqlite3.connect('database.db')
c = con.cursor()

dataframe = pd.read_sql_query("SELECT * FROM users group by username", con)


''' <--- Numero de muestras (valores distintos de missing) ---> '''
missing = 0
for index, row in dataframe.iterrows(): # recorremos el dataframe
    if row['phone'] == '0':
        missing = missing + 1

    if row['province'] == '0':
        missing = missing + 1

missing = missing + 4 # por las 4 ips a none que suprimimos
valores = len(dataframe) * len(dataframe.columns) - missing
print("Numero de muestras: ", valores)


''' <--- Media y desviacion estandar del total de fechas que se ha iniciado sesion ---> '''
dfDates = pd.read_sql_query("SELECT COUNT(dates) FROM dates GROUP BY user_id", con)

''' MEDIA (.mean()) '''
datesAverage = float(dfDates.mean())
print("Media del total de fechas que se ha iniciado sesion: ", datesAverage)

''' DESVIACI0N ESTANDAR (.std()) '''
datesDesviation = float(dfDates.std())
print("Desviacion estandar del total de fechas que se ha iniciado sesion: ", datesDesviation)


''' <--- Media y desviacion estandar del total de IPs que se han detectado ---> '''
dfIPs = pd.read_sql_query("SELECT COUNT(ips) FROM ips", con)

''' MEDIA (.mean()) '''
ipsAverage = float(dfIPs.sum() / len(dataframe))
print("Media del total de IPs que se han detectado: ", ipsAverage)

''' DESVIACI0N ESTANDAR (.std()) '''
dfIPs2 = pd.read_sql_query("SELECT COUNT(ips) FROM ips GROUP BY user_id", con)

ipsDesviation = float(dfIPs2.std())
print("Desviacion del total de IPs que se han detectado: ", ipsDesviation)


''' <--- Media y desviacion estandar del numero de emails recibidos ---> '''

''' MEDIA (.mean()) '''
dfEmailTotales = pd.read_sql_query("SELECT totalEmails FROM users GROUP BY username", con)
emailsAverage = float(dfEmailTotales.mean())
print("Media del numero de emails recibidos: ", emailsAverage)

''' DESVIACI0N ESTANDAR (.std()) '''
emailDesviation = float(dfEmailTotales.std())
print("Desviacion estandar del numero de emails recibidos: ", emailDesviation)


''' <--- Valor minimo y valor maximo del total de fechas que se ha iniciado sesion ---> '''

''' MIN (.min()) '''
datesMin = int(dfDates.min())
print("Valor minimo del total de fechas que se ha iniciado sesion: ", datesMin)

''' MAX (.max()) '''
datesMax = int(dfDates.max())
print("Valor maximo del total de fechas que se ha iniciado sesion: ", datesMax)


''' <--- Valor mınimo y valor maximo del numero de emails recibidos ---> '''

''' MIN (.min()) '''
emailsMin = int(dfEmailTotales.min())
print("Valor minimo del numero de email recibidos: ", emailsMin)

''' MAX (.max()) '''
emailsMax = int(dfEmailTotales.max())
print("Valor maximo del numero de email recibidos: ", emailsMax)
