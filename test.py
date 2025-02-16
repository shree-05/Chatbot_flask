

# import os
# import openai
# from dotenv import load_dotenv
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from pymongo import MongoClient
# from datetime import datetime, timedelta
# import pytz


# # Load environment variables from .env file
# load_dotenv()

# # Get OpenAI API key
# API_KEY = os.getenv("OPENAI_API_KEY")

# if not API_KEY:
#     raise ValueError("Missing OpenAI API key. Set OPENAI_API_KEY in environment variables.")

# # Get MongoDB connection string
# MONGO_URI = os.getenv("MONGO_URI")
# if not MONGO_URI:
#     raise ValueError("Missing MongoDB URI. Set MONGO_URI in environment variables.")

# # Configure OpenAI API
# openai.api_key = API_KEY

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)  # Enable CORS for frontend access

# # Connect to MongoDB
# client = MongoClient(MONGO_URI)
# db = client["chatbot_db"]  # Database name
# chat_collection = db["chat_history"]  # Collection name


# def get_ist_time():
#     ist_timezone = pytz.timezone("Asia/Kolkata")
#     ist_time = datetime.now(ist_timezone)
#     return ist_time


# def cleanup_old_chats():
#     """Delete chats older than 24 hours"""
#     cutoff_time = get_ist_time() - timedelta(days=1)
#     chat_collection.delete_many({"timestamp": {"$lt": cutoff_time}})


# # System message to define chatbot's role
# system_prompt = """
# You are a friendly, compassionate mental health assistant designed to support users after they complete tests for depression and anxiety. Your primary tasks are to monitor their emotional well-being, provide thoughtful feedback, and offer helpful suggestions when needed.

# Your Responsibilities:
# 1️ **Daily Check-ins:**  
#    - Greet the user warmly and ask about their day.  
#    - Use open-ended, non-judgmental questions like:  
#      "How are you feeling today?"  
#      "What was the best part of your day?"  

# 2️ **Emotional Analysis:**  
#    - Detect signs of depression or anxiety.  
#    - Track changes in mood over time.  

# 3️ **Providing Support:**  
#    - Offer empathetic, supportive responses.  
#    - Suggest healthy coping mechanisms.  

# 4️ **Encouraging Positive Habits:**  
#    - Recommend journaling, mindfulness, sleep, and exercise.  
#    - Suggest breathing exercises for anxiety.  

# 5️ **Recognizing Urgent Situations:**  
#    - If severe distress is detected, recommend seeking professional help.  
#    - Example: "I'm sorry you're feeling this way. It might help to talk to a trusted person or professional."  

#  **Remember:** You are a supportive companion, not a replacement for professional therapy.
#  also give all the responses in Marathi language
#  when you are asked who are you should ans " "Hello! I am your personal mental health assistant "Manodarpan", here to support and guide you. I can help you track your mental well-being, assess your mood, suggest self-care tips, and connect you with professionals if needed. Feel free to share how you're feeling, and I'll do my best to assist you!" "
# """

# # Store conversation histories for different sessions
# session_histories = {}

# # Function to generate chatbot response
# def get_response(conversation):
#     response = openai.ChatCompletion.create(
#         model="gpt-4o-mini",
#         messages=conversation,
#         temperature=0.8
#     )
#     return response["choices"][0]["message"]["content"]

# # Function to save chat messages to MongoDB
# def save_to_db(session_id, user_message, bot_message):
#     chat_entry = {
#         "session_id": session_id,
#         "user_message": user_message,
#         "bot_message": bot_message,
#         "timestamp": get_ist_time()
#     }
#     chat_collection.insert_one(chat_entry)

# # Function to get conversation history for a session
# def get_session_history(session_id):
#     if session_id not in session_histories:
#         session_histories[session_id] = [{"role": "system", "content": system_prompt}]
    
#     # Get today's chat history from MongoDB
#     today_start = get_ist_time().replace(hour=0, minute=0, second=0, microsecond=0)
#     chats = chat_collection.find({
#         "session_id": session_id,
#         "timestamp": {"$gte": today_start}
#     }).sort("timestamp", 1)
    
#     history = [{"role": "system", "content": system_prompt}]
#     for chat in chats:
#         history.extend([
#             {"role": "user", "content": chat["user_message"]},
#             {"role": "assistant", "content": chat["bot_message"]}
#         ])
    
#     session_histories[session_id] = history
#     return history

