from src import app
from .service import InstitutionService
from .dtos_mapper import InstitutionMapper
from flask import request, Flask, jsonify
from src.core.api_errors import InputValidationError


def build(app: Flask, service: InstitutionService, mapper: InstitutionMapper):
    @app.route('/institutions/direction', methods=['GET'])
    def handler_direction_institution():
        if request.method == 'GET':
            results = service.get_all()
            results = [mapper.entity_to_direction_view(e) for e in results]
            return {"message": "success", "count": len(results), "data": results}

    @app.route('/institution', methods=['POST', 'GET'])
    def handler_institutions():
        if request.method == 'POST':
            if request.is_json:
                body = request.get_json()

                try:
                    body = mapper.body_to_create_dto(body)
                    entity = service.create(body)
                except InputValidationError as e:
                    return jsonify(e.message), 400

                return {"message": "success", 'entity_id': entity.id}
            else:
                return "The request payload is not in JSON format", 400

        if request.method == 'GET':
            results = service.get_all()
            results = [mapper.entity_to_summary(e) for e in results]
            return {"message": "success", "count": len(results), "data": results}

    @app.route('/institution/<_id>', methods=['GET', 'PUT', 'DELETE'])
    def handler_institution(_id):

        if request.method == 'GET':
            entity = service.get_by_id(_id)
            return {"message": "success", "entity": mapper.entity_to_details(entity)}

        elif request.method == 'PUT':
            if request.is_json:
                body = request.get_json()

                try:
                    body = mapper.body_to_update_dto(body)
                    _ = service.update(_id, body)
                except InputValidationError as e:
                    return jsonify(e.message), 400

                return {"message": "success"}
            else:
                return "The request payload is not in JSON format", 400

        elif request.method == 'DELETE':
            _ = service.delete(_id)
            return {"message": "success"}
