sh.addShard("mongors1/mongors1n1");
sh.addShard("mongors2/mongors2n1");

sh.enableSharding("profiles");

db = db.getSiblingDB('profiles');

db.createCollection(
    "user_profile",
    {
        clusteredIndex: {
            "key": { _id: 1 },
            "unique": true,
            "name": "stocks clustered key"
        },
        validator: {
            $jsonSchema: {
                bsonType: "object",
                required: ["user_id", "purchased_films"],
                properties: {
                    user_id: {
                        bsonType: "string",
                        description: "must be a string and is required"
                    },
                    purchased_films: {
                        bsonType: [ "array" ],
                        items: {
                            bsonType: "string",
                        },
                        description: "must be a array of objects containing strings"
                    }
                }
            }
        }
    },
);

sh.shardCollection("profiles.user_profile", {"user_id": 1}, true);