import asyncpg
import logging

logging.basicConfig(filename='Logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def insert_data(input_text, output_response, feedback):
    try:
        conn = await asyncpg.connect(
            database="SUMMARIZER",
            user="postgres",
            password="extension",
            host="localhost",
            port="5432"
        )

        sql = """INSERT INTO request_response (request, response, feedback)
                 VALUES ($1, $2, $3)"""

        #TODO: Get feedback from frontend
        await conn.execute(sql, input_text, output_response, feedback)
        await conn.close()

        logging.info("Data inserted into PostgreSQL")

    except (Exception, asyncpg.PostgresError) as error:
        logging.error("Error while connecting to PostgreSQL: %s", error)