from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from . import mongo

class User:
    """User model for handling user-related operations"""
    
    def __init__(self, username, email, password, nickname=None):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.nickname = nickname
        self.created_at = datetime.utcnow()
    
    @staticmethod
    def create_user(username, email, password, nickname=None):
        """Create a new user"""
        user = User(username, email, password, nickname)
        user_data = {
            'username': user.username,
            'email': user.email,
            'password': user.password_hash,
            'nickname': user.nickname,
            'created_at': user.created_at
        }
        result = mongo.db.users.insert_one(user_data)
        return result.inserted_id
    
    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        return mongo.db.users.find_one({'username': username})
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        return mongo.db.users.find_one({'email': email})
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        return mongo.db.users.find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def verify_password(username, password):
        """Verify password for given username"""
        user = User.get_by_username(username)
        if user and check_password_hash(user['password'], password):
            return True
        return False
    
    @staticmethod
    def update_profile(username, update_data):
        """Update user profile"""
        # Don't allow username or password updates through this method
        safe_data = {k: v for k, v in update_data.items() 
                    if k not in ['username', 'password', '_id']}
        
        result = mongo.db.users.update_one(
            {'username': username},
            {'$set': safe_data}
        )
        return result.modified_count > 0

class Message:
    """Message model for handling chat messages"""
    
    def __init__(self, content, sender_username, room_id, message_type='text'):
        self.content = content
        self.sender_username = sender_username
        self.room_id = room_id
        self.message_type = message_type
        self.timestamp = datetime.utcnow()
    
    @staticmethod
    def create_message(content, sender_username, room_id, message_type='text'):
        """Create a new message"""
        message = Message(content, sender_username, room_id, message_type)
        message_data = {
            'content': message.content,
            'sender_username': message.sender_username,
            'room_id': message.room_id,
            'message_type': message.message_type,
            'timestamp': message.timestamp
        }
        result = mongo.db.messages.insert_one(message_data)
        return result.inserted_id
    
    @staticmethod
    def get_room_messages(room_id, limit=50):
        """Get messages for a specific room"""
        return list(mongo.db.messages.find(
            {'room_id': room_id}
        ).sort('timestamp', -1).limit(limit))

class Room:
    """Room model for handling chat rooms"""
    
    def __init__(self, name, created_by, is_private=False):
        self.name = name
        self.created_by = created_by
        self.is_private = is_private
        self.created_at = datetime.utcnow()
        self.members = [created_by]  # List of usernames
    
    @staticmethod
    def create_room(name, created_by, is_private=False):
        """Create a new room"""
        room = Room(name, created_by, is_private)
        room_data = {
            'name': room.name,
            'created_by': room.created_by,
            'is_private': room.is_private,
            'created_at': room.created_at,
            'members': room.members
        }
        result = mongo.db.rooms.insert_one(room_data)
        return result.inserted_id
    
    @staticmethod
    def get_room(room_id):
        """Get room by ID"""
        return mongo.db.rooms.find_one({'_id': ObjectId(room_id)})
    
    @staticmethod
    def get_user_rooms(username):
        """Get all rooms for a user"""
        return list(mongo.db.rooms.find({'members': username}))
    
    @staticmethod
    def add_member(room_id, username):
        """Add a member to a room"""
        result = mongo.db.rooms.update_one(
            {'_id': ObjectId(room_id)},
            {'$addToSet': {'members': username}}
        )
        return result.modified_count > 0