# @app.route('/chat', methods=['POST'])
# def chat():
#     try:
#         # Get user input from request
#         data = request.json
#         user_message = data.get("message", "").strip()
#         session_id = data.get("session_id", "default")

#         if not user_message:
#             return jsonify({"error": "No message provided"}), 400

#         # Clean up old chats
#         cleanup_old_chats()

#         # Get conversation history for this session
#         conversation_history = get_session_history(session_id)

#         # Add user message to conversation history
#         conversation_history.append({"role": "user", "content": user_message})

#         # Get chatbot response
#         bot_message = get_response(conversation_history)

#         # Add chatbot response to conversation history
#         conversation_history.append({"role": "assistant", "content": bot_message})

#         # Store chat in MongoDB
#         save_to_db(session_id, user_message, bot_message)

#         return jsonify({"response": bot_message})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/get_chat_history', methods=['GET'])
# def get_chat_history():
#     try:
#         session_id = request.args.get('session_id', 'default')
        
#         # Get today's chat history
#         today_start = get_ist_time().replace(hour=0, minute=0, second=0, microsecond=0)
#         chats = chat_collection.find({
#             "session_id": session_id,
#             "timestamp": {"$gte": today_start}
#         }).sort("timestamp", 1)
        
#         chat_history = []
#         for chat in chats:
#             chat_history.extend([
#                 {"sender": "user", "text": chat["user_message"]},
#                 {"sender": "bot", "text": chat["bot_message"]}
#             ])
            
#         return jsonify({"history": chat_history})
        
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)








# working code 


# import os
# import openai
# from dotenv import load_dotenv
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from pymongo import MongoClient
# from datetime import datetime, timedelta
# import pytz

# # Load environment variables
# load_dotenv()

# # Validate API and Database credentials
# API_KEY = os.getenv("OPENAI_API_KEY")
# MONGO_URI = os.getenv("MONGO_URI")
# if not API_KEY or not MONGO_URI:
#     raise ValueError("Missing required environment variables")

# openai.api_key = API_KEY
# app = Flask(__name__)
# CORS(app)

# # Database setup
# client = MongoClient(MONGO_URI)
# db = client["chatbot_db"]
# chat_collection = db["chat_history"]

# # Time and chat management
# def get_ist_time():
#     return datetime.now(pytz.timezone("Asia/Kolkata"))

# def cleanup_old_chats():
#     chat_collection.delete_many({"timestamp": {"$lt": get_ist_time() - timedelta(days=1)}})

# system_prompt = """
# तुम्ही 'मनोदर्पण' मानसिक आरोग्य सहाय्यक आहात. तुमचा उद्देश वापरकर्त्यांची मानसिक स्थिती समजून त्यांना आधार देणे आहे. तुमचे उत्तर नेहमी मराठीत असले पाहिजे. वापरकर्त्याला गरज असल्यास व्यावसायिक मदत घेण्याचा सल्ला द्या.
# """

# session_histories = {}

# def get_response(conversation):
#     response = openai.ChatCompletion.create(
#         model="gpt-4o-mini",
#         messages=conversation,
#         temperature=0.8
#     )
#     return response["choices"][0]["message"]["content"]

# def save_to_db(session_id, user_message, bot_message):
#     chat_collection.insert_one({
#         "session_id": session_id,
#         "user_message": user_message,
#         "bot_message": bot_message,
#         "timestamp": get_ist_time()
#     })

# def get_session_history(session_id):
#     today_start = get_ist_time().replace(hour=0, minute=0, second=0)
#     chats = chat_collection.find({"session_id": session_id, "timestamp": {"$gte": today_start}}).sort("timestamp", 1)
#     history = [{"role": "system", "content": system_prompt}]
#     for chat in chats:
#         history.extend([
#             {"role": "user", "content": chat["user_message"]},
#             {"role": "assistant", "content": chat["bot_message"]}
#         ])
#     session_histories[session_id] = history
#     return history

# @app.route('/chat', methods=['POST'])
# def chat():
#     try:
#         data = request.json
#         session_id = data.get("session_id", "default")
#         user_message = data.get("message", "").strip()

#         if not user_message:
#             return jsonify({"error": "Empty message"}), 400

