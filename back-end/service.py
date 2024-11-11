
import random
import db_utils
import math
import json
import ast

class Service():
    def __init__(self, n_instances = 3, n_participant_per_condition = 35, ai_performance = 0.67):
        self.n_instances  = n_instances
        self.n_participant_per_condition = n_participant_per_condition
        self.ai_performance = ai_performance
        self.db = db_utils.get_instance()
        
    def generate_ai_incorrect_suggestion_indexes(self, task_instances):
        ### calculate number of incorret ai suggestions based on its performance
        correct_ai_num = math.floor(float(self.ai_performance * self.n_instances))
        error_ai_num = self.n_instances - correct_ai_num
        
        ### select the indexes of task instances for which ai generates errors
        error_index_list = []
        i = 0
        while i < error_ai_num:
            error_idx = random.randint(0, (self.n_instances - 1))
            if error_idx not in error_index_list:
                error_index_list.append(error_idx)
                i += 1
        
        return error_index_list
        
        
    def set_tasks_instances_with_ai_suggestions(self, task_instances):
        assigned_task_instances = []
        error_index_list = self.generate_ai_incorrect_suggestion_indexes(task_instances)
        
        ### select another route for tasks intances for which ai generates error otherwise ai suggests the best route
        for i, task in enumerate(task_instances):
            if i in error_index_list:
                ai_route_id = -1
                route_transfer_mapping = ast.literal_eval(task["route_transfer_mapping"])
                
                while 1:
                    route_idx = random.randint(0, (len(route_transfer_mapping)-1))
                    if route_idx != int(task["best_route_id"]) and ai_route_id == -1:
                        ai_route_id = route_idx
                        break
                        
                ai_time = str(route_transfer_mapping[ai_route_id]["time"])
                ai_cost = str(route_transfer_mapping[ai_route_id]["cost"])
                ai_route_id = str(ai_route_id)
                
            else:
                ai_route_id = task["best_route_id"]
                ai_time = task["best_time"]
                ai_cost = task["best_cost"]
                
            assigned_task = {"task_id": task["task_id"], "study_condition": task["study_condition"], "scenario": task["scenario"], "complexity": task["complexity"], "task_type": task["task_type"], "best_route_id":task["best_route_id"], "best_time":task["best_time"], "best_cost": task["best_cost"], "ai_route_id":ai_route_id, "ai_time":ai_time, "ai_cost":ai_cost, "route_info_list": task["route_info_list"], "pickup_point": task["pickup_point"], "n_transfer":task["n_transfer"], "static_info": task["static_info"], "route_start_time": task["route_start_time"] , "chance_list": task["chance_list"]}
            assigned_task_instances.append(assigned_task)
            
        return assigned_task_instances
    
    
    def validate_pre_test_attention_checks(self, pre_test):
        ### check if attention checks are answered correctly and return true of false
        for question in pre_test:
            if question["question_id"] == "00_01" and question["answer"] != 3:
                return False
            if question["question_id"] == "00_02" and question["answer"] != 4:
                return False
         
        return True
    

    def save_user_pre_test_response(self, user_id, pre_test):
        ### save pre-test responses in responses db
        pre_test_json = json.dumps(pre_test, sort_keys=False)
        self.db.update_response_pre_test(user_id, pre_test_json)
        
        
        return
    
    

    def set_user_study_condition(self, user_id):
        ### extract all unassigned conditions
        unassigned_conditions = self.db.extract_unassigned_study_conditions(self.n_participant_per_condition)
        
        ### assign a study condition for the user
        assigned_condition = unassigned_conditions[random.randint(0,len(unassigned_conditions) - 1)]
        
        ### manually assign study condition for troubleshooting
        # low_comp = str(random.randint(1,2))
        # assigned_condition = {"study_condition": low_comp}
        
        assigned_condition = {"study_condition": "5"}
        
        ### insert the user with study condition and status in the response table
        self.db.insert_response_user_entry(user_id, assigned_condition["study_condition"])
        
        return assigned_condition["study_condition"]
    
    
    def set_user_tutorial(self, study_condition):
        ### set tutorial based on user study condition
        tutorial = self.db.extract_feature_explanations_study_condition(study_condition)
        return tutorial
    
    
    def set_user_training_task(self, study_condition):
        ### extract training task
        training_task = self.db.extract_training_task(study_condition)[0]
        training_task["ai_route_id"] = training_task["best_route_id"]
        training_task["ai_time"] = training_task["best_time"]
        training_task["ai_cost"] = training_task["best_cost"]
        
        return training_task
    

    def find_feature_quiz_key_answer(self, feature, question_type, quiz_features_key):
        correct_answer = ""
        if question_type == "features_impact":
            for item in ast.literal_eval(quiz_features_key["features_impact"]):
                if item["feature"] == feature: 
                    correct_answer = item["impact"]
                    
        return correct_answer
                                          
    
    
    def set_user_quiz_questions(self, study_condition):
        quiz_features = self.db.extract_quiz_study_condition(study_condition)
        
        quiz_questions = {"features_impact": []}
        
        ### we remove correct answer from the quiz features sent to user
        for item in ast.literal_eval(quiz_features["features_impact"]):
            quiz_questions["features_impact"].append(item["feature"])
            
        return quiz_questions
    
    
    ### quiz_responsne = {"features_impact": [{ "feature": f , "user_answer": [ans]}, ...] }
    def calculate_quiz_score(self, user_id, study_condition, quiz_response):
        features_impact_score = 0
    
    
        quiz_features_key = self.db.extract_quiz_study_condition(study_condition)
        
        ### [ {"feature": f, "question_type": "feature_impact"/"feature_type"} ] 
        incorrect_features_response = []
        
        
        ### feature impact
        for item in quiz_response["features_impact"]:
            for key_item in ast.literal_eval(quiz_features_key["features_impact"]):
                if item["feature"] == key_item["feature"]:
                    ### no negative score for extra impact
                    if len(item["user_answer"]) > len(key_item["impact"]):
                        # features_impact_score = features_impact_score - (len(item["user_answer"]) - len(key_item["impact"]))
                        incorrect_features_response.append({"feature": item["feature"], "question_type": "features_impact"})
                    else:
                        for imp in key_item["impact"]:
                            if imp in item["user_answer"]:
                                features_impact_score += 1
                            else:
                                incorrect_features_response.append({"feature": item["feature"], "question_type": "features_impact"})
                                
    
        
        features_impact_score = float(features_impact_score/int(quiz_features_key["features_impact_score"])) * 100
       
        
                           
        return features_impact_score, incorrect_features_response
    
    
    
    
    ### quiz key = {"features_impact": [{"feature":"estimated_duration", "impact": ["time"]}, ...], "features": {"name": "The name of each sub-route.", ...}}
    def find_feature_explanations_for_incorrect_quiz_response(self, study_condition, incorrect_features_response):
        feature_explanations_to_resend = []
        
        all_feature_explanations = self.db.extract_feature_explanations_study_condition(study_condition)
        quiz_features_key = self.db.extract_quiz_study_condition(study_condition)
        
        for item in incorrect_features_response:
            
            features = all_feature_explanations["features"]
            features = features.replace("\'", "\"")
            features = json.loads(features) 
            
            correct_answer = self.find_feature_quiz_key_answer(item["feature"], item["question_type"], quiz_features_key)
            key_anwser_item = { "feature": item["feature"], "explanation": features[item["feature"]], "question_type": item["question_type"], "correct_answer": correct_answer}
            feature_explanations_to_resend.append(key_anwser_item)
            
        return feature_explanations_to_resend
            
    
    
    
    def check_user_qualification(self, user_id, study_condition, quiz_response, acceptance_threshold = 65):
        
        ### check whether user passed or faild in the quiz
        features_impact_score, incorrect_features_response = self.calculate_quiz_score(user_id, study_condition, quiz_response)
        
        ### disqualify user if the score is below a threshold
        if features_impact_score <= acceptance_threshold:
            ### change the status of the user to failed in responses db
            self.db.set_response_failed_user(user_id)
            return {"status": "failed"}
        else:
            feature_explanations_to_resend = self.find_feature_explanations_for_incorrect_quiz_response(study_condition, incorrect_features_response)
            quiz_transcript = { "status": "passed", "errors": feature_explanations_to_resend}
        
        return quiz_transcript
    
    
    
    
    def set_user_main_task_instances(self, user_id, study_condition):
        
        ### extract task instances corresponding to assigned study condition
        task_instances = self.db.extract_task_instances(study_condition)
        random.shuffle(task_instances)
        
        ### assign task instances with ai suggestion for a user
        assigned_task_instances = self.set_tasks_instances_with_ai_suggestions(task_instances)
        
        ### save user assigned task instances in user_tasks db - only ai suggestions and best answers are added to db
        self.db.insert_user_assigned_tasks(user_id, assigned_task_instances)
        
        ### save user assigned task instances in response db - ai suggestions are added to task instances
        assigned_task_instances_json = json.dumps(assigned_task_instances, sort_keys=False)
        self.db.update_response_assigned_tasks(user_id, assigned_task_instances_json)
        
        ### add +1 to number of assigned participants to the selected study condition in task_assignments db
        self.db.update_assigned_users_study_condition(study_condition)
        
        return assigned_task_instances
    
    
    def calculate_user_score(self, user_id, user_study):
        user_score = 0
        user_tasks = self.db.extract_user_assigned_tasks(user_id)
        for item in user_tasks:
            for res in user_study:
                if item["task_id"] == res["task_id"]:
                    if item["best_route_id"] == res["final_decision"]:
                        user_score+=1
        return user_score
                        
      
    
    def save_user_main_study_response(self, user_id, start_time, end_time, user_study, decision_times):
        ### calculate user score
        user_score = self.calculate_user_score(user_id, user_study)
        
        ### save main user study responses in responses db
        user_study_json = json.dumps(user_study, sort_keys=False)
        decision_times_json = json.dumps(decision_times, sort_keys=False)
        self.db.update_response_user_study(user_id, user_study_json, start_time, end_time, decision_times_json, str(user_score))
        
        return user_score
    
    
    def complete_study(self, user_id, post_test):
        ### save post-test responses in responses db 
        post_test_json = json.dumps(post_test, sort_keys=False)
        self.db.update_response_post_test(user_id, post_test_json)
        
        
        ### add +1 to number of completed participants to the selected study condition in task_assignments db
        study_condition = self.db.extract_user_study_condition(user_id)
        self.db.update_completed_users_study_condition(study_condition)
        
        return
    
    
    
    
    def save_user_event(self, user_id, task_id, event_type, timestamp, event_value):
        ### save event in the user_behaviour db
        self.db.insert_user_ui_interaction(user_id, task_id, event_type, timestamp, event_value)
        
        return
        
        
    
    
    
        
    


    
    
