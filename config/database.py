import mysql.connector
from mysql.connector import Error
import os
from urllib.parse import urlparse

class DatabaseConfig:
    """Database configuration for XAMPP MySQL connection"""
    
    # XAMPP MySQL default settings
    # Note: Railway MySQL plugin commonly provides MYSQLHOST/MYSQLPORT/MYSQLUSER/MYSQLPASSWORD/MYSQLDATABASE
    MYSQL_HOST = os.getenv('MYSQL_HOST') or os.getenv('MYSQLHOST') or 'localhost'
    MYSQL_PORT = int(os.getenv('MYSQL_PORT') or os.getenv('MYSQLPORT') or '3306')
    MYSQL_USER = os.getenv('MYSQL_USER') or os.getenv('MYSQLUSER') or 'root'
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD') or os.getenv('MYSQLPASSWORD') or ''
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE') or os.getenv('MYSQLDATABASE') or 'iclinic_db'

    @staticmethod
    def _parse_database_url():
        database_url = os.getenv('DATABASE_URL') or os.getenv('MYSQL_URL')
        if not database_url:
            return None

        parsed = urlparse(database_url)
        if parsed.scheme not in ('mysql', 'mysql+pymysql'):
            return None

        return {
            'host': parsed.hostname,
            'port': parsed.port or 3306,
            'user': parsed.username,
            'password': parsed.password,
            'database': (parsed.path or '').lstrip('/') or None,
        }

    @staticmethod
    def _get_connection_params(include_database: bool = True):
        url_cfg = DatabaseConfig._parse_database_url()
        if url_cfg:
            params = {
                'host': url_cfg['host'],
                'port': url_cfg['port'],
                'user': url_cfg['user'],
                'password': url_cfg['password'],
            }
            if include_database and url_cfg.get('database'):
                params['database'] = url_cfg['database']
            elif include_database:
                params['database'] = DatabaseConfig.MYSQL_DATABASE
            return params

        params = {
            'host': DatabaseConfig.MYSQL_HOST,
            'port': DatabaseConfig.MYSQL_PORT,
            'user': DatabaseConfig.MYSQL_USER,
            'password': DatabaseConfig.MYSQL_PASSWORD,
        }
        if include_database:
            params['database'] = DatabaseConfig.MYSQL_DATABASE
        return params
    
    @staticmethod
    def get_connection():
        """Get MySQL database connection"""
        try:
            connection = mysql.connector.connect(**DatabaseConfig._get_connection_params(include_database=True), autocommit=True)
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    @staticmethod
    def create_database():
        """Create the database if it doesn't exist"""
        try:
            # Connect without specifying database
            connection = mysql.connector.connect(**DatabaseConfig._get_connection_params(include_database=False))
            cursor = connection.cursor()
            
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DatabaseConfig.MYSQL_DATABASE}")
            cursor.execute(f"USE {DatabaseConfig.MYSQL_DATABASE}")
            
            print(f"Database '{DatabaseConfig.MYSQL_DATABASE}' created/selected successfully")
            
            cursor.close()
            connection.close()
            return True
            
        except Error as e:  
            print(f"Error creating database: {e}")
            return False
