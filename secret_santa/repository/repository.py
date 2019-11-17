import secret_santa.database
import traceback
from secret_santa.response import ErrorException


class Repository():
    db_session = secret_santa.database.db_session

    def __init__(self, table):
        self.table = table

    def create(self, model):
        self.db_session.add(model)
        self.db_session.commit()

    def create_and_return(self, model):
        try:
            self.create(model)
            return model
        except Exception:
            traceback.print_exc()
        return None

    def retrieve_all(self):
        models = self.db_session.query(self.table).all()
        return models

    def retrieve_by_id(self, id):
        model = self.db_session.query(self.table) \
            .filter(self.table.id == id) \
            .first()
        return model

    def update(self, model):
        self.db_session.query(self.table) \
            .filter(self.table.id == model.id) \
            .update({
                column: getattr(model, column) for column in self.table
                                                                 .__table__
                                                                 .columns
                                                                 .keys()
            })
        self.db_session.commit()

    def update_and_return(self, model):
        self.update(model)
        return model

    def delete(self, model):
        self.db_session.delete(model)
        self.db_session.commit()

    def delete_by_id(self, model_id):
        try:
            model = self.retrieve_by_id(model_id)
            self.delete(model)
        except Exception:
            message = "Failed to delete entry in table: \
                    {table_name}, make sure the entry is not referenced"
            message = message.format(table_name=self.table.__tablename__)
            traceback.print_exc()
            raise ErrorException(message, 500)
