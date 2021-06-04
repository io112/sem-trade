from mongodb_migrations.base import BaseMigration


class Migration(BaseMigration):
    def upgrade(self):
        for item in self.db.fiting.find():
            if item['parameters'].get('angle') is None:
                item['parameters']['angle'] = 'нет'
                self.db.fiting.save(item)

    def downgrade(self):
        self.db.order.update_many({}, {'$unset': 'parameters.angle'})
