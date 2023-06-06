sh.addShard("mongors1/mongors1n1");
sh.addShard("mongors2/mongors2n1");

sh.enableSharding("ugc");

db = db.getSiblingDB('ugc');

db.createCollection(
    "film_rating",
    {
        clusteredIndex: {
            "key": { _id: 1 },
            "unique": true,
            "name": "stocks clustered key"
        },
        validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["user_id", "film_id", "rating"],
                properties: {
                    rating: {
                        bsonType: "int",
                        description: "can only be a integer",
                        minimum: 1,
                        maximum: 10
                    }
                }
            }
        }
    },
);

db.createCollection(
    "film_review",
    {
        clusteredIndex: {
            "key": { _id: 1 },
            "unique": true,
            "name": "stocks clustered key"
        },
        validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["user_id", "film_id", "review"],
                properties: {
                    review: {
                        bsonType: "string",
                        description: "must be a string",
                    }
                }
            }
        }
    }
);

db.createCollection(
    "user_bookmark",
    {
        clusteredIndex: {
            "key": { _id: 1 },
            "unique": true,
            "name": "stocks clustered key"
        },
        validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["user_id", "bookmark_film_id"]
            }
        }
    }
);

db.user_bookmark.createIndex(
    {user_id: 1, bookmark_film_id: 1}, {unique: true}
);

sh.shardCollection("ugc.film_rating", {"user_id": 1, "film_id": 1}, true);
sh.shardCollection("ugc.film_review", {"user_id": 1, "film_id": 1}, true);
sh.shardCollection("ugc.user_bookmark", {"user_id": 1});