import pymongo as pymongo
import logging


class MongoDbWriter:
    def write(spark, db_name, tbl_name, db_conf, df, id_column):
        from urllib.parse import quote_plus
        username = quote_plus(db_conf['DB_USER'])
        password = quote_plus(db_conf['DB_PASS'])
        client = pymongo.MongoClient(
            "mongodb+srv://" + username + ":" + password + "@ihubcluster.rxkoa.mongodb.net/?retryWrites=true&w=majority")
        db = client[db_name]
        collection = db[tbl_name]
        pandasDF = df.toPandas()
        for index, row1 in pandasDF.iterrows():
            row = row1.to_dict()
            row['_id'] = row[id_column]
            collection.insert_one(row)
        logging.info("Data loaded into MongoDB target table:" + db_name + "." + tbl_name)
        print("Data loaded into MongoDB target table:" + db_name + "." + tbl_name)
