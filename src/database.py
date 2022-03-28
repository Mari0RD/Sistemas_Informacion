
import sqlite3
import json

con = sqlite3.connect('database.db')
c = con.cursor()

def initDatabase():
    fUser = open('users.json')
    fLegal = open('legal.json')
    userFile = json.load(fUser)
    legalFile = json.load(fLegal)


    """ BORRADO DE LAS TABLAS EN CASO DE QUE EXISTAN """
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("DROP TABLE IF EXISTS dates")
    c.execute("DROP TABLE IF EXISTS ips")
    c.execute("DROP TABLE IF EXISTS legal")

    """ CREACION DE LAS TABLAS """
    c.execute("CREATE TABLE users (username text, phone integer, password text, province text, permissions bool,"
              "totalEmails integer, phishingEmails integer, clickedEmails integer, PRIMARY KEY (username))")

    c.execute("CREATE TABLE dates (user_id text, dates text, FOREIGN KEY (user_id) REFERENCES users(username))")

    c.execute("CREATE TABLE ips (user_id text, ips text, FOREIGN KEY (user_id) REFERENCES users(username))")

    c.execute("CREATE TABLE legal (url text, cookies integer, warning bool, dataProtection bool, creation integer, PRIMARY KEY (url))")

    """ GUARDAR CAMBIOS """
    con.commit()

    """ INSERCION EN LA TABLA USERS """
    for user in userFile['usuarios']:
        for userData in user.keys():
            phone = user[userData]['telefono']
            password = user[userData]['contrasena']
            province = user[userData]['provincia']
            permissions = user[userData]['permisos']
            totalEmails = user[userData]['emails']['total']
            phishingEmails = user[userData]['emails']['phishing']
            clickedEmails = user[userData]['emails']['cliclados']

            """ELIMINAR LOS VALORES A NONE"""
            if phone =='None' and province !='None':
                c.execute("INSERT INTO users (username, phone, password, province, permissions,"
                          "totalEmails, phishingEmails, clickedEmails) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                          (userData, '0', password, province, permissions, totalEmails, phishingEmails, clickedEmails))

            elif province =='None' and phone !='None':
                c.execute("INSERT INTO users (username, phone, password, province, permissions,"
                          "totalEmails, phishingEmails, clickedEmails) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                          (userData, phone, password, '0', permissions, totalEmails, phishingEmails, clickedEmails))

            elif phone =='None' and province =='None':
                c.execute("INSERT INTO users (username, phone, password, province, permissions,"
                          "totalEmails, phishingEmails, clickedEmails) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                          (userData, '0', password, '0', permissions, totalEmails, phishingEmails, clickedEmails))

            else:
                c.execute("INSERT INTO users (username, phone, password, province, permissions," 
                      "totalEmails, phishingEmails, clickedEmails) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (userData, phone, password, province, permissions, totalEmails, phishingEmails, clickedEmails))

    """ INSERCION EN LA TABLA DATES """
    for user in userFile['usuarios']:
        for userData in user.keys():
            for date in user[userData]['fechas']:

                c.execute("INSERT INTO dates (user_id, dates) VALUES (?, ?)",(userData, date))

    """ INSERCION EN LA TABLA IPS """
    for user in userFile['usuarios']:
        for userData in user.keys():
            for ips in user[userData]['ips']:

                # Le quitamos porque tiene valores a none
                if userData != 'jesus.duarte':
                    c.execute("INSERT INTO ips (user_id, ips) VALUES (?, ?)", (userData, ips))


    """ INSERCION EN LA TABLA LEGAL """
    for url in legalFile['legal']:
        for urlData in url.keys():
            cookies = url[urlData]['cookies']
            warning = url[urlData]['aviso']
            dataProtection = url[urlData]['proteccion_de_datos']
            creation = url[urlData]['creacion']

            c.execute("INSERT INTO legal (url, cookies, warning, dataProtection, creation) VALUES (?,?, ?, ?, ?)",
                      (urlData, cookies, warning, dataProtection, creation))


    """ GUARDAR CAMBIOS """
    con.commit()
    con.close()

if __name__ == '__main__':
    initDatabase()