from app import webserver
from flask import request, jsonify
from app.data_ingestor import DataIngestor 

import os
import json

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")
    # TODO
    # Check if job_id is valid
    
    with open(f"buna.txt","w") as f:
            f.write(str(webserver.tasks_runner.get_ids))
    if int(job_id) not in webserver.tasks_runner.get_ids:
       
        return jsonify({"status": "error","reason": "Invalid job_id"})
    elif int(job_id) in webserver.tasks_runner.get_ids and os.path.exists(f"results/{job_id}.json"):
        
        with open(f"./results/{job_id}.json","r") as f:
        #     res = f.read()
        # return jsonify({ "status": "done", "data": jsonify(res) })
            result = json.load(f)
        return jsonify({ "status": "done", "data": result })
    else:
        
        return jsonify({"status": "running"})

    # Check if job_id is done and return the result
    #    res = res_for(job_id)
    #    return jsonify({
    #        'status': 'done',
    #        'data': res
    #    })

    # If not, return running status
    return jsonify({'status': 'NotImplemented'})

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    # Get request data
    # TODO
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.get_states_data(data))
    webserver.job_counter += 1

    

    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    # TODO
    
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.get_state_data(data))
    webserver.job_counter += 1
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    
    
    

    return jsonify({"job_id": webserver.job_counter - 1})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.best_5(data))
    webserver.job_counter += 1
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.worst_5(data))
    webserver.job_counter += 1

    return jsonify({"job_id": webserver.job_counter - 1})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.global_mean(data))
    webserver.job_counter += 1

    return jsonify({"job_id": webserver.job_counter - 1})

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.diff_from_mean(data))
    webserver.job_counter += 1

    return jsonify({"job_id": webserver.job_counter - 1})

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.diff_from_mean_state(data))
    webserver.job_counter += 1

    return jsonify({"job_id": webserver.job_counter - 1})

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id
    
    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.mean_by_category(data))
    webserver.job_counter += 1

    return jsonify({"job_id": webserver.job_counter - 1})

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    data = request.json
    webserver.tasks_runner.submit(webserver.job_counter, lambda: webserver.data_ingestor.mean_by_category(data))
    webserver.job_counter += 1

    return jsonify({"job_id": webserver.job_counter - 1})

    return jsonify({"status": "NotImplemented"})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
