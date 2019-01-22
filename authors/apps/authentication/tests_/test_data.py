
responses = {
    'test_login_with_invalid_user_fails':{
            "errors": {
                "error": [
                    "A user with this email and password was not found."
                ]
            }
        },
        
    'invalid_username':{
        "errors":{
            "username": [
                "Username cannot contain special characters."
            ]
        }
    },

    'numeric_first_char_username':{
        "errors":{
            "username": [
                "Username must start with a letter."
            ]
        }
    },

    'short_username':{
        "errors":{
            "username": [
                "Username must be longer than 5 characters."
            ]
        }
    },
    
    'test_login_with_missing_email_fails': {
            "errors": {
                "error": [
                    "A user with this email and password was not found."
                ]
            }
        },
    'email_already_exists':{
            "errors": {
                "email": [
                    "Email already exists."
                ]
            }
        },
    'password_is_too_short': {
            "errors": {
                "password": [
                    "Password must be longer than 8 characters."
                ]
            }
        },
    'password_is_weak':  {
            "errors": {
                "password": [
                    "Password should at least contain a number, capital and small letter."
                ]
            }
        },
    'username_already_exists': {
            "errors": {
                "username": [
                    "Username already exists."
                ]
            }
        }
        
}

invalid_user_data = {
    'invalid_username': {
            "user": {
                "username": "Jac  @ob",
                "email": "jake@jake.jake",
                "password": "JakeJake12"
            }
        }, 

    'weak_password':{
            "user": {
                "username": "Jacob",
                "email": "jake@jake.jake",
                "password": "jakejake"
            }
        }, 

    'short_password': {
            "user": {
                "username": "Jacob",
                "email": "jake@jake.jake",
                "password": "jake"
            }
        }, 

    'same_email_user': {
            "user": {
                "username": "Jackson",
                "email": "jake@jake.jake",
                "password": "jAckson5"
            }
        }, 

    'same_username_user' : {
            "user": {
                "username": "Jacob",
                "email": "jake@gmail.com",
                "password": "jAcobson10"
            }
        }, 
    'short_username' : {
            "user": {
                "username": "J",
                "email": "jake@gmail.com",
                "password": "jAcobson10"
            }
        }, 

    'numeric_first_char_username' :{
        "user": {
                "username": "12jake",
                "email": "jake@gmail.com",
                "password": "jAcobson10"
            }
    },
    'not_author_login_credentials':{
            "user":{
                "email":"notauthor@author.com",
                "password":"NotAuthoruser12"
            }
        }

    }

comment_data={
   'comment_data':{
            'body':'a test comment body'
        },
        
    'comment_update':{
            'body':'a test comment body updated'
        }

    }
commentReply_data={
    'reply_data':{
        "reply_body":"a test comment reply body"
    },
    "reply_update_data":{
        "reply_body":"a test comment reply update body"
    }
}