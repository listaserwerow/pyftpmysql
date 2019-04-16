import os
import yaml
import pymysql

from mysql_ftpd import MysqlAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def main():
    if not os.path.exists("config.yml"):
        with open('config.yml', 'w+') as yaml_file:
            yaml.dump(dict(mysql=dict(
                host="localhost",
                port=3306,
                database="hosting",
                user="hosting",
                password="hosting"
            )), yaml_file)

    with open("config.yml", 'r') as yaml_file:
        config = yaml.full_load(yaml_file)

    database = pymysql.connect(**config["mysql"], charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
                               autocommit=True)
    cursor = database.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `ftp_server` (`id` INT AUTO_INCREMENT, `user` VARCHAR(32) NOT NULL, `password` VARCHAR(72) NOT NULL, `home` VARCHAR(255) NOT NULL, PRIMARY KEY (`id`), UNIQUE (`user`))")
    cursor.close()

    authorizer = MysqlAuthorizer(database)

    handler = FTPHandler
    handler.banner = "FTP is ready"
    handler.authorizer = authorizer
    server = FTPServer(('', 2121), handler)
    server.serve_forever()

    database.close()


if __name__ == '__main__':
    main()
