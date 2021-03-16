name = "20211603_reserved"
dependencies = []


def upgrade(db):
    db.arm.update_many({'reserved': {'$exists': False}}, {'$set': {'reserved': 0}})


def downgrade(db):
    db.arm.update_many({}, {'$unset': 'reserved'})
