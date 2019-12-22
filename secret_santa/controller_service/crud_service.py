###
# This is a base class for CRUD operations (CREATE, RETRIVE, UPDATE, DELETE)
from secret_santa.repository import Repository
from secret_santa.response import SuccessResponse,\
    ErrorException, ErrorResponse, Response
from abc import abstractmethod
import traceback


class CRUDService():
    def __init__(self, table):
        self.table = table
        self.repo = Repository(table)

    def create(self, json_input):
        try:
            model = self.get_table_model(json_input)
            model = self.repo.create_and_return(model)
            if model is None:
                raise ErrorException(
                    "Failed to create entry in table: {table_name}"
                    .format(table_name=self.table.__tablename__), 500)
            response = SuccessResponse(
                "Entry created in table: {table_name}"
                .format(table_name=self.table.__tablename__), 201)
        except ErrorException as e:
            response = ErrorResponse(e.status_code, e.message)
        except Exception:
            traceback.print_exc()
            response = ErrorResponse(500, "Unknown Error")
        return response

    def update(self, json_input, id):
        try:
            current_model = self.repo.retrieve_by_id(id)
            if(current_model is None):
                raise ErrorException(
                    "Entry with id {id} does not exist".format(id=id), 400)

            model = self._get_updated_table_model(json_input, current_model)
            model = self.repo.update_and_return(model)

            if model is None:
                raise ErrorException(
                    "Failed to update entry in table: {table_name}"
                    .format(table_name=self.table.__tablename__),
                    500
                )
            response = SuccessResponse(
                "Successfully updated entry in table {table_name}"
                .format(table_name=self.table.__tablename__))
            return response
        except ErrorException as e:
            response = ErrorResponse(e.status_code, e.message)
        except Exception:
            traceback.print_exc()
            response = ErrorResponse(500, "Unknown error")

        return response

    def delete(self, id):
        try:
            self.repo.delete_by_id(id)
            response = SuccessResponse(
                "Successfully deleted entry in table {table_name}"
                .format(table_name=self.table.__tablename__))
            return response
        except ErrorException as e:
            response = ErrorResponse(e.status_code, e.message)
        except Exception:
            traceback.print_exc()
            response = ErrorResponse(500, "Unknown error")
        return response

    def retrieve_all(self):
        models = self.repo.retrieve_all()
        return self._retrieve_multiple(models)

    def retrieve_by_id(self, id):
        try:
            model = self.repo.retrieve_by_id(id)
            model_object = self.get_model_json_object(model)
            response = Response(200, model_object)
        except ErrorException as e:
            response = ErrorResponse(e.status_code, e.message)
        except Exception:
            traceback.print_exc()
            response = ErrorResponse(500, "Unknown error")

        return response

    def _retrieve_multiple(self, models):
        try:
            model_objects = list(map(lambda x: self.get_model_json_object(x),
                                     models))
            response = Response(200, model_objects)
        except ErrorException as e:
            response = ErrorResponse(e.status_code, e.message)
        except Exception:
            traceback.print_exc()
            response = ErrorResponse(500, "Unknown error")

        return response

    @abstractmethod 
    def get_table_model(self, json_input):
        pass 

    @abstractmethod
    def get_model_json_object(self, model):
        pass
    ###
    # override in child class if the json_input key's and values are not
    # exactly the same as the table model or if you don't want to be able to
    # change everyting in the entry
    ###

    def _get_updated_table_model(self, json_input, current_model):
        model = current_model
        for key, value in model.__dict__.items():
            if(key in json_input.keys()):
                model.__dict__[key] = json_input.get(key)
        return model
