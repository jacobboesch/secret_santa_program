###
# This is a base class for CRUD operations (CREATE, RETRIVE, UPDATE, DELETE)
from secret_santa.repository import Repository
from secret_santa.response import SuccessResponse,\
    ErrorException, ErrorResponse, Response
from abc import abstractmethod
import traceback


class CRUDService():
    def __init__(self, table, input_object_class):
        self.table = table
        self.repo = Repository(table)
        self.input_object_class = input_object_class

    def create(self, json_input):
        try:
            input_object = self._get_input_object(json_input)
            model = self.get_table_model(input_object)
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
    ###
    # TODO change this method so that it only needs the fields that are
    # to be updated instead of needing everything
    ###

    def update(self, json_input, id):
        try:
            input_object = self._get_input_object(json_input)
            model = self.get_table_model(input_object)
            model.id = id
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

    def _get_input_object(self, json_input):
        input_object = self.input_object_class()
        input_object.init_from_json(json_input)

        return input_object

    def retrieve_all(self):
        models = self.repo.retrieve_all()

        return self._retrieve_multiple(models)

    def retrieve_by_id(self, id):
        try:
            model = self.repo.retrieve_by_id(id)
            model_object = self.get_model_json_object(model)
            output_data = model_object
            response = Response(200, output_data)
        except ErrorException as e:
            response = ErrorResponse(e.status_code, e.message)
        except Exception:
            traceback.print_exc()
            response = ErrorResponse(500, "Unknown error")

        return response

    def _retrieve_multiple(self, models):
        try:
            table_name = self.table.__tablename__
            model_objects = list(map(lambda x: self.get_model_json_object(x),
                                     models))
            output_data = {table_name: model_objects}
            response = Response(200, output_data)
        except ErrorException as e:
            response = ErrorResponse(e.status_code, e.message)
        except Exception:
            traceback.print_exc()
            response = ErrorResponse(500, "Unknown error")

        return response

    @abstractmethod
    def get_table_model(self, input_object):
        pass

    @abstractmethod
    def get_model_json_object(self, model):
        pass
