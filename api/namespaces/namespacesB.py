from flask_restx import Resource, fields, Namespace
from werkzeug.exceptions import BadRequest
import json
from namespaces.util import token_required


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}

api = Namespace('tasks'
# , authorizations=authorizations
)

add_tasks = api.model('tasks', {
    "title": fields.String('complete test cases'),
    "description": fields.String('tests cases for global project'),
    "done": fields.Boolean(False)
})


@api.route('/gettasks')
class Tasks(Resource):
    @api.doc(security='apikey')
    # @token_required
    def get(self):
        with open('api/data/tasks.json') as f:
            tasksList = json.load(f)
        return tasksList


@api.route('/addTasks')
class AddTasks(Resource):
    @api.doc(security='apikey')
    @api.expect(add_tasks)
    # @token_required
    def post(self):
        with open('api/data/tasks.json','r') as f:
            tasksList = json.load(f)
        data = api.payload
        title = data.get('title')
        description = data.get('description')
        done = data.get('done')
        task = {
            'id': tasksList['tasks'][-1]['id'] + 1,
            'title': title,
            'description': description,
            'done':done
        }
        tasksList['tasks'].append(task)
        with open('api/data/tasks.json', 'w') as fp:
            json.dump(tasksList, fp)

        return {'result': 'Task Added', 'success': True}


@api.route('/<int:task_id>')
class EditTasks(Resource):
    @api.doc(security='apikey')
    # @token_required
    def delete(self, task_id):
        with open('api/data/tasks.json','r') as f:
            tasksList = json.load(f)
        task = [task for task in tasksList['tasks'] if task['id'] == task_id]
        if len(task) == 0:
            raise BadRequest()
        tasksList['tasks'].remove(task[0])
        with open('api/data/tasks.json', 'w') as fp:
            json.dump(tasksList, fp)
        return {'result': 'Task Deleted', 'success': True}

    @api.expect(add_tasks)
    @api.doc(security='apikey')
    # @token_required
    def put(self, task_id):
        with open('api/data/tasks.json','r') as f:
            tasksList = json.load(f)
        if len(tasksList) == 0:
            return {"message": "no tasks created"}
        if not api.payload:
            raise BadRequest()
        if 'title' in api.payload and type(api.payload['title']) != str :
            raise BadRequest()
        if 'description' in api.payload and type(api.payload['description']) is not str:
            raise BadRequest()
        if 'done' in api.payload and type(api.payload['done']) is not bool:
            raise BadRequest()
        for task in tasksList['tasks']:
            if task['id'] == task_id:
                task['title'] = api.payload.get('title')
                task['description'] = api.payload.get('description')
                task['done'] = api.payload.get('done')
                with open('api/data/tasks.json', 'w') as fp:
                    json.dump(tasksList, fp)
                return {'result': 'Task updated', 'success': True}
            else:
                continue
        return {'message': "no such record found"}