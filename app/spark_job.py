import os
from pyspark.sql import SparkSession # similar pandas pero manera ejecucion lazy

def main() -> None:
    
    spark = (
        SparkSession.builder.appName("Appto_SnowFlake").getOrCreate()
    )
     
     # Read postgres data   
    jdbc_url = os.getenv("POSTGRES_URL")
     
    connection_properties = {
        "user": os.getenv("POSTGRES_USER"),
        "password": os.getenv("POSTGRES_PASSWORD"),
        "driver": "org.postgresql.Driver"
     }
    
    df = (
        spark.read.jdbc(
            url = jdbc_url,
            table="user", 
            properties=connection_properties
                        
    )
    )
    
    print("Data Extracted from Appliaction")
    df.show() # como un head
    
     # Write data to snowflake
     
    sfOptions = {
        "sfURL":f"{os.get("SNOWFLAKE_ACCOUNT")}.snowflakecomputing.com",
        "sfUser": os.getenv("SNOWFLAKE_USER"),
        "sfPassword": os.getenv("SNOWFLAKE_PASSWORD"),
        "sfDatabase": os.getenv("SNOWFLAKE_DATABASE"),
        "sfSchema":os.getenv("SNOWFLAKE_SCHEMA"),
        "sfWarehouse": os.getenv("SNOWFLAKE_WAREHOUSE")
    }
    
    (
        df.
        write.
        format("snowflake")
        .options(**sfOptions)
        .option("dbtable", "users")
        .mode("overwrite")
        .save()
    )
     
    return None

if __name__ == "__main__":
    main()