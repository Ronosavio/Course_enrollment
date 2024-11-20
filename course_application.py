import json
import os
from abc import ABC, abstractmethod
import smtplib
from email.message import EmailMessage
from pydantic import BaseModel, SecretStr, ValidationError, EmailStr, field_validator
import getpass
import keyboard

#NOTICE : I HAVEN'T FINISHED THE COMPLETE WORKING OF THIS CODE.IT STILL WORKS BUT I DO HAVE THINGS TO ADD UP TO IT.

class Courses(ABC):
      @abstractmethod
      def course(username):
          pass
      
class Machine_learning(Courses):
      count = 0
      def course(username):
          with open('course_enrollment/course_modules_Machine_Learning/machine_learning_module1.txt', 'r') as file:
               print("\n\n\t\t***MODULE ONE****(X -> exit course)\t\t\n\n")
               data = file.read()  # Reads the entire file
               print(data)
          
          question = input("\nWould you like to continue to the next module?:\t")
          if question.lower() == 'y':
            return Machine_learning.module2(username)
          if question.lower() == 'n':
             return Machine_learning.course(username) 
          keyboard.add_hotkey('x', Machine_learning.exit_course(username))

      def module2(username):
          with open('course_enrollment/course_modules_Machine_Learning/machine_learning_module2.txt', 'r') as file:
               print("\n\n\t\t***MODULE TWO****(X -> exit course)\t\t\n\n")
               data = file.read()  # Reads the entire file
               print(data)
          question = (input("\nWould you like to go back to the previous  module?:\t"))
          if question.lower() == 'y':
            return Machine_learning.course(username)
          if question.lower() == 'n':
            return Machine_learning.module2(username)
          keyboard.add_hotkey('x', Machine_learning.exit_course(username))   

      def exit_course(username):
          print("\nExiting the current module...")
          return Allotment.course_registration(username)
      @classmethod
      def get_Machine_learning_count(cls):
          return cls.count

class Data_Science(Courses): 
      count = 0 
      def course(username):
          with open('course_enrollment/course_modules_Data_Science/module_1.txt', 'r') as file:
               print("\t\t\n\n***MODULE ONE****(X -> exit course)\t\t\n\n")
               data = file.read()  # Reads the entire file
               print(data)
    # Add a hotkey listener for 'X' to trigger exit_course
          question = input(f"\n{username}, would you like to continue to the next module ?:\t")
          if question.lower() == 'y':
            return Machine_learning.module2(username)
          if question.lower() == 'n':
             return Machine_learning.course(username)
          keyboard.add_hotkey('x', Data_Science.exit_course(username))

      def module2(username):
          with open('course_enrollment/course_modules_Data_Science/module_2.txt', 'r') as file:
               print("\n\n\t\t***MODULE TWO****(X -> exit course)\t\t\n\n")
               data = file.read()  # Reads the entire file
               print(data)
          question = (input("\nWould you like to go back to the previous  module?:\t"))
          if question.lower() == 'y':
            return Data_Science.course(username)   
          if question.lower() == 'n':
             return Data_Science.module2(username)
          keyboard.add_hotkey('x', Machine_learning.exit_course(username))

      def exit_course(username):
          print("\nExiting the current course...")
          return Allotment.course_registration(username)
    
      @classmethod
      def get_Data_Science_count(cls):
          return cls.count

    
class Login:
      username = str
      password = str

      def sign_in():
          print("\n\t\tLOGIN\t\t\n")
          username = input("USER_NAME: \t")
          if username.lower() == 'x':
             return Login.exit_login()
          if Login.is_username_matching(username) == True: 
             password = input("PASSWORD: \t")
             if Login.password_validator(username, password) == True:
                print("\n\t\tLOGIN SUCCESSFUL\t\t\n")
                return username
             else: 
                 print("\n**Wrong password**\n")
                 return Login.sign_in()
          else:
               print("\n**Username does not exist**\n")
               return Login.sign_in()

  
      def is_username_matching(username: str, file_path: str = 'course_enrollment/Registered_users.json') -> bool:
          if not os.path.exists(file_path):
              return False
          with open(file_path, 'r') as f:
              try:
                  users_data = json.load(f)
              except json.JSONDecodeError:
                  return False 
          for user in users_data.get("users", []):
              if user['username'] == username:
                 return True   
          return False

      def password_validator(username: str, password: str, file_path: str = 'course_enrollment/Registered_users.json') -> bool:
          if not os.path.exists(file_path):
              return False
          # Load existing data from JSON file
          with open(file_path, 'r') as f:
              try:
                  users_data = json.load(f)
              except json.JSONDecodeError:
                  return False 
          for user in users_data.get("users", []):
              if user['username'] == username and user['password'] == password:
                 return True   
          return False
          
      @staticmethod
      def exit_login():
          print("\nLOGIN PORTAL ABORTED\n")
          return start()


