from flask_restx import Namespace, Resource, fields, abort
from flask import request
from util.helper import *
from util.models import *
import db.init_db as db

api = Namespace('ai', description='ai Services')

@api.route('/recommendLLM')
class RecommendLLM(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Missing Arguments')
    @api.response(403, 'Invalid Token')
    @api.expect(llm_request_details(api))
    @api.doc(description='''
        This is used to recommend users the LLM that best suits their needs.
    ''')
    def post(self):
        if not request.json:
            abort(400, 'Malformed Request')
        
        (Service, Price, Response_Speed, Accuracy, Ethical_Training, Green_Computing_Resources, Local_Deployment_Capability, Training_Resource_Requirements, Fine_Tuning_Difficulty, Multilingual_Support_Capability, Model_Scalability) = unpack(request.json, 'Service', 'Price', 'Response_Speed', 'Accuracy', 'Ethical_Training', 'Green_Computing_Resources', 'Local_Deployment_Capability', 'Training_Resource_Requirements', 'Fine_Tuning_Difficulty', 'Multilingual_Support_Capability', 'Model_Scalability')

        session = db.get_session()
        allList = session.query(db.LLM).all()
        session.close()
        
        weights = {
            'Price': Price,
            'Response_Speed': Response_Speed,
            'Accuracy': Accuracy,
            'Ethical_Training': Ethical_Training,
            'Green_Computing_Resources': Green_Computing_Resources,
            'Local_Deployment_Capability': Local_Deployment_Capability,
            'Training_Resource_Requirements': Training_Resource_Requirements,
            'Fine_Tuning_Difficulty': Fine_Tuning_Difficulty,
            'Multilingual_Support_Capability': Multilingual_Support_Capability,
            'Model_Scalability': Model_Scalability
        }

        # Normalize each model's parameter to the range [0, 1]
        def normalize(value, min_value, max_value):
            return (value - min_value) / (max_value - min_value) if max_value != min_value else 1

        # Filter models that do not support the requested functionalities
        filtered_models = []
        for model in allList:
            # Check if each model supports all the requested services
            supported = True
            for service in Service:
                # If the service is not supported, exclude the model
                if getattr(model, service) == 0:
                    supported = False
                    break
            if supported:
                filtered_models.append(model)

        # If no models match the user's requirements, return empty list
        if not filtered_models:
            return {
                'result': []
            }

        # Calculate the total score for each model
        scored_models = []
        for model in filtered_models:
            # Get the minimum and maximum values for each parameter in the filtered models, for normalization
            min_max_values = {
                'Price': (min([m.Price for m in filtered_models]), max([m.Price for m in filtered_models])),
                'Response_Speed': (min([m.Response_Speed for m in filtered_models]), max([m.Response_Speed for m in filtered_models])),
                'Accuracy': (min([m.Accuracy for m in filtered_models]), max([m.Accuracy for m in filtered_models])),
                'Ethical_Training': (min([m.Ethical_Training for m in filtered_models]), max([m.Ethical_Training for m in filtered_models])),
                'Green_Computing_Resources': (min([m.Green_Computing_Resources for m in filtered_models]), max([m.Green_Computing_Resources for m in filtered_models])),
                'Local_Deployment_Capability': (min([m.Local_Deployment_Capability for m in filtered_models]), max([m.Local_Deployment_Capability for m in filtered_models])),
                'Training_Resource_Requirements': (min([m.Training_Resource_Requirements for m in filtered_models]), max([m.Training_Resource_Requirements for m in filtered_models])),
                'Fine_Tuning_Difficulty': (min([m.Fine_Tuning_Difficulty for m in filtered_models]), max([m.Fine_Tuning_Difficulty for m in filtered_models])),
                'Multilingual_Support_Capability': (min([m.Multilingual_Support_Capability for m in filtered_models]), max([m.Multilingual_Support_Capability for m in filtered_models])),
                'Model_Scalability': (min([m.Model_Scalability for m in filtered_models]), max([m.Model_Scalability for m in filtered_models]))
            }

            # Perform weighted calculation for each parameter
            total_score = 0
            for param, weight in weights.items():
                normalized_score = normalize(getattr(model, param), *min_max_values[param])
                total_score += normalized_score * weight

            scored_models.append((model, total_score))

        # Sort models by total score in descending order
        scored_models.sort(key=lambda x: x[1], reverse=True)

        # Get the top recommended models (top 3)
        top_models = scored_models[:3]

        # Return the recommendation results
        recommendations = [{"Name": model.Name, "Score": score} for model, score in top_models]
        
        return {
            'result': recommendations
        }
    

@api.route('/compareLLM')
class CompareLLM(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Missing Arguments')
    @api.response(403, 'Invalid Token')
    @api.expect(llm_compare_details(api))
    @api.doc(description='''
        This is used to compare the LLM.
    ''')
    def post(self):
        if not request.json:
            abort(400, 'Malformed Request')
        
        (names) = unpack(request.json, 'names')

        session = db.get_session()
        allList = session.query(db.LLM).all()
        session.close()
        
        def getModelInfo(raw):
            return {
                "id": raw.id,
                "Name": raw.Name,
                "Development_Company": raw.Development_Company,
                "Price": raw.Price,
                "Response_Speed": raw.Response_Speed,
                "Accuracy": raw.Accuracy,
                "Ethical_Training": raw.Ethical_Training,
                "Green_Computing_Resources": raw.Green_Computing_Resources,
                "Local_Deployment_Capability": raw.Local_Deployment_Capability,
                "Training_Resource_Requirements": raw.Training_Resource_Requirements,
                "Fine_Tuning_Difficulty": raw.Fine_Tuning_Difficulty,
                "Multilingual_Support_Capability": raw.Multilingual_Support_Capability,
                "Model_Scalability": raw.Model_Scalability,
                "Text_Generation": raw.Text_Generation,
                "Image_Generation": raw.Image_Generation,
                "Song_Generation": raw.Song_Generation,
                "Code_Generation": raw.Code_Generation,
                "Table_Processing": raw.Table_Processing,
                "Summarization": raw.Summarization,
                "Logical_Reasoning": raw.Logical_Reasoning,
                "Mathematical_Problem_Solving": raw.Mathematical_Problem_Solving,
                "Description": raw.Description
            }
        
        returnList = []
        for model in allList:
            if model.Name in names[0]:
                returnList.append(getModelInfo(model))
        
        return {
            'result': returnList
        }
    
@api.route('/getAllInfo')
class GetAllInfo(Resource):
    @api.response(200, 'Success')
    @api.response(400, 'Missing Arguments')
    @api.response(403, 'Invalid Token')
    @api.doc(description='''
        This is used to get the LLM info.
    ''')
    def get(self):
        session = db.get_session()
        allList = session.query(db.LLM).all()
        session.close()
        
        def getModelInfo(raw):
            return {
                "id": raw.id,
                "Name": raw.Name,
                "Description": raw.Description
            }
        
        returnList = []
        for model in allList:
            returnList.append(getModelInfo(model))
        
        return {
            'result': returnList
        }
