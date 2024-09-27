import aiomysql
from dotenv import load_dotenv
import os
 
load_dotenv()  # Carga las variables de entorno desde .env

async def get_db():
    # conn = await aiomysql.connect(host=os.environ.get('MYSQL_URL'),port=os.environ.get('MYSQL_PORT'),user=os.environ.get('MYSQL_USER'), 
    #                              password=os.environ.get('MYSQL_PASSWORD'),
    #                              db=os.environ.get('MYSQL_DATABASE'))
    
    
    conn = await aiomysql.connect(host=os.environ.get('MYSQL_URL'),port=int(os.environ.get('MYSQL_PORT')), 
                                  user=os.environ.get('MYSQL_USER'), password=os.environ.get('MYSQL_PASSWORD'),db=os.environ.get('MYSQL_DATABASE'),)
    
    return conn 

