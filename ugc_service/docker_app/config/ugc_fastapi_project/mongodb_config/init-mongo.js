db.createUser(
    {
        user: "ugc_admin",
        pwd: "ugc_admin",
        roles: [
            {
                role: "readWrite",
                db: "ugc"
            }
        ]
    }
);

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
                    user_id: {
                        bsonType: "string",
                        description: "must be a string"
                    },
                    film_id: {
                        bsonType: "string",
                        description: "must be a string"
                    },
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

db.film_rating.createIndex(
    {film_id: 1, user_id: 1}, {unique: true}
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
                    user_id: {
                        bsonType: "string",
                        description: "must be a string"
                    },
                    film_id: {
                        bsonType: "string",
                        description: "must be a string"
                    },
                    review: {
                        bsonType: "string",
                        description: "must be a string",
                    }
                }
            }
        }
    }
);

db.film_review.createIndex(
    {film_id: 1, user_id: 1}, {unique: true}
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
                required: ["user_id", "bookmark_film_id"],
                properties: {
                    user_id: {
                        bsonType: "string",
                        description: "must be a string"
                    },
                    bookmark_film_id: {
                        bsonType: "string",
                        description: "must be a string"
                    }
                }
            }
        }
    }
);

db.user_bookmark.createIndex(
    {user_id: 1, bookmark_film_id: 1}, {unique: true}
);