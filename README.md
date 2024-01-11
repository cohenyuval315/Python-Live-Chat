# Project Overview
Live Terminal Chat Rooms written in Python, based on Asynchronous Client-Server architecture. The development stack incorporates aiohttp, prompt-toolkit, and SQLAlchemy for seamless integration with both SQLite and PostgreSQL databases.

# Project objective
The goal is to create a concise yet robust project with clear software layers, specifically designing an interactive chat platform for local area network (LAN) use. The focus is on providing essential features for user management, such as role permissions, moderation capabilities (ban, silence, unban), and channel administration. This ensures control over the chat environment, making it suitable for diverse users while preventing misuse.

# Project Timeline
- Anticipated total work hours: Approximately 35 hours
- Adjustments: 6 additional man-hours
  
# Project Components:
- Graphical User Interface (GUI) - ChannelWindow utilizing prompt-toolkit
- Presentation Logic - Implementation of Asynchronous Client Managers
- Server Endpoints
- Controllers for effective interaction
- Services - Implementing Business Logic
- Data Access Layer (DAO) - Incorporating the repository pattern, and bridge with SQLite, PostgreSQL,  provided by SQLAlchemy 
- Definition of Entities

## key features:
- Authentication and anonymous login.
- Real-time chat updates to enhance user engagement.
- Role-based permission hierarchy for streamlined access control.
- Administrative operations to manage the system.
- Moderator operations for efficient content moderation.
- Online status service for users and channels visibility.

# Project Setup
## server setup
```
docker compose up server --build
```

## client setup
1. Establish a virtual environment
```code
python -m venv ./venv
```

2. Activate the virtual environment
  - unix :
      ```code
        source ./venv/bin/activate
      ``` 
  - windows :
      ```code
        ./venv/Scripts/activate
      ```

3. Install dependencies from requirements.txt
 ```
   pip install -r requirements.txt
 ```
4. Execute and re-run the application, utilizing the configuration provided by the Click library.
```
  python main.py
```

# Project Preview
## Lobby View
![LiveChat3](https://github.com/cohenyuval315/Python-Live-Chat/assets/61754002/fec6e847-196b-4464-ba7d-f5b1c441cf1f)

## Inside ChatRoom
![LiveChat1](https://github.com/cohenyuval315/Python-Live-Chat/assets/61754002/87a0d986-09d5-49c6-b9a7-6b04887d9a3c)

## Permissions In Chatroom
![LiveChat2](https://github.com/cohenyuval315/Python-Live-Chat/assets/61754002/f5803d8c-fe86-4b03-b4fa-3da6a7517d57)


