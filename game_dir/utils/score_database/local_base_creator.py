from pymongo import MongoClient
from datetime import datetime
import json
from typing import List, Dict


client = MongoClient("mongodb://localhost:27017/")
db = client["games"]


schema = {
    "bsonType": "object",
    "required": [
        "result",
        "winner",
        "game_type",
        "history",
        "time started",
        "time ended",
    ],
    "properties": {
        "result": {
            "bsonType": "string",
            "description": "must be a string and is required",
        },
        "winner": {
            "bsonType": "string",
            "description": "must be a string and is required",
        },
        "game_type": {
            "bsonType": "string",
            "description": "must be a string and is required",
        },
        "history": {
            "bsonType": "array",
            "items": {"bsonType": "string"},
            "description": "must be an array of strings and is required",
        },
        "player_color": {
            "bsonType": ["string", "null"],
            "description": "can be a string or null",
        },
        "engine elo": {
            "bsonType": ["int", "null"],
            "description": "can be an integer or null",
        },
        "time started": {
            "bsonType": "date",
            "description": "must be a date and is required",
        },
        "time ended": {
            "bsonType": "date",
            "description": "must be a date and is required",
        },
    },
}


def collection_remover(collection: str) -> None:
    """
    Drop the specified collection from the database.

    :param collection: Name of the collection to be dropped.
    :return: None
    """
    try:
        db.drop_collection(collection)
    except Exception as e:
        print(e)


def create_collection_with_schema(collection: str, schema: Dict) -> None:
    """
    Create a new collection with the specified schema.

    :param collection: Name of the collection to be created.
    :param schema: Schema definition for the collection.
    :return: None
    """
    try:
        db.create_collection(collection, validator={"$jsonSchema": schema})
    except Exception as e:
        print(e)


def base_cleaner(collection_name: str) -> None:
    """
    Remove all documents from the specified collection.

    :param collection: Name of the collection to be cleaned.
    :return: None
    """
    try:
        collection = db[collection_name]
        collection.delete_many({})
    except Exception as e:
        print(e)


def upload_existing(path: str, collection_name: str) -> None:
    """
    Upload existing game data from a JSON file to the specified collection.

    :param path: Path to the JSON file containing the game data.
    :param collection_name: Name of the collection to upload the data to.
    :return: None
    """
    try:
        collection = db[collection_name]
        with open(path, "r") as file:
            print("Reading file...")
            file_content = file.read()
            if not file_content.strip():
                print("File is empty.")
                return
            data = json.loads(file_content)
            print("Loaded JSON data:", data)
        for game in data:
            game["time started"] = datetime.strptime(
                game["time started"], "%Y-%m-%d %H:%M:%S"
            )
            game["time ended"] = datetime.strptime(
                game["time ended"], "%Y-%m-%d %H:%M:%S"
            )
            collection.insert_one(game)
        print("Data uploaded successfully.")
    except Exception as e:
        print("Error:", e)


def main() -> None:
    """
    Main function to set up the collection and upload existing data.

    :return: None
    """
    try:
        path = "game_dir/utils/past_games.json"
        collection_remover("games")
        create_collection_with_schema("games", schema)
        collection_name = "games"
        base_cleaner(collection_name)
        upload_existing(path, collection_name)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()


def upload_new(data: List[Dict]) -> None:
    """
    Upload new game data to the collection.

    :param data: List of dictionaries containing game data.
    :return: None
    """
    try:
        collection = db["games"]
        print("DATA:", data)
        game = data[-1]
        print("GAME:", game)
        game["time started"] = datetime.strptime(
            game["time started"], "%Y-%m-%d %H:%M:%S"
        )
        game["time ended"] = datetime.strptime(game["time ended"], "%Y-%m-%d %H:%M:%S")
        collection.insert_one(game)
        # print every game in the collection
        for game in collection.find():
            print("COLGAME\n", game)
    except Exception as e:
        print(e)
