import mysql.connector
from mysql.connector import Error
import os

class DatabaseConfig:
    """Database configuration for XAMPP MySQL connection"""
    
    # XAMPP MySQL default settings
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''  # Default XAMPP MySQL has no password
    MYSQL_DATABASE = 'iclinic_db'
    
    @staticmethod
    def get_connection():
        """Get MySQL database connection"""
        try:
            connection = mysql.connector.connect(
                host=DatabaseConfig.MYSQL_HOST,
                port=DatabaseConfig.MYSQL_PORT,
                user=DatabaseConfig.MYSQL_USER,
                password=DatabaseConfig.MYSQL_PASSWORD,
                database=DatabaseConfig.MYSQL_DATABASE,
                autocommit=True
            )
            return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    @staticmethod
    def create_database():
        """Create the database if it doesn't exist"""
        try:
            # Connect without specifying database
            connection = mysql.connector.connect(
                host=DatabaseConfig.MYSQL_HOST,
                port=DatabaseConfig.MYSQL_PORT,
                user=DatabaseConfig.MYSQL_USER,
                password=DatabaseConfig.MYSQL_PASSWORD
            )
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
