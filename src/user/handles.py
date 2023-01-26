from src import app
from .service import UserService
from .dtos_mapper import UserMapper
from flask import request, Flask, jsonify
from src.core.api_errors import InputValidationError


def build(app: Flask, service: UserService, mapper: UserMapper):
    @app.route('/user', methods=['GET'])
    def user_get():
        """
        This the endpoint return all of users
        ---
        tags:
          - User EndPoints
        definitions:
            UserProjectReadDto:
                type: object
                properties:
                    id:
                        type: integer
                    name:
                        type: string
                    description:
                        type: string
                    start_date:
                        type: date
                        description: date when project start
                    end_date:
                        type: date
                        description: date when project end
                    institution_id:
                        type: integer
                        description: project institutions id

            UserSummaryDto:
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
                        description: This field only apparent when the query has its filter
                    office:
                        type: string
                        description: user's company position
                    age:
                        type: integer
                    projects:
                        type: array
                        description: This field only apparent when the query has the rut filter
                        items:
                            $ref: '#/definitions/UserProjectReadDto'

        responses:
          500:
            description: There should be a connection database problem
          200:
            description: It's a success response. You should read the response description, because son field are conditionals
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
                             $ref: '#/definitions/UserSummaryDto'
        """

        rut = request.args.get('rut')
        if rut:
            results = service.find_by_rut(rut)
            results = [mapper.entity_to_rut_view(e) for e in results]
        else:
            results = service.get_all()
            results = [mapper.entity_to_summary(e) for e in results]

        return {"message": "success", "count": len(results), "data": results}

    @app.route('/user', methods=['POST'])
    def user_post():
        """
        This the endpoint create an user
        ---
        tags:
          - User EndPoints
        parameters:
            -   name: _id
                in: path
                type: string
                required: true
            -   name: body
                in: body
                required: true
                schema:
                    id: UserCreateDto
                    required:
                        - name
                        - last_name
                        - rut
                        - office
                        - birthday
                    properties:
                        name:
                            type: string
                            default: "Tomas"
                        last_name:
                            type: string
                            default: "Dos"
                        rut:
                            type: string
                            default: "1234567890"
                        office:
                            type: string
                            description: user's company position
                            default: "developer"
                        birthday:
                            type: date
                            default: "1997-04-01T0:0:0.0"
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

    @app.route('/user/<_id>', methods=['GET'])
    def user_get_by(_id):
        """
        This the endpoint return an user
        ---
        tags:
          - User EndPoints
        definitions:

            UserDetailsDto:
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
                    birthday:
                        type: date
                    created_at:
                        type: date
                        description: time when entity was created
                    updated_at_at:
                        type: date
                        description: time when entity was updated
                    projects:
                        type: array
                        items:
                            $ref: '#/definitions/UserProjectReadDto'

        responses:
          500:
            description: There should be a connection database problem
          200:
            description: It's a success response. You should read the response description, because son field are conditionals
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
                             $ref: '#/definitions/UserDetailsDto'
        """

        entity = service.get_by_id(_id)
        return {"message": "success", "entity": mapper.entity_to_details(entity)}

    @app.route('/user/<_id>', methods=['PUT'])
    def user_put(_id):
        """
        This the endpoint update an user
        ---
        tags:
          - User EndPoints
        parameters:
            -   name: _id
                in: path
                type: string
                required: true
            -   name: body
                in: body
                required: true
                schema:
                    id: UserUpdateDto
                    properties:
                        name:
                            type: string
                            default: "Tomas"
                        last_name:
                            type: string
                            default: "Dos"
                        rut:
                            type: string
                            default: "1234567890"
                        office:
                            type: string
                            description: user's company position
                            default: "developer"
                        birthday:
                            type: date
                            default: "1997-04-01T0:0:0.0"
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

    @app.route('/user/<_id>', methods=['DELETE'])
    def user_delete(_id):
        """
        This the endpoint remove an user
        ---
        tags:
          - User EndPoints
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
