
responses = {
    'test_login_with_invalid_user_fails':{
            "errors": {
                "error": [
                    "A user with this email and password was not found."
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