#         cleanup_old_chats()
#         conversation = get_session_history(session_id) + [{"role": "user", "content": user_message}]
#         bot_message = get_response(conversation)
#         save_to_db(session_id, user_message, bot_message)
#         return jsonify({"response": bot_message})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/get_chat_history', methods=['GET'])
# def get_chat_history():
#     try:
#         session_id = request.args.get('session_id', 'default')
#         today_start = get_ist_time().replace(hour=0, minute=0, second=0)
#         chats = chat_collection.find({"session_id": session_id, "timestamp": {"$gte": today_start}}).sort("timestamp", 1)
#         return jsonify({"history": [{"sender": "user" if c["user_message"] else "bot", "text": c["user_message"] or c["bot_message"]} for c in chats]})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


# import os
# import openai
# import uuid
# from dotenv import load_dotenv
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from pymongo import MongoClient
# from datetime import datetime, timedelta
# import pytz

# # Load environment variables
# load_dotenv()
# API_KEY = os.getenv("OPENAI_API_KEY")
# MONGO_URI = os.getenv("MONGO_URI")
# if not API_KEY or not MONGO_URI:
#     raise ValueError("Missing required environment variables")

# openai.api_key = API_KEY
# app = Flask(__name__)
# CORS(app)

# # Database setup
# client = MongoClient(MONGO_URI)
# db = client["chatbot_db"]
# chat_collection = db["chat_history"]
# session_collection = db["user_sessions"]

# # Time management
# def get_ist_time():
#     return datetime.now(pytz.timezone("Asia/Kolkata"))

# def cleanup_old_chats():
#     chat_collection.delete_many({"timestamp": {"$lt": get_ist_time() - timedelta(days=1)}})

# # System Prompt
# system_prompt = """
# तुम्ही 'मनोदर्पण' मानसिक आरोग्य सहाय्यक आहात. तुमचा उद्देश वापरकर्त्यांची मानसिक स्थिती समजून त्यांना आधार देणे आहे. तुमचे उत्तर नेहमी मराठीत असले पाहिजे.
# """

# def get_response(conversation):
#     response = openai.ChatCompletion.create(
#         model="gpt-4o-mini",
#         messages=conversation,
#         temperature=0.8
#     )
#     return response["choices"][0]["message"]["content"]

# def save_to_db(session_id, user_message, bot_message):
#     chat_collection.insert_one({
#         "session_id": session_id,
#         "user_message": user_message,
#         "bot_message": bot_message,
#         "timestamp": get_ist_time()
#     })

# def get_session_history(session_id):
#     chats = chat_collection.find({"session_id": session_id}).sort("timestamp", 1)
#     history = [{"role": "system", "content": system_prompt}]
#     for chat in chats:
#         history.append({"role": "user", "content": chat["user_message"]})
#         history.append({"role": "assistant", "content": chat["bot_message"]})
#     return history

# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.json
#     session_id = data.get('session_id') or str(uuid.uuid4())
#     user_message = data.get('message')

#     session_collection.update_one(
#         {"session_id": session_id},
#         {"$push": {"messages": user_message}},
#         upsert=True
#     )

#     conversation = get_session_history(session_id)
#     conversation.append({"role": "user", "content": user_message})
#     bot_response = get_response(conversation)

#     save_to_db(session_id, user_message, bot_response)

#     return jsonify({"response": bot_response, "session_id": session_id})

# @app.route('/get_chat_history', methods=['GET'])
# def get_chat_history():
#     session_id = request.args.get('session_id')
#     chats = chat_collection.find({"session_id": session_id}).sort("timestamp", 1)
#     history = [{"sender": "user" if c["user_message"] else "bot", "text": c["user_message"] or c["bot_message"]} for c in chats]
#     return jsonify({"history": history})

# if __name__ == '__main__':
#     cleanup_old_chats()
#     app.run(debug=True)






# fire base wala code 

# import os
# import openai
# import uuid
# import firebase_admin
# from firebase_admin import credentials, firestore
# from dotenv import load_dotenv
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from datetime import datetime, timedelta
# import pytz

# # Load environment variables
# load_dotenv()
# API_KEY = os.getenv("OPENAI_API_KEY")
# FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

# if not API_KEY or not FIREBASE_CREDENTIALS:
#     raise ValueError("Missing required environment variables")

# openai.api_key = API_KEY

# # Initialize Flask App
# app = Flask(__name__)
# CORS(app)

# # Initialize Firebase
# cred = credentials.Certificate(FIREBASE_CREDENTIALS)
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# # Time Management
# def get_ist_time():
#     return datetime.now(pytz.timezone("Asia/Kolkata"))

