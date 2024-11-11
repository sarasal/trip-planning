
import json
import sys
from flask import Flask , jsonify, request 
from flask_cors import CORS
import ast

import service

n_instances = 3
n_participant_per_condition = 43
user_service = service.Service(n_instances, n_participant_per_condition)


app = Flask(__name__)
CORS(app)



# assign a study condition to the user & get the pre_test response
@app.route('/get_user_tutorial', methods = ['POST'])
def send_tutorial():
    
    try:
        
        
        user_data = request.json
        
        ### check if data format is correct
        if ("user_id" not in user_data) or ("pre_test" not in user_data):
            return "Bad Request -- TRIP-PLANNER", 400
        
        ### check if attention checks are answered correctly, otherwise reject the user instantly
        pre_test = ast.literal_eval(user_data["pre_test"])
        attention_check = user_service.validate_pre_test_attention_checks(pre_test)
        if attention_check == False:
            return { "status": "failed" }
        

        ### assign the study condition
        study_condition = user_service.set_user_study_condition(user_data["user_id"])
        

        ### set the tutorial based on study condition
        tutorial = user_service.set_user_tutorial(study_condition)
        

        ### save the pre_test
        user_service.save_user_pre_test_response(user_data["user_id"], pre_test)
        
        
        tutorial["status"] = "passed"

        ### convert the string to json
        tutorial_json = json.dumps(tutorial, sort_keys=False, indent=4)
        
        return tutorial_json
        
    except Exception as e:
        print(e)
        return "Internal Server Error -- TRIP-PLANNER", 500





# get the study condition from the user & send the training task
@app.route('/get_user_training_task', methods = ['POST'])
def send_training_task():
    
    try: 
        user_data = request.json
        
        ### check if data format is correct
        if "study_condition" not in user_data:
            return "Bad Request -- TRIP-PLANNER", 400

        ### set the training task
        training_task = user_service.set_user_training_task(user_data["study_condition"])

        ### convert the string to json
        training_task_json = json.dumps(training_task, sort_keys=False, indent=4)

        return training_task_json
    
    except Exception as e:
        print(e)
        return "Internal Server Error -- TRIP-PLANNER", 500






# get the study condition from the user & send the quiz
@app.route('/get_user_quiz', methods = ['POST'])
def send_quiz():
    
    try: 
        user_data = request.json
        
        ### check if data format is correct
        if "study_condition" not in user_data:
            return "Bad Request -- TRIP-PLANNER", 400

        ### set the quiz
        quiz_features = user_service.set_user_quiz_questions(user_data["study_condition"])

        ### convert the string to json
        quiz_features_json = json.dumps(quiz_features, sort_keys=False, indent=4)

        return quiz_features_json
    
    except Exception as e:
        print(e)
        return "Internal Server Error -- TRIP-PLANNER", 500
    
    

@app.route('/check_user_qualification', methods = ['POST'])
def send_quiz_key_answers():
   
    try:
        user_data = request.json

        ### check if data format is correct
        if ("user_id" not in user_data) or ("study_condition" not in user_data) or ("quiz_response" not in user_data):
            return "Bad Request -- TRIP-PLANNER", 400

        ### check whether the user qualify to continiue, if so, send them the key answers for incorrect quiz response
        quiz_transcript = user_service.check_user_qualification(user_data["user_id"], user_data["study_condition"], user_data["quiz_response"])
        

        ### convert the string to json
        quiz_transcript_json = json.dumps(quiz_transcript, sort_keys=False, indent=4)

        return quiz_transcript_json
    
    except Exception as e:
        print(e)
        return "Internal Server Error -- TRIP-PLANNER", 500
        
    
    

# verify if the user passed in the quiz or not, if so then send main study task instances
@app.route('/get_user_task_instances', methods = ['POST'])
def send_task_instances():
    
    try:
        user_data = request.json
        
        ### check if data format is correct
        if "user_id" not in user_data:
            return "Bad Request -- TRIP-PLANNER", 400

        ### set the main task instances for the user
        task_instances = user_service.set_user_main_task_instances(user_data["user_id"], user_data["study_condition"])

         ### convert the string to json   
        assigned_task_instances_json = json.dumps(task_instances, sort_keys=False, indent=4)

        return assigned_task_instances_json
    
    except Exception as e:
        print(e)
        return "Internal Server Error -- TRIP-PLANNER", 500




# get user_responses
@app.route('/submit_user_study', methods = ['POST'])
def save_user_study_responses():
    
    try:
        user_data = request.json
        
        ### check if data format is correct
        if ("user_id" not in user_data) or ("start_time" not in user_data) or ("end_time" not in user_data) or ("decision_times" not in user_data):
            return "Bad Request -- TRIP-PLANNER", 400
        
        ### save user decisions for main task instances and return their score
        user_score = user_service.save_user_main_study_response(user_data["user_id"], user_data["start_time"], user_data["end_time"], user_data["user_study"], user_data["decision_times"])
        res = {"score": user_score}
        res_json = json.dumps(res, sort_keys=False, indent=4)
        
        return res_json
    
    except Exception as e:
        print(e)
        return "Internal Server Error -- TRIP-PLANNER", 500

    


# get post_test
@app.route('/submit_post_test', methods = ['POST'])
def save_post_test():
    
    try:
        user_data = request.json
        
        ### check if data format is correct
        if ("user_id" not in user_data) or ("post_test" not in user_data):
            return "Bad Request -- TRIP-PLANNER", 400
        
        
        ### save the post test and complete the study for the user 
        post_test = ast.literal_eval(str(user_data["post_test"]))
        # print(post_test)
        user_service.complete_study(user_data["user_id"], post_test)

        return "OK -- TRIP-PLANNER", 200
    
    except Exception as e:
        print(e)
        return "Internal Server Error -- TRIP-PLANNER", 500



# get the event invoked by the user
@app.route('/submit_event', methods = ['POST'])
def save_event():
    
    try:
        user_data = request.json
        
        # print("event")
        # print(user_data)

        ### check if data format is correct
        if ("user_id" not in user_data) or ("task_id" not in user_data) or ("event_type" not in user_data) or ("timestamp" not in user_data) or ("event_value" not in user_data):
            return "Bad Request -- TRIP-PLANNER", 400

        ### save the event invoked by the user corresponding to a task id in the db
        user_service.save_user_event(user_data["user_id"], user_data["task_id"], user_data["event_type"], user_data["timestamp"], user_data["event_value"])
        

        return "OK -- TRIP-PLANNER", 200
    
    except Exception as e:
        print(e)
        return "Internal Server Error -- TRIP-PLANNER", 500




if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6800', debug=False)


    
    





# for instance in task_instances:
#     task = {"task_id": instance["task_id"], 
#             "study_condition": instance["study_condition"], 
#             "scenario": instance["scenario"],
#             "complexity":instance["complexity"],
#             "task_type": instance["task_type"],
#             "best_route_id": instance["best_route_id"],
#             "best_time": instance["best_time"],
#             "best_cost": instance["best_cost"],
#             "ai_route_id": instance["ai_route_id"],
#             "ai_time": instance["ai_time"],
#             "ai_cost": instance["ai_cost"],
#             "map_url_list": instance["map_url_list"],
#             "route_info_list": instance["route_info_list"],
#             "pickup_point": instance["pickup_point"],
#             "n_transfer": instance["n_transfer"],
#             "static_info": instance["static_info"],
#             "chance_list": instance["chance_list"]}
#     task_list.append(task)
