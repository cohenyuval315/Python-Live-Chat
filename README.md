# Python-Live-Chat
A Async Client Server Live Chat project
using SQLAlchemy, aiohttp, prompt-toolkit

- project length: 2 weeks

The Project divides into layer application:
1. Presentation(GUI) - https://github.com/cohenyuval315/Python-Live-Chat/tree/main/prompt_python_chat/client/view/channel_window.py
2. Presentation Logic - https://github.com/cohenyuval315/Python-Live-Chat/tree/main/prompt_python_chat/client/
3. Routes - https://github.com/cohenyuval315/Python-Live-Chat/tree/main/prompt_python_chat/routes
4. Controller - https://github.com/cohenyuval315/Python-Live-Chat/tree/main/prompt_python_chat/controllers
5. Services - https://github.com/cohenyuval315/Python-Live-Chat/tree/main/prompt_python_chat/service
6. DAO layer - https://github.com/cohenyuval315/Python-Live-Chat/tree/main/prompt_python_chat/db_dao
7. DB models - https://github.com/cohenyuval315/Python-Live-Chat/tree/main/prompt_python_chat/db_models 

## features:
- each user type chat commands
- channels with constraints
- anoynymous login
- real live chat updating
- handles multiple clients
- terminal gui
- role permission hierachy
- admin operations
- mod operations
- authentication
- online service

---
**role permission hierachy** : four types of users(each user type has all operations available from the user types under him):
  1. Admin:
     - can enter admin channels
     - can promote a user to be mod
     - can demote mod to be user
     - can clean channel messages from db
     - can promote channel for admins only
     - can demote channel from admins only
     - can create admin channel
     - can delete admin channel
       
  3. Mod
     - can enter mod channels
     - can mute user in chosen channels
     - can unmute user in chosen channels
     - can ban user in chosen channels
     - can unban user in chosen channels
     - can create mod/user/free-for-all channel
     - can delete mod/user/free-for-all channel
     
  5. User
     - can enter user channels
     - can create user channel
     - can create free-for-all channel
       
  6. Guest(Anonymous)
     - /help for help
     - /lobby for lobby chat
     - /clear for cleaning current chat visually
     - /exit exiting the application
     - can change channel
     - has self lobby chat
     - can enter guest channels



# setup
1. create virtual environment
```code
python -m venv ./venv
```

2. activate venv
  - unix :
      ```code
        source ./venv/bin/activate
      ``` 
  - windows :
      ```code
        ./venv/Scripts/activate
      ```
3. setup.py
```code
pip -e setup.py
```

4. libs
```code
pip install -r requirement.txt
```

5. env file
- enter your configuration in this file format and change file name to .env  
https://github.com/cohenyuval315/Python-Live-Chat/blob/main/prompt_python_chat/env_example.txt

6. start server
```code
  python promopt_python_chat/server.py
```
![image](https://github.com/cohenyuval315/Python-Live-Chat/assets/61754002/093ad4a4-0f7e-402a-b483-1e1337988478)


7. start client
```code
  python promopt_python_chat/client/client.py # start one client
```
![image](https://github.com/cohenyuval315/Python-Live-Chat/assets/61754002/2c82d882-c480-429d-9c33-d15eb0d86d9b)


# Preview
![image](https://github.com/cohenyuval315/python_terminal_prompt_server_clients_live_chat/assets/61754002/bc126ede-ea44-43d8-b587-4370cc9145d3)