# # System Prompt
# system_prompt = """
# तुम्ही 'मनोदर्पण' मानसिक आरोग्य सहाय्यक आहात. तुमचा उद्देश वापरकर्त्यांची मानसिक स्थिती समजून त्यांना आधार देणे आहे. तुमचे उत्तर नेहमी मराठीत असले पाहिजे.

# You are a friendly, compassionate mental health assistant designed to support users after they complete tests for depression and anxiety. Your primary tasks are to monitor their emotional well-being, provide thoughtful feedback, and offer helpful suggestions when needed.

# Your Responsibilities:
# 1️ **Daily Check-ins:**  
#    - Greet the user warmly and ask about their day.  
#    - Use open-ended, non-judgmental questions like:  
#      "How are you feeling today?"  
#      "What was the best part of your day?"  

# 2️ **Emotional Analysis:**  
#    - Detect signs of depression or anxiety.  
#    - Track changes in mood over time.  

# 3️ **Providing Support:**  
#    - Offer empathetic, supportive responses.  
#    - Suggest healthy coping mechanisms.  

# 4️ **Encouraging Positive Habits:**  
#    - Recommend journaling, mindfulness, sleep, and exercise.  
#    - Suggest breathing exercises for anxiety.  

# 5️ **Recognizing Urgent Situations:**  
#    - If severe distress is detected, recommend seeking professional help.  
#    - Example: "I'm sorry you're feeling this way. It might help to talk to a trusted person or professional."  

#  **Remember:** You are a supportive companion, not a replacement for professional therapy.
#  also give all the responses in Marathi language
#  when you are asked who are you should ans " "Hello! I am your personal mental health assistant "Manodarpan", here to support and guide you. I can help you track your mental well-being, assess your mood, suggest self-care tips, and connect you with professionals if needed. Feel free to share how you're feeling, and I'll do my best to assist you!"
# """

# # OpenAI Chat Function
# def get_response(conversation):
#     response = openai.ChatCompletion.create(
#         model="gpt-4o-mini",
#         messages=conversation,
#         temperature=0.8
#     )
#     return response["choices"][0]["message"]["content"]

# # Save Chat to Firestore
# def save_to_db(session_id, user_message, bot_message):
#     chat_ref = db.collection("chat_history").document(session_id).collection("chats").document()
#     chat_ref.set({
#         "session_id": session_id,
#         "user_message": user_message,
#         "bot_message": bot_message,
#         "timestamp": get_ist_time()
#     })

# # Get Chat History from Firestore
# def get_session_history(session_id):
#     chats_ref = db.collection("chat_history").document(session_id).collection("chats").order_by("timestamp")
#     chats = chats_ref.stream()

#     history = [{"role": "system", "content": system_prompt}]
#     for chat in chats:
#         chat_data = chat.to_dict()
#         history.append({"role": "user", "content": chat_data["user_message"]})
#         history.append({"role": "assistant", "content": chat_data["bot_message"]})
    
#     return history

# # Cleanup Old Chats (Delete chats older than 1 day)
# def cleanup_old_chats():
#     cutoff_time = get_ist_time() - timedelta(days=1)
#     chat_sessions = db.collection("chat_history").stream()

#     for session in chat_sessions:
#         chats_ref = db.collection("chat_history").document(session.id).collection("chats")
#         old_chats = chats_ref.where("timestamp", "<", cutoff_time).stream()
        
#         for chat in old_chats:
#             chat.reference.delete()

# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.json
#     session_id = data.get('session_id') or str(uuid.uuid4())
#     user_message = data.get('message')

#     # Update session messages
#     session_ref = db.collection("user_sessions").document(session_id)
#     session_ref.set({"session_id": session_id}, merge=True)
#     session_ref.update({"messages": firestore.ArrayUnion([user_message])})

#     # Get past chat history
#     conversation = get_session_history(session_id)
#     conversation.append({"role": "user", "content": user_message})
#     bot_response = get_response(conversation)

#     # Save chat to Firestore
#     save_to_db(session_id, user_message, bot_response)

#     return jsonify({"response": bot_response, "session_id": session_id})

# @app.route('/get_chat_history', methods=['GET'])
# def get_chat_history():
#     session_id = request.args.get('session_id')
#     chats_ref = db.collection("chat_history").document(session_id).collection("chats").order_by("timestamp")
#     chats = chats_ref.stream()