class Allotment():
      def course_registration(user_login):
          course = input("Select the course you want to enroll in : \n1.MACHINE LEARNING\n2.DATA SCIENCE\n(1/2):\t") 
          if course == '1':
             return Machine_learning.course(user_login)
          elif course == '2':
             return Data_Science.course(user_login)
          elif course.lower() == 'x':
             return Allotment.exit_course(user_login)
          else: 
             print("\nINVALID CHOICE\n")
             return Allotment.course_registration(user_login)
             
      def exit_course(username):
          print(f"\nUSER:{username}-> LOGGING  OUT...\n\n")
          return start()

    
          
class Registration(BaseModel):  
    username : str
    password : SecretStr
    email : EmailStr
    
    @staticmethod
    def register(user_register):
        user_details = Registration.to_dict(user_register)
        try:
            with open('course_enrollment/Registered_users.json', 'r') as json_file:
                users_data = json.load(json_file)
        except FileNotFoundError:
            users_data = {"users": []}
        # Append new user details to the users list
        users_data["users"].append(user_details)
        # Write updated data back to the file
        with open('course_enrollment/Registered_users.json', 'w') as json_file:
            json.dump(users_data, json_file, indent=4)
        Registration.send_registration_notification(user_register.email, user_register.username)

        print(f"Username: {user_register.username}")
        print(f"Email: {user_register.email}")
        print(f"Password (hidden): {user_register.password}")

    @staticmethod
    def get_user_credentials():
        print("\n\t\t********REGISTER******(x -> exit)\n")
        username = input("\nEnter your username:\t ")
        if username.lower() == 'x':
            return Registration.exit_registration()

        if Registration.is_username_taken(username):
            print("\nOOPS..User already exists")
            return Registration.get_user_credentials()

        email = input("Enter your email:\t")
        password = getpass.getpass("Enter your password:\t")

        try:
            user = Registration(username=username, email=email, password=password)
            return user
        except ValidationError as e:
            print(f"Validation error: {e}")
            return Registration.get_user_credentials()

    @staticmethod
    def is_username_taken(username: str, file_path: str = 'course_enrollment/Registered_users.json') -> bool:
        if not os.path.exists(file_path):
            return False
        # Load existing data from JSON file
        with open(file_path, 'r') as f:
            try:
                users_data = json.load(f)
            except json.JSONDecodeError:
                return False
        
        for user in users_data.get("users", []):
            if user['username'] == username:
                return True
        return False

    @field_validator('password')
    def validate_password(cls, value: SecretStr):
        password = value.get_secret_value()
        # Minimum length
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        # At least one uppercase letter
        if not any(char.isupper() for char in password):
            raise ValueError('Password must contain at least one uppercase letter')
        # At least one lowercase letter
        if not any(char.islower() for char in password):
            raise ValueError('Password must contain at least one lowercase letter')
        # At least one digit
        if not any(char.isdigit() for char in password):
            raise ValueError('Password must contain at least one digit')
        # At least one special character
        if not any(char in "@$!%*?&#" for char in password):
            raise ValueError('Password must contain at least one special character (@$!%*?&#)')
        return value  

    @field_validator('email')
    def check_custom_email_domain(cls, value: EmailStr):
        if not value.endswith('@gmail.com'):
            raise ValueError('Email must be from the domain @gmail.com only\n')
        return value

    @staticmethod
    def send_registration_notification(email: str, username: str):
        msg = EmailMessage()
        msg['Subject'] = 'REGISTRATION NOTIFICATION'
        msg['From'] = 'courseregister483@gmail.com'  
        msg['To'] = email
        msg.set_content(f"Hello {username},\n\nYou have successfully registered into your Course Application\n\n HAPPY LEARNING....")

        # SMTP server setup and sending the email
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp: 
                smtp.login('courseregister483@gmail.com', 'jthx gjsh lebt oxcd') 
                smtp.send_message(msg)
                print(f"\n********REGISTRATION SUCCESSFUL*******\n\t\t ( @ {email} )\n")
        except Exception as e:
            print(f"Failed to send email: {e}\n Check your network connection")
            return Registration.get_user_credentials()

    def to_dict(self):
        return {
            'username' : self.username,
            'email' : self.email,
            'password' : self.password.get_secret_value()     
        }

    @staticmethod
    def exit_registration():
        print("\nREGISTRATION PORTAL ABORTED\n")
        return start()


def start():
    
    print("\n\n\t\tWELCOME TO COURSE ENROLLMENT PLATFORM\n\n")
    option = input("\nREGISTRATION OR LOGIN? (or 'x' to exit)\n")
    
    if option.lower() == 'x':
        print("\nEXITING PLATFORM\n")
        input()
        return
    elif option.lower() == 'registration':
        Registration.register(Registration.get_user_credentials())
        user_login = Login.sign_in()
        Allotment.course_registration(user_login)
    elif option.lower() == 'login':
        user_login = Login.sign_in()
        Allotment.course_registration(user_login)
    else:
        print("\nInvalid option! Please try again.")
        return start()


if __name__ == '__main__':
   start()