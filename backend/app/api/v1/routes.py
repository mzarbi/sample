from ...common.broker_access import get_value


def register_routes(api):
    @api.route('/hello', methods=['GET'])
    def hello_world():
        """
        A Hello World Endpoint
        ---
        tags:
          - Test
        responses:
          200:
            description: A single hello world object
            schema:
              id: hello_world
              properties:
                message:
                  type: string
                  default: Hello, World!
        """
        return {'message': get_value()}