#     history = [{"sender": "user" if chat.to_dict()["user_message"] else "bot", 
#                 "text": chat.to_dict()["user_message"] or chat.to_dict()["bot_message"]} for chat in chats]

#     return jsonify({"history": history})

# if __name__ == '__main__':
#     cleanup_old_chats()
#     app.run(debug=True)




#day wise data store but not in the user entered data

# import os
# import openai
# import uuid
# import firebase_admin
# from firebase_admin import credentials, firestore
# from dotenv import load_dotenv
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from datetime import datetime
# import pytz

# # Load environment variables
# load_dotenv()
# API_KEY = os.getenv("OPENAI_API_KEY")
# FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

# if not API_KEY or not FIREBASE_CREDENTIALS:
#     raise ValueError("Missing required environment variables")

# openai.api_key = API_KEY

# # Initialize Flask App
# app = Flask(__name__)
# CORS(app)

# # Initialize Firebase
# cred = credentials.Certificate(FIREBASE_CREDENTIALS)
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# # Time Management
# def get_ist_time():
#     return datetime.now(pytz.timezone("Asia/Kolkata"))

# def get_date_str():
#     """Get current date in YYYY-MM-DD format."""
#     return get_ist_time().strftime('%Y-%m-%d')

# # System Prompt
# system_prompt = """
# तुम्ही 'मनोदर्पण' मानसिक आरोग्य सहाय्यक आहात. तुमचा उद्देश वापरकर्त्यांची मानसिक स्थिती समजून त्यांना आधार देणे आहे. तुमचे उत्तर नेहमी मराठीत असले पाहिजे.
# """

# # OpenAI Chat Function
# def get_response(conversation):
#     response = openai.ChatCompletion.create(
#         model="gpt-4o-mini",
#         messages=conversation,
#         temperature=0.8
#     )
#     return response["choices"][0]["message"]["content"]

# # Save Chat to Firestore (Daily Document Structure)
# def save_to_db(session_id, user_message, bot_message):
#     date_str = get_date_str()
#     daily_doc_ref = db.collection("chat_history").document(session_id).collection("daily_chats").document(date_str)

#     daily_doc_ref.set({
#         "date": date_str,
#         "session_id": session_id,
#         "chats": firestore.ArrayUnion([
#             {
#                 "user_message": user_message,
#                 "bot_message": bot_message,
#                 "timestamp": get_ist_time().isoformat()
#             }
#         ])
#     }, merge=True)

# # Get Chat History from Firestore (All chats for the day)
# def get_session_history(session_id):
#     date_str = get_date_str()
#     daily_doc_ref = db.collection("chat_history").document(session_id).collection("daily_chats").document(date_str)
#     daily_doc = daily_doc_ref.get()

#     history = [{"role": "system", "content": system_prompt}]
#     if daily_doc.exists:
#         chats = daily_doc.to_dict().get("chats", [])
#         for chat in chats:
#             history.append({"role": "user", "content": chat["user_message"]})
#             history.append({"role": "assistant", "content": chat["bot_message"]})
    
#     return history

# # Store User Session
# def update_user_session(session_id, user_message):
#     session_ref = db.collection("user_sessions").document(session_id)
#     session_ref.set({"session_id": session_id}, merge=True)
#     session_ref.update({"messages": firestore.ArrayUnion([user_message])})

# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.json
#     session_id = data.get('session_id') or str(uuid.uuid4())
#     user_message = data.get('message')

#     # Update User Session
#     update_user_session(session_id, user_message)

#     # Get past chat history
#     conversation = get_session_history(session_id)
#     conversation.append({"role": "user", "content": user_message})
#     bot_response = get_response(conversation)

#     # Save chat to Firestore
#     save_to_db(session_id, user_message, bot_response)

#     return jsonify({"response": bot_response, "session_id": session_id})

# @app.route('/get_chat_history', methods=['GET'])
# def get_chat_history():
#     session_id = request.args.get('session_id')
#     date_str = request.args.get('date') or get_date_str()

#     daily_doc_ref = db.collection("chat_history").document(session_id).collection("daily_chats").document(date_str)
#     daily_doc = daily_doc_ref.get()

#     if daily_doc.exists:
#         chats = daily_doc.to_dict().get("chats", [])
#         history = [{"sender": "user", "text": chat["user_message"]} if chat["user_message"] else 
#                    {"sender": "bot", "text": chat["bot_message"]} for chat in chats]
#     else:
#         history = []

