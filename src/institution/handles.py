from src import app
from .service import InstitutionService
from .dtos_mapper import InstitutionMapper
from flask import request, Flask, jsonify
from src.core.api_errors import ApplicationInconsistencyError, InputValidationError


def build(app: Flask, service: InstitutionService, mapper: InstitutionMapper):
    @app.route('/institutions/direction', methods=['GET'])
    def institution_get_direction():
        """
        This the endpoint return all of institutions with a specific structure to map its direction to link
        ---
        tags:
          - Institution EndPoints
        definitions:
            InstitutionDirectionReadDto:
                type: object
                properties:
                    id:
                        type: integer
                    name:
                        type: string
                        description: It's a abbreviator of institution's name
                    direction:
                        type: string
                        default: It doesnt have description yet
                        description: It can be the default value or a link compose by https://www.google.com/maps/search/ + entity_db.direction
        responses:
          500:
            description: There should be a connection database problem
          200:
            description: It's a success response
            schema:
                properties:
                    message:
                         type: string
                         default: success
                    count:
                         type: integer
                         description: Number of results
                    data:
                         type: array
                         items:
                             $ref: '#/definitions/InstitutionDirectionReadDto'
        """

        results = service.get_all()
        results = [mapper.entity_to_direction_view(e) for e in results]
        return {"message": "success", "count": len(results), "data": results}

    @app.route('/institution', methods=['POST'])
    def institution_post():
        """
        This the endpoint create an institution
        ---
        tags:
            - Institution EndPoints
        parameters:
            -   name: _id
                in: path
                type: string
                required: true
            -   name: body
                in: body
                required: true
                schema:
                    id: InstitutionCreateDto
                    required:
                        - name
                    properties:
                        name:
                            type: string
                            description: institution's name.
                            default: "Inti Inc."
                        description:
                            type: string
                        direction:
                            type: string
        responses:
          500:
            description: There should be a connection database problem
          400:
            description: You should read the response, because this error can be for the type, structure or rules of endpoint's input 
          200:
            description: It's a success response
            schema:
                properties:
                    message:
                        type: string
                        default: success
                    entity_id:
                        type: integer
        """
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

    @app.route('/institution', methods=['GET'])
    def institution_get():
        """
        This the endpoint return all of institutions
        ---
        tags:
          - Institution EndPoints
        definitions:

            InstitutionSummaryDto:
                type: object
                properties:
                    id:
                        type: integer
                    name:
                        type: string
                        description: institution's name
                    direction:
                        type: string
                        default: It doesnt have description yet
                    description:
                        type: string
                        default: It doesnt have description yet    

        responses:
          500:
            description: There should be a connection database problem
          200:
            description: It's a success response
            schema:
                properties:
                    message:
                         type: string
                         default: success
                    count:
                         type: integer
                         description: Number of results
                    data:
                         type: array
                         items:
                             $ref: '#/definitions/InstitutionReadDto'
        """

        results = service.get_all()
        results = [mapper.entity_to_summary(e) for e in results]
        return {"message": "success", "count": len(results), "data": results}

    @app.route('/institution/<_id>', methods=['GET'])
    def institution_get_id(_id):
        """
        This the endpoint return an institutions
        ---
        tags:
            - Institution EndPoints
        parameters:
            -   name: _id
                in: path
                type: string
                required: true
        definitions:
            InstitutionProjectReadDto:
                type: object
                properties:
                    id:
                        type: integer
                    name:
                        type: string
                        description: project's name
                    description:
                        type: string
                    start_date:
                        type: date
                        description: date when project start  
                    end_date:
                        type: date
                        description: date when project end
                    main_user:
                        type: object
                        properties:
                            id:
                                type: integer
                            name:
                                type: string
                            last_name:
                                type: string
                            rut:
                                type: string
                            office:
                                type: string
                                description: user's company position   
                            age:
                                type: integer

            InstitutionReadDto:
                type: object
                properties:
                    id:
                        type: integer
                    name:
                        type: string
                        description: institution's name
                    direction:
                        type: string
                        default: It doesnt have description yet
                    description:
                        type: string
                        default: It doesnt have description yet    
                    created_at:
                        type: date
                        description: time when entity was created  
                    updated_at_at:
                        type: date
                        description: time when entity was updated
                    projects:
                        type: array
                        items:
                            $ref: '#/definitions/InstitutionProjectReadDto'
        responses:
          500:
            description: There should be a connection database problem
          200:
            description: It's a success response
            schema:
                properties:
                    message:
                         type: string
                         default: success
                    entity:
                        $ref: '#/definitions/InstitutionReadDto'
        """
        try:
            entity = service.get_by_id(_id)
        except ApplicationInconsistencyError as e:
            return e.message, 404
        return {"message": "success", "entity": mapper.entity_to_details(entity)}

    @app.route('/institution/<_id>', methods=['PUT'])
    def institution_put(_id):
        """
        This the endpoint update an institution
        ---
        tags:
            - Institution EndPoints
        parameters:
            -   name: _id
                in: path
                type: string
                required: true
            -   name: body
                in: body
                required: true
                schema:
                    id: InstitutionUpdateDto
                    properties:
                        name:
                            type: string
                            description: institution's name.
                            default: "Inti Inc."
                        description:
                            type: string
                        direction:
                            type: string
        responses:
          500:
            description: There should be a connection database problem
          400:
            description: You should read the response, because this error can be for the type, structure or rules of endpoint's input 
          200:
            description: It's a success response
            schema:
                properties:
                    message:
                         type: string
                         default: success
        """
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

    @app.route('/institution/<_id>', methods=['DELETE'])
    def institution_delete(_id):
        """
        This the endpoint remove an institution
        ---
        tags:
            - Institution EndPoints
        parameters:
            -   name: _id
                in: path
                type: string
                required: true
        responses:
          500:
            description: There should be a connection database problem
          200:
            description: It's a success response
            schema:
                properties:
                    message:
                         type: string
                         default: success
        """

        _ = service.delete(_id)
        return {"message": "success"}
