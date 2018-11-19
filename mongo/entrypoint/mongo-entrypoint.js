var db = connect("mongodb://localhost/admin");

db = db.getSiblingDB("supermamas");

db.createUser(
    {
        user: "web",
        pwd: "web",
        roles: [ { role: "readWrite", db: "supermamas" } ]
    }
)