#     return jsonify({"history": history})

# if __name__ == '__main__':
#     app.run(debug=True)











# import os
# import openai
# import uuid
# import firebase_admin
# from firebase_admin import credentials, firestore
# from dotenv import load_dotenv
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from datetime import datetime
# import pytz

# # Load environment variables
# load_dotenv()
# API_KEY = os.getenv("OPENAI_API_KEY")
# FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

# if not API_KEY or not FIREBASE_CREDENTIALS:
#     raise ValueError("Missing required environment variables")

# openai.api_key = API_KEY

# # Initialize Flask App
# app = Flask(__name__)
# CORS(app)

# # Initialize Firebase
# cred = credentials.Certificate(FIREBASE_CREDENTIALS)
# firebase_admin.initialize_app(cred)
# db = firestore.client()

# # Time Management
# def get_ist_time():
#     return datetime.now(pytz.timezone("Asia/Kolkata"))

# def get_date_str():
#     return get_ist_time().strftime('%Y-%m-%d')

# # System Prompt
# system_prompt = """
# तुम्ही 'मनोदर्पण' मानसिक आरोग्य सहाय्यक आहात. तुमचा उद्देश वापरकर्त्यांची मानसिक स्थिती समजून त्यांना आधार देणे आहे. तुमचे उत्तर नेहमी मराठीत असले पाहिजे.
# """

# # OpenAI Chat Function
# def get_response(conversation):
#     response = openai.ChatCompletion.create(
#         model="gpt-4o-mini",
#         messages=conversation,
#         temperature=0.8
#     )
#     return response["choices"][0]["message"]["content"]

# # Save Chat to Firestore (Day-wise under user_sessions)
# def save_to_db(session_id, user_message, bot_message):
#     date_str = get_date_str()
#     daily_doc_ref = db.collection("user_sessions").document(date_str)

#     daily_doc_ref.set({
#         "date": date_str,
#         "chats": firestore.ArrayUnion([{
#             "session_id": session_id,
#             "user_message": user_message,
#             "bot_message": bot_message,
#             "timestamp": get_ist_time().isoformat()
#         }])
#     }, merge=True)

# # Get Chat History from Firestore
# def get_session_history(session_id):
#     date_str = get_date_str()
#     daily_doc_ref = db.collection("user_sessions").document(date_str)
#     daily_doc = daily_doc_ref.get()

#     history = [{"role": "system", "content": system_prompt}]
#     if daily_doc.exists:
#         chats = daily_doc.to_dict().get("chats", [])
#         for chat in chats:
#             if chat["session_id"] == session_id:
#                 history.append({"role": "user", "content": chat["user_message"]})
#                 history.append({"role": "assistant", "content": chat["bot_message"]})
    
#     return history

# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.json
#     session_id = data.get('session_id') or str(uuid.uuid4())
#     user_message = data.get('message')

#     conversation = get_session_history(session_id)
#     conversation.append({"role": "user", "content": user_message})
#     bot_response = get_response(conversation)

#     save_to_db(session_id, user_message, bot_response)

#     return jsonify({"response": bot_response, "session_id": session_id})

# @app.route('/get_chat_history', methods=['GET'])
# def get_chat_history():
#     date_str = request.args.get('date') or get_date_str()
#     daily_doc_ref = db.collection("user_sessions").document(date_str)
#     daily_doc = daily_doc_ref.get()

#     history = []
#     if daily_doc.exists:
#         chats = daily_doc.to_dict().get("chats", [])
#         history = [{"sender": "user", "text": chat["user_message"]} if chat["user_message"] else 
#                    {"sender": "bot", "text": chat["bot_message"]} for chat in chats]

#     return jsonify({"history": history})

# if __name__ == '__main__':
#     app.run(debug=True)



import os
import openai
import uuid
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import pytz

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")

if not API_KEY or not FIREBASE_CREDENTIALS:
    raise ValueError("Missing required environment variables")

