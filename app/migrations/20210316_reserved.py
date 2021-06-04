from mongodb_migrations.base import BaseMigration


class Migration(BaseMigration):
    def upgrade(self):
        for item in self.db.order.find():
            num = item['order_num']
            item['_number'] = int(num[3:])
            self.db.order.save(item)

    def downgrade(self):
        self.db.order.update_many({}, {'$unset': '_number'})
