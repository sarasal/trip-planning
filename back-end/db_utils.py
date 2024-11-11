import json
import sqlite3
from datetime import datetime

class DatabaseManager():
    
    def __init__(self, db_path, total_task_instances, total_study_conditions, desc_file, route_file, static_file, training_desc_file, training_route_file, training_static_file, quiz_file, feature_file):
        self.db_path = db_path
        self.total_task_instances = total_task_instances
        self.total_study_conditions = total_study_conditions
        self.create_db()
        self.init_task_instances(desc_file, route_file, static_file, "main")
        self.init_task_instances(training_desc_file, training_route_file, training_static_file, "training")
        self.init_quizes(quiz_file)
        self.init_feature_explantions(feature_file)
        
    def dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def create_connection_db(self):
        connection = None
        try:
            connection = sqlite3.connect(self.db_path +'.sqlite')
        except Error as e:
            print(e)

        if connection != None:
            connection.row_factory = self.dict_factory
            

        return connection


    def create_db(self):
        connection = None

        try:
            connection = sqlite3.connect(self.db_path +'.sqlite')
        except Error as e:
            print(e)

        ### responses
        ### status: in_progress, completed, failed
        response_table =  """ CREATE TABLE IF NOT EXISTS responses (
                                            user_id TEXT PRIMARY KEY,
                                            start_time TEXT,
                                            end_time TEXT, 
                                            pre_test TEXT, 
                                            assigned_task_instances TEXT,
                                            user_study TEXT,
                                            decision_times TEXT,
                                            score TEXT,
                                            post_test TEXT,
                                            status TEXT,
                                            study_condition TEXT
                                        ); """

        ### tasks
        task_table = """ CREATE TABLE IF NOT EXISTS tasks (
                                            task_id TEXT PRIMARY KEY,
                                            study_condition TEXT, 
                                            scenario TEXT,
                                            complexity TEXT,
                                            task_type TEXT,
                                            best_route_id TEXT,
                                            best_time TEXT,
                                            best_cost TEXT,
                                            route_transfer_mapping TEXT,
                                            route_info_list TEXT,
                                            pickup_point TEXT,
                                            n_transfer TEXT,
                                            static_info TEXT,
                                            route_start_time TEXT,
                                            chance_list TEXT
                                        ); """
        
        
        ### trainings
        training_table = """ CREATE TABLE IF NOT EXISTS trainings(
                                            task_id TEXT PRIMARY KEY,
                                            study_condition TEXT, 
                                            scenario TEXT,
                                            complexity TEXT,
                                            task_type TEXT,
                                            best_route_id TEXT,
                                            best_time TEXT,
                                            best_cost TEXT,
                                            route_transfer_mapping TEXT,
                                            route_info_list TEXT,
                                            pickup_point TEXT,
                                            n_transfer TEXT,
                                            static_info TEXT,
                                            route_start_time TEXT, 
                                            chance_list TEXT
                                        ); """
        
        

        ### number of users assigned to study conditions 
        task_assignment_table = """ CREATE TABLE IF NOT EXISTS task_assignments (
                                            study_condition TEXT PRIMARY KEY,
                                            assigned_users INTEGER,
                                            completed_users INTEGER
                                            
                                        ); """
        
        
        ### user_tasks
        user_tasks_table = """ CREATE TABLE IF NOT EXISTS user_tasks (
                                            user_id TEXT,
                                            task_id TEXT,
                                            best_route_id TEXT,
                                            best_time TEXT,
                                            best_cost TEXT,
                                            ai_route_id TEXT,
                                            ai_time TEXT,
                                            ai_cost TEXT,
                                            PRIMARY KEY(user_id, task_id)
                                        ); """
        
        ### quiz_questions 
        quiz_questions_table = """ CREATE TABLE IF NOT EXISTS quiz_questions (
                                            study_condition TEXT PRIMARY KEY,
                                            complexity TEXT,
                                            task_type TEXT,
                                            features_impact_score TEXT, 
                                            features_impact TEXT
                                        ); """
        
        ### feature_explanations
        feature_explanations_table = """ CREATE TABLE IF NOT EXISTS feature_explanations (
                                            study_condition TEXT PRIMARY KEY,
                                            complexity TEXT,
                                            task_type TEXT,
                                            features TEXT
                                        ); """
        
        
        
        ### user_behaviour
        user_behaviour_table = """ CREATE TABLE IF NOT EXISTS user_behaviour (
                                            user_id TEXT,
                                            task_id TEXT, 
                                            event_type TEXT,
                                            timestamp TEXT, 
                                            event_value TEXT
                                        ); """


        ### create tables
        if connection != None:
            connection.row_factory = self.dict_factory
            conn = connection.cursor()
            conn.execute(response_table)
            conn.execute(task_table)
            conn.execute(task_assignment_table)
            conn.execute(user_tasks_table)
            conn.execute(training_table)
            conn.execute(quiz_questions_table)
            conn.execute(feature_explanations_table)
            conn.execute(user_behaviour_table)
            connection.commit()
        
        connection.close()

        return 




    def table_is_empty(self, table_name):
        connection = self.create_connection_db()
        sql = 'SELECT count(*) From '+ table_name
        cur = connection.cursor()
        cur.execute(sql)
        result = cur.fetchall()

        cur.close()
        connection.close()
        if result[0]['count(*)'] == 0:
            return True
        else:
            return False
        
    
    def get_table_length(self, table_name):
        connection = self.create_connection_db()
        sql = 'SELECT count(*) From '+ table_name
        cur = connection.cursor()
        cur.execute(sql)
        result = cur.fetchall()

        cur.close()
        connection.close()
        table_len = result[0]['count(*)']
        return table_len

    
    
    
    
    
    
    
    
    

    ############ responses table
    def insert_response_user_entry(self, user_id, study_condition):
        status = "in_progress"
        try:
            connection = self.create_connection_db()
            sql = ''' INSERT INTO responses (user_id, status, study_condition)
                      VALUES(?,?,?) '''
            cur = connection.cursor()
            value = (user_id, status, study_condition,)
            cur.execute(sql, value)
            connection.commit()
            cur.close()
            connection.close()
        except:
            print(" *********************** error insert user entry info with user with id ", user_id, " in responses table")
        
        return
    
    
    
    def update_response_pre_test(self, user_id, pre_test):
        try:
            connection = self.create_connection_db()
            sql = ''' UPDATE responses SET pre_test = ? WHERE user_id = ? '''
            cur = connection.cursor()
            value = (pre_test, user_id,)
            cur.execute(sql, value)
            connection.commit()
            cur.close()
            connection.close()
        except:
            print(" *********************** error insert pretest of the user with id ", user_id, " in responses table")
        
        return
    
    
    def update_response_assigned_tasks(self, user_id, assigned_tasks):
        try:
            connection = self.create_connection_db()
            sql = ''' UPDATE responses SET assigned_task_instances = ? WHERE user_id = ? '''
            cur = connection.cursor()
            value = (assigned_tasks, user_id, )
            cur.execute(sql, value)
            connection.commit()
            cur.close()
            connection.close()
        except:
            print(" *********************** error insert user task instances of the user with id ", user_id, " in responses table")
        return



    def update_response_user_study(self, user_id, user_study, start_time, end_time, decision_times, score):
        try:
            connection = self.create_connection_db()
            sql = ''' UPDATE responses SET start_time = ?, end_time = ?, user_study = ?, decision_times = ?, score = ? WHERE user_id = ? '''
            cur = connection.cursor()
            value = (start_time, end_time, user_study, decision_times, score, user_id, )
            cur.execute(sql, value)
            connection.commit()
            cur.close()
            connection.close()
        except: 
            print(" *********************** error update user study of the user with id ", user_id, " in responses table")
                  
        return


    def update_response_post_test(self, user_id, post_test):
        status = "completed"
        try: 
            connection = self.create_connection_db()
            sql = ''' UPDATE responses SET post_test = ?, status = ? WHERE user_id = ? '''
            cur = connection.cursor()
            value = (post_test, status, user_id, )
            cur.execute(sql, value)
            connection.commit()
            cur.close()
            connection.close()
        except:
            print(" *********************** error update post-test of the user with id ", user_id, " in responses table")
                  
        return
    
    
    def set_response_failed_user(self, user_id):
        status = "failed"
        try: 
            connection = self.create_connection_db()
            sql = ''' UPDATE responses SET status = ? WHERE user_id = ? '''
            cur = connection.cursor()
            value = (status, user_id, )
            cur.execute(sql, value)
            connection.commit()
            cur.close()
            connection.close()
        except:
            print(" *********************** error update status of the failed user with id ", user_id, " in responses table")
                  
        return
        

    
    def extract_user_study_condition(self, user_id):
        connection = self.create_connection_db()
        cur = connection.cursor()
        sql = ''' SELECT study_condition FROM responses WHERE user_id = ? '''
        value = (user_id,)
        cur.execute(sql, value)
        row = cur.fetchone()
        cur.close()
        connection.close()
        return row["study_condition"]


    def extract_user_response(self,user_id):
        connection = self.create_connection_db()
        cur = connection.cursor()
        sql = ''' SELECT * FROM responses WHERE user_id = ? '''
        value = (user_id,)
        cur.execute(sql, value)
        rows = cur.fetchall()
        cur.close()
        connection.close()
        return rows
    
    
    
    
    
    
    
    
    

    ############ user_tasks table
    def insert_user_assigned_tasks(self, user_id, task_instances):
        
        try:
            connection = self.create_connection_db()
            sql = ''' INSERT INTO user_tasks (user_id, task_id, best_route_id, best_time, best_cost, ai_route_id, ai_time, ai_cost)
                      VALUES(?,?,?,?,?,?,?,?) '''
            cur = connection.cursor()
            
            for task_instance in task_instances:
                value = (user_id, task_instance["task_id"], task_instance["best_route_id"], task_instance["best_time"], task_instance["best_cost"], task_instance["ai_route_id"], task_instance["ai_time"], task_instance["ai_cost"],)
                cur.execute(sql, value)
                
            connection.commit()
            cur.close()
            connection.close()
        except:
            print(" *********************** error insert user task instance for user with id ", user_id, " in user_tasks table")
        
        return
    
    
    
    def extract_user_assigned_tasks(self, user_id):
        connection = self.create_connection_db()
        cur = connection.cursor()
        sql = ''' SELECT * FROM user_tasks WHERE user_id = ? '''
        value = (user_id,)
        cur.execute(sql, value)
        rows = cur.fetchall()
        cur.close()
        connection.close()
        return rows
    
    
    
    
    
    
    
    
    
    
    
    ############ user_behaviour table
    def insert_user_ui_interaction(self, user_id, task_id, event_type, timestamp, event_value):
        try:
            connection = self.create_connection_db()
            sql = ''' INSERT INTO user_behaviour (user_id, task_id, event_type, timestamp, event_value )
                      VALUES(?,?,?,?,?) '''
            cur = connection.cursor()
            value = (user_id, task_id, event_type, timestamp, event_value, )
            cur.execute(sql, value)
            connection.commit()
            cur.close()
            connection.close()
        except:
            print(" *********************** error insert event ", event_type, " with value of ", event_value, " for user with id ", user_id, " in user_behaviour table")
        
        return
    
    
    
    

    
    
    
    
    
    
    
    
        
    
    
    
    

    ######### tasks table
    def insert_task_instance(self, task_id, study_condition, scenario, complexity, task_type, best_route_id, best_time, best_cost, route_transfer_mapping, route_info_list, pickup_point, n_transfer, static_info, route_start_time, chance_list):
        try: 
            tasks_len = self.get_table_length('tasks')
            if tasks_len >= self.total_task_instances:
                return

            connection = self.create_connection_db()
            sql = ''' INSERT INTO tasks (task_id, study_condition, scenario, complexity, task_type, best_route_id, best_time, best_cost, route_transfer_mapping, route_info_list, pickup_point, n_transfer, static_info, route_start_time, chance_list)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
            cur = connection.cursor()
            value = (task_id, study_condition, scenario, complexity, task_type, best_route_id, best_time, best_cost, route_transfer_mapping, route_info_list, pickup_point, n_transfer, static_info, route_start_time, chance_list, )
            cur.execute(sql, value)
            connection.commit()
            cur.close()
            connection.close()
        except:
            print(" *********************** error insert task with id ", task_id, " in tasks table")
            
        return


    
    def extract_task_instances(self, study_condition):
        connection = self.create_connection_db()
        cur = connection.cursor()
        sql = ''' SELECT * FROM tasks WHERE study_condition = ? '''
        value = (study_condition,)
        cur.execute(sql, value)
        rows = cur.fetchall()
        cur.close()
        connection.close()
        return rows
    
    
    
    
    
    
    
    
    
    
    
    ######### trainings table
    def insert_training_task(self, task_id, study_condition, scenario, complexity, task_type, best_route_id, best_time, best_cost, route_transfer_mapping, route_info_list, pickup_point, n_transfer, static_info, route_start_time, chance_list):
        try: 
            tasks_len = self.get_table_length('trainings')
            if tasks_len >= (self.total_study_conditions):
                return

            connection = self.create_connection_db()
            sql = ''' INSERT INTO trainings (task_id, study_condition, scenario, complexity, task_type, best_route_id, best_time, best_cost, route_transfer_mapping, route_info_list, pickup_point, n_transfer, static_info, route_start_time, chance_list)
                      VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
            cur = connection.cursor()
            value = (task_id, study_condition, scenario, complexity, task_type, best_route_id, best_time,  best_cost, route_transfer_mapping, route_info_list, pickup_point, n_transfer, static_info, route_start_time, chance_list, )
            cur.execute(sql, value)
            connection.commit()
            cur.close()
            connection.close()
        except:
            print(" *********************** error insert training task with id ", task_id, " in trainings table")
            
        return


    
    def extract_training_task(self, study_condition):
        connection = self.create_connection_db()
        cur = connection.cursor()
        sql = ''' SELECT * FROM trainings WHERE study_condition = ? '''
        value = (study_condition,)
        cur.execute(sql, value)
        rows = cur.fetchall()
        cur.close()
        connection.close()
        return rows
    
    
    
    
    
    
    
    
    
    

    
    ######## task_assignments
    def insert_users_task_assigments(self, study_condition):
        try:
            connection = self.create_connection_db()
            sql = ''' INSERT INTO task_assignments (study_condition, assigned_users, completed_users)
                      VALUES(?,?,?) '''
            cur = connection.cursor()
            value = (study_condition, 0, 0,  )
            cur.execute(sql, value)
            connection.commit()
            cur.close()
            connection.close()
        except:
            print(" *********************** error insert a study condition in task_assignments table")
            
        return


    def update_assigned_users_study_condition(self, study_condition):
        try:
            connection = self.create_connection_db()
            sql = ''' UPDATE task_assignments SET assigned_users = assigned_users + 1 WHERE study_condition = ? '''
            cur = connection.cursor()
            value = (study_condition,)
            cur.execute(sql, value)
            connection.commit()
            cur.close()
            connection.close()
        except:
            print(" *********************** error update assigned users for study condition with id ", study_condition, " in task_assignmenst table")
            
        return


    def update_completed_users_study_condition(self, study_condition):
        try:
            connection = self.create_connection_db()
            sql = ''' UPDATE task_assignments SET completed_users = completed_users + 1 WHERE study_condition = ? '''
            cur = connection.cursor()
            value = (study_condition,)
            cur.execute(sql, value)
            connection.commit()
            cur.close()
            connection.close()
        except:
            print(" *********************** error update completed users for study condition with id ", study_condition, " in task_assignmenst table")
            
        return


    def extract_min_max_assigend_study_condition(self):
        connection = self.create_connection_db()
        cur = connection.cursor()
        sql = ''' SELECT min(assigned_users) FROM task_assignments '''
        cur.execute(sql)
        min_val = cur.fetchone()
        min_val = min_val["min(assigned_users)"]

        sql = ''' SELECT max(assigned_users) FROM task_assignments '''
        cur.execute(sql)
        max_val = cur.fetchone()
        max_val = max_val["max(assigned_users)"]

        cur.close()
        connection.close()
        return min_val, max_val


    def extract_unassigned_study_conditions(self, threshold):
        min_val, max_val = self.extract_min_max_assigend_study_condition()
        
        connection = self.create_connection_db()
        cur = connection.cursor()
        if min_val == max_val:
            sql = ''' SELECT study_condition FROM task_assignments WHERE completed_users < ?  '''
            value = (threshold,)
        else:
            sql = ''' SELECT study_condition FROM task_assignments WHERE completed_users < ?  AND assigned_users == ? '''
            value = (threshold,min_val, )

        cur.execute(sql, value)
        rows = cur.fetchall()
        cur.close()
        connection.close()
        return rows
    
    def find_task(self, study_json_list, task_id):
        for task in study_json_list:
            if task["task_id"] == task_id:
                return task
        return {}
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ######## quiz questions
    def insert_quiz_questions(self, study_condition, complexity, task_type, features_impact_score, features_impact):
        try:
            connection = self.create_connection_db()
            sql = ''' INSERT INTO quiz_questions (study_condition, complexity, task_type, features_impact_score, features_impact)
                      VALUES(?,?,?,?,?) '''
            cur = connection.cursor()
            value = (study_condition, complexity, task_type, features_impact_score, features_impact,)
            cur.execute(sql, value)
            connection.commit()
            cur.close()
            connection.close()
        except:
            print(" *********************** error insert questions into the quiz questions table ")
        
        return
    
    
    def extract_quiz_study_condition(self, study_condition):
        connection = self.create_connection_db()
        cur = connection.cursor()
        sql = ''' SELECT features_impact_score, features_impact FROM quiz_questions WHERE study_condition = ? '''
        value = (study_condition,)
        cur.execute(sql, value)
        row = cur.fetchone()
        cur.close()
        connection.close()
        return row
    
    
    
    def init_quizes(self, quiz_file):
        f_quiz = open(quiz_file)
        quiz_data = json.load(f_quiz)
        
        for instance in quiz_data:
            self.insert_quiz_questions(instance["study_condition"], instance["complexity"], instance["task_type"], instance["features_impact_score"], str(instance["features_impact"]))
        
        return
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    ### feature_explanations
    def insert_feature_explanations(self, study_condition, complexity, task_type, features):
        try:
            connection = self.create_connection_db()
            sql = ''' INSERT INTO feature_explanations (study_condition, complexity, task_type, features)
                      VALUES(?,?,?,?) '''
            cur = connection.cursor()
            value = (study_condition, complexity, task_type, features,)
            cur.execute(sql, value)
            connection.commit()
            cur.close()
            connection.close()
        except:
            print(" *********************** error insert into feature explantions table")
        
        return
    
    
    
    
    def extract_feature_explanations_study_condition(self, study_condition):
        connection = self.create_connection_db()
        cur = connection.cursor()
        sql = ''' SELECT * FROM feature_explanations WHERE study_condition = ? '''
        value = (study_condition,)
        cur.execute(sql, value)
        row = cur.fetchone()
        cur.close()
        connection.close()
        return row
    
    
    
    def init_feature_explantions(self, feature_file):
        f_features = open(feature_file)
        exp_data = json.load(f_features)
        
        for instance in exp_data:
            self.insert_feature_explanations(instance["study_condition"], instance["complexity"], instance["task_type"], str(instance["features"]))
              
        return
    
    
    
    
    
    
    
    
    
    
    
    
    
    #### init tasks/trainings and task_assignments table from file
    def init_task_instances(self, desc_file, route_file, static_file, training_or_main):
        
        study_condition_list = []
        
        ### desc_data is like [ {"task_id": taskid, "study_condition": sc_value, "scenario":s_vale, "complexity": low/medium/high, "task_type": diagnostic/prognostic}]
        f_desc = open(desc_file)
        desc_data = json.load(f_desc)
        
        ### route_data is like [{"task_id": taskid, "study_condition": sc_value, "best_index": best_route_id, "best_time": time, "best_cost": cost, "route_transfer_mapping": rt_value, "route_info_list": route_value,"pickup_point": [,], "n_transfer": n, "chance_list": c_value ]
        f_route = open(route_file)
        route_data = json.load(f_route)
        
        
        # ### map_file is like [{"task_id": taskid, "study_condition": sc_value, "map_url_list": url_list }]
        # f_map = open(map_file)
        # map_data = json.load(f_map)
        
        ### static file is like [ {"task_id": taskid, "study_condition": sc_value, "general_features": [{"train": n1, "taxi": n2, "bus": n3, "study_feature": sf_value, "attr": speed_kph/cost}] }
        f_static = open(static_file)
        static_data = json.load(f_static)
        
        
        ### init tasks/trainings table
        for instance in desc_data:
            route_dict = self.find_task(route_data, instance["task_id"])
            # map_dict = self.find_task(map_data, instance["task_id"])
            static_dict = self.find_task(static_data, instance["task_id"])
            
            ### insert task instance to tasks db or trainings db according to the file it reads from (identified with parameter training or main)
            if training_or_main == "main":
                self.insert_task_instance(instance["task_id"], instance["study_condition"], instance["scenario"], instance["complexity"], instance["task_type"], route_dict["best_index"], route_dict["best_time"], route_dict["best_cost"], route_dict["route_transfer_mapping"], route_dict["route_info_list"], route_dict["pickup_point"], route_dict["n_transfer"], static_dict["general_features"], route_dict["route_start_time"] , route_dict["chance_list"])
            elif training_or_main == "training":
                self.insert_training_task(instance["task_id"], instance["study_condition"], instance["scenario"], instance["complexity"], instance["task_type"], route_dict["best_index"], route_dict["best_time"], route_dict["best_cost"], route_dict["route_transfer_mapping"], route_dict["route_info_list"], route_dict["pickup_point"], route_dict["n_transfer"], static_dict["general_features"], route_dict["route_start_time"], route_dict["chance_list"])
        
            if instance["study_condition"] not in study_condition_list:
                study_condition_list.append(instance["study_condition"])
        
        
        ### init task_assignments table - if insert into tasks table 
        if training_or_main == "main":
            for cond in study_condition_list:
                self.insert_users_task_assigments(cond)
        
        return
    
    
total_task_instances = 18
total_study_conditions = 6

db_path = "/root/trip_planner/backend/writing"
description_path = '/root/trip_planner/config_files/description.json'
route_path = '/root/trip_planner/config_files/route.json'
static_path = '/root/trip_planner/config_files/static.json'

training_description_path = '/root/trip_planner/config_files/training_description.json'
training_route_path = '/root/trip_planner/config_files/training_route.json'
training_static_path = '/root/trip_planner/config_files/training_static.json'

quiz_path = '/root/trip_planner/config_files/quiz.json'
features_path = '/root/trip_planner/config_files/feature_explanations.json'



db = DatabaseManager(db_path, total_task_instances, total_study_conditions, description_path, route_path, static_path , training_description_path, training_route_path, training_static_path, quiz_path, features_path)
    
def get_instance():
    global db
    if db != None:
        return db
    
    db = DatabaseManager(db_path, total_task_instances, total_study_conditions, description_path, route_path, static_path, training_description_path, training_route_path, training_static_path,quiz_path, features_path)
