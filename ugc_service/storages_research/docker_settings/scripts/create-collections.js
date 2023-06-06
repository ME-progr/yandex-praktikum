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