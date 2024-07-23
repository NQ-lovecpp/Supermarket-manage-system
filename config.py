# import os

# class Config:
#     # 其他配置...

#     SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://LAPTOP-EUN5VQCN/小型超市管理系统?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'

#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
#     # 其他配置...


import os

class Config:
    # 其他配置...

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://chen:Cydia4384!@139.196.238.17/SupermarketDB'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    # 其他配置...
