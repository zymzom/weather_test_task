CREATE_WEATHER_TABLE = """
            CREATE TABLE open_weathers(
                id serial PRIMARY KEY,
                time timestamp,
                city_name text,
                temperature float,
                wind_speed float
            )
        """


EXIST_WEATHER_TABLE = """
        SELECT EXISTS(SELECT * FROM information_schema.tables where lower(table_name) = lower($1));
        """


INSERT_CITY = "INSERT INTO open_weathers(city_name, temperature, wind_speed, time) VALUES($1, $2, $3, $4)"

SELECT_CITY = "SELECT * FROM open_weathers WHERE city_name = $1 ORDER BY time DESC"