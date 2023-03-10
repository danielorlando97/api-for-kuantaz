from src import app
from .service import ProjectService
from .dtos_mapper import ProjectMapper
from flask import request, Flask, jsonify
from src.core.api_errors import ApplicationInconsistencyError, InputValidationError, ApplicationValidationError


def build(app: Flask, service: ProjectService, mapper: ProjectMapper):
    @app.route('/projects/durations', methods=['GET'])
    def project_durations():
        """
        This the endpoint return all of projects with a specific structure 
        ---
        tags:
            - Project EndPoints
        definitions:
            ProjectDurationReadDto:
                type: object
                properties:
                    id:
                        type: integer
                    name:
                        type: string
                    days_to_release:
                        type: integer
                        description: Days number to the project's end 
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
                             $ref: '#/definitions/ProjectDurationReadDto'
        """

        results = service.get_all()
        results = [mapper.entity_to_durations(e) for e in results]
        return {"message": "success", "count": len(results), "data": results}

    @app.route('/project', methods=['GET'])
    def project_get():
        """
        This the endpoint return all of projects
        ---
        tags:
            - Project EndPoints
        definitions:
            ProjectSummaryReadDto:
                type: object
                properties:
                    id:
                        type: integer
                    name:
                        type: string
                    description:
                        type: string
                        default: It doesnt have description yet 
                    start_date:
                        type: date
                        description: date when project start  
                    end_date:
                        type: date
                        description: date when project end
                    days_to_release:
                        type: integer
                        description: Days number to the project's end 
                    institution:
                        type: object
                        properties:
                            id:
                                type: integer
                            name:
                                type: string
                            description:
                                type: string
                            direction:
                                type: string
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
        results = [mapper.entity_to_summary(e) for e in results]
        return {"message": "success", "count": len(results), "data": results}

    @app.route('/project', methods=['POST'])
    def project_post():
        """
        This the endpoint create an project
        ---
        tags:
            - Project EndPoints
        parameters:
            -   name: _id
                in: path
                type: string
                required: true
            -   name: body
                in: body
                required: true
                schema:
                    id: ProjectCreateDto
                    required:
                        - name
                        - start_date
                        - end_date
                        - main_user_id
                        - institution_id
                    properties:
                        name:
                            type: string
                            description: project's name.
                            default: "IA"
                        description:
                            type: string
                        start_date:
                            type: date
                            description: date when project start  
                        end_date:
                            type: date
                            description: date when project end
                        main_user_id: 
                            type: integer
                        institution_id: 
                            type: integer
        responses:
          500:
            description: There should be a connection database problem
          400:
            description: You should read the response, because this error can be for the type, structure or rules of endpoint's input 
          401:
            description: When main_user_id or institution_id aren't valid ids
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
            except ApplicationInconsistencyError as e:
                return e.message, 404

            return {"message": "success", 'entity_id': entity.id}
        else:
            return "The request payload is not in JSON format", 400

    @app.route('/project/<_id>', methods=['GET'])
    def project_get_id(_id):
        """
        This the endpoint return all of projects
        ---
        tags:
            - Project EndPoints
        definitions:
            ProjectDetailsReadDto:
                type: object
                properties:
                    id:
                        type: integer
                    name:
                        type: string
                    start_date:
                        type: date
                        description: date when project start  
                    end_date:
                        type: date
                        description: date when project end
                    created_at:
                        type: date
                        description: time when entity was created  
                    updated_at_at:
                        type: date
                        description: time when entity was updated

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

        try:
            entity = service.get_by_id(_id)
        except ApplicationInconsistencyError as e:
            return e.message, 404
        return {"message": "success", "entity": mapper.entity_to_details(entity)}

    @app.route('/project/<_id>', methods=['PUT'])
    def project_put(_id):
        """
        This the endpoint update an project
        ---
        tags:
            - Project EndPoints
        parameters:
            -   name: _id
                in: path
                type: string
                required: true
            -   name: body
                in: body
                required: true
                schema:
                    id: ProjectUpdateDto
                    properties:
                        name:
                            type: string
                            description: project's name.
                            default: "IA"
                        description:
                            type: string
                        start_date:
                            type: date
                            description: date when project start  
                        end_date:
                            type: date
                            description: date when project end
                        main_user_id: 
                            type: integer
                        institution_id: 
                            type: integer
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
            except ApplicationValidationError as e:
                return e.message, 400
            except ApplicationInconsistencyError as e:
                return e.message, 404

            return {"message": "success"}
        else:
            return "The request payload is not in JSON format", 400

    @app.route('/project/<_id>', methods=['GET', 'PUT', 'DELETE'])
    def project_delete(_id):
        """
        This the endpoint remove an project
        ---
        tags:
            - Project EndPoints
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
