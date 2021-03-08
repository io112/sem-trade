from datetime import datetime


class Session:
    def __init__(self):
        self.user = ''
        self._id = ''
        self.last_modified = datetime.utcnow()
        self.data = {}

    def add_data(self, data):
        self.data.update(data)
        self.last_modified = datetime.utcnow()

    def set_data(self, key, val):
        self.data[key] = val
        self.last_modified = datetime.utcnow()

    def remove_data(self, key):
        del self.data[key]
        self.last_modified = datetime.utcnow()

    def to_dict(self):
        return {"_id": self._id,
                "user": self.user,
                "data": self.data,
                "last_modified": self.last_modified,
                }

    def get_id(self):
        return self._id

    def set_id(self, sid):
        if self._id != '':
            raise Exception("sid is read-only")
        else:
            self._id = sid

    def create_from_struct(self, struct):
        self.set_id(struct["_id"])
        self.data = struct["data"]
        self.last_modified = struct["last_modified"]
        self.user = struct["user"]
