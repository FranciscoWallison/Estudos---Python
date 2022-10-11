from flask_restx import Resource, fields, Namespace
from werkzeug.exceptions import BadRequest
from namespaces.util import token_required

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Namespace('testing'
# , authorizations=authorizations
)


sum_of_integer = api.model('sum', {
    "number1": fields.Integer('1'),
    "number2": fields.Integer('2')
})

hello_name = api.model('hello', {
    "name": fields.String('Shorya')
})


@api.route('/hello')
class HelloWorld(Resource):
    @api.doc(security='apikey')
    # @token_required
    def get(self):
        return {'hello': 'world'}

    @api.expect(hello_name)
    # @token_required
    def post(self):
        data = api.payload
        name = data['name']
        return {'hello': name}


@api.route('/sum')
class SumOfNumbers(Resource):
    @api.expect(sum_of_integer)
    # @token_required
    def post(self):
        try:
            data = api.payload
            number1 = data['number1']
            number2 = data['number2']
            sum = number1 + number2
            return {'sum': sum}
        except:
            raise BadRequest()