openai.api_key = API_KEY

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Initialize Firebase
cred = credentials.Certificate(FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Time Management
def get_ist_time():
    return datetime.now(pytz.timezone("Asia/Kolkata"))

def get_date_str():
    """Get current date in YYYY-MM-DD format."""
    return get_ist_time().strftime('%Y-%m-%d')

# System Prompt
system_prompt = """
तुम्ही 'मनोदर्पण' मानसिक आरोग्य सहाय्यक आहात. तुमचा उद्देश वापरकर्त्यांची मानसिक स्थिती समजून त्यांना आधार देणे आहे. तुमचे उत्तर नेहमी मराठीत असले पाहिजे.

You are a friendly, compassionate mental health assistant designed to support users after they complete tests for depression and anxiety. Your primary tasks are to monitor their emotional well-being, provide thoughtful feedback, and offer helpful suggestions when needed.

Your Responsibilities:
1️ **Daily Check-ins:**  
   - Greet the user warmly and ask about their day.  
   - Use open-ended, non-judgmental questions like:  
     "How are you feeling today?"  
     "What was the best part of your day?"  

2️ **Emotional Analysis:**  
   - Detect signs of depression or anxiety.  
   - Track changes in mood over time.  

3️ **Providing Support:**  
   - Offer empathetic, supportive responses.  
   - Suggest healthy coping mechanisms.  

4️ **Encouraging Positive Habits:**  
   - Recommend journaling, mindfulness, sleep, and exercise.  
   - Suggest breathing exercises for anxiety.  

5️ **Recognizing Urgent Situations:**  
   - If severe distress is detected, recommend seeking professional help.  
   - Example: "I'm sorry you're feeling this way. It might help to talk to a trusted person or professional."  

 **Remember:** You are a supportive companion, not a replacement for professional therapy.
 also give all the responses in Marathi language
 when you are asked who are you should ans " "Hello! I am your personal mental health assistant "Manodarpan", here to support and guide you. I can help you track your mental well-being, assess your mood, suggest self-care tips, and connect you with professionals if needed. Feel free to share how you're feeling, and I'll do my best to assist you!" 
"""

# OpenAI Chat Function
def get_response(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=conversation,
        temperature=0.8
    )
    return response["choices"][0]["message"]["content"]

# Store User Entered Messages in user_sessions (Day-wise)
def save_user_session(session_id, user_message):
    date_str = get_date_str()
    user_session_ref = db.collection("user_sessions").document(date_str)
    user_session_ref.set({
        "date": date_str,
        "user_messages": firestore.ArrayUnion([{
            "session_id": session_id,
            "user_message": user_message,
            "timestamp": get_ist_time().isoformat()
        }])
    }, merge=True)

# Store Full Chat (User + Bot) in chat_history (Day-wise)
def save_chat_history(session_id, user_message, bot_message):
    date_str = get_date_str()
    chat_history_ref = db.collection("chat_history").document(date_str)
    chat_history_ref.set({
        "date": date_str,
        "chats": firestore.ArrayUnion([{
            "session_id": session_id,
            "user_message": user_message,
            "bot_message": bot_message,
            "timestamp": get_ist_time().isoformat()
        }])
    }, merge=True)

# Get Chat History from chat_history
def get_session_history(session_id):
    date_str = get_date_str()
    chat_history_ref = db.collection("chat_history").document(date_str)
    chat_doc = chat_history_ref.get()

    history = [{"role": "system", "content": system_prompt}]
    if chat_doc.exists:
        chats = chat_doc.to_dict().get("chats", [])
        for chat in chats:
            if chat["session_id"] == session_id:
                history.append({"role": "user", "content": chat["user_message"]})
                history.append({"role": "assistant", "content": chat["bot_message"]})
    return history

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get('session_id') or str(uuid.uuid4())
    user_message = data.get('message')

    # Store User Message in user_sessions
    save_user_session(session_id, user_message)

    # Get Conversation History and Generate Bot Response
    conversation = get_session_history(session_id)
    conversation.append({"role": "user", "content": user_message})
    bot_response = get_response(conversation)

    # Store Full Chat (User + Bot) in chat_history
    save_chat_history(session_id, user_message, bot_response)

    return jsonify({"response": bot_response, "session_id": session_id})

@app.route('/get_chat_history', methods=['GET'])
def get_chat_history():
    date_str = request.args.get('date') or get_date_str()
    chat_history_ref = db.collection("chat_history").document(date_str)
    chat_doc = chat_history_ref.get()

    history = []
    if chat_doc.exists:
        chats = chat_doc.to_dict().get("chats", [])
        history = [
            {"sender": "user", "text": chat["user_message"]} if chat["user_message"] else 
            {"sender": "bot", "text": chat["bot_message"]}
            for chat in chats
        ]

    return jsonify({"history": history})

if __name__ == '__main__':
    app.run(debug=True)
