"""
Implementing the API endpoints
"""

import os
import json
from flask import request, jsonify
from app import webserver
from app.data_ingestor import DataIngestor


# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """
    # Assuming the request contains JSON data
    # Process the received data
    # For demonstration purposes, just echoing back the received data
    # Sending back a JSON response
    """
    if request.method == 'POST':
        data = request.json
        print(f"got data in post {data}")
        response = {"message": "Received data successfully", "data": data}
        return jsonify(response)
    return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """
    Check if job_id is valid
    Check if job_id is done and return the result
       res = res_for(job_id)
       return jsonify({
           'status': 'done',
           'data': res
       })
    If not, return running status
    """
    print(f"JobID is {job_id}")
    if int(job_id) not in webserver.tasks_runner.get_ids:
        return jsonify({"status": "error", "reason": "Invalid job_id"})
    elif int(job_id) in webserver.tasks_runner.get_ids and os.path.exists(f"results/{job_id}.json"):
        with open(f"./results/{job_id}.json", "r") as file:
            result = json.load(file)
        return jsonify({"status": "done", "data": result})
    else:
        return jsonify({"status": "running"})

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.get_states_data(data))
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.get_state_data(data))
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.best_5(data))
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.worst_5(data))
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.global_mean(data))
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.diff_from_mean(data))
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.diff_from_mean_state(data))
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.mean_by_category(data))
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """
    Get request data
    Register job. Don't wait for task to finish
    Increment job_id counter
    Return associated job_id
    """
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.mean_by_category_state(data))
    webserver.job_counter += 1
    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/jobs', methods=['GET'])
def jobs():
    """
    Getting the status for all jobs that are un the queue
    """
    state = {}
    state["status"] = "done"
    state["data"] = {[]}
    for i in webserver.tasks_runner.get_ids:
        result = get_response(i)
        state.data.append({"job_id_" + str(i): result["status"]})
    return jsonify(state)

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    """
    Graceful shutdown of the server
    """
    webserver.tasks_runner.is_alive = False
    return jsonify({"status": "shutting_down"})

@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    """
    Return the number of jobs in the queue
    """
    if webserver.tasks_runner.is_alive:
        return jsonify({"num_jobs": webserver.tasks_runner.task_queue.qsize()})
    return jsonify({"num_jobs": 0})

@webserver.route('/')
@webserver.route('/index')
def index():
    """
    Display each route as a separate HTML <p> tag
    """
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"
    msg += paragraphs
    return msg

def get_defined_routes():
    """
    Get all the defined routes
    """
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
