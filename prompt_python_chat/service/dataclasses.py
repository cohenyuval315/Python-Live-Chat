import dataclasses

@dataclasses.dataclass
class OnlineUser:
    user_id:int
    nickname:str
    color:str
    def __eq__(self, other) -> bool:
        if not isinstance(other, OnlineUser):
            return False
        if self.user_id != other.user_id:
            return False
        if self.nickname != other.nickname:
            return False
        return True

    def __hash__(self):
        return hash(id(self))
    

@dataclasses.dataclass
class OnlineChannel:
    online:bool
    channel_id:int
    name:str
    color:str
    users:set

    def __eq__(self, other) -> bool:
        if not isinstance(other, OnlineChannel):
            return False
        if self.channel_id != other.channel_id:
            return False
        if self.name != other.name:
            return False
        return True

    def __hash__(self):
        return hash(id(self))
    
    def add_user(self,user:OnlineUser):
        self.users.add(user)    
        return True

    def remove_user_by_id(self,user_id:int):
        for user in self.users.copy():
            if not isinstance(user,OnlineUser):
                raise Exception("user must be Online user type")
            if user_id == user.user_id:
                self.users.remove(user)
                return True           
        return False

    def remove_user_by_nickname(self,nickname:str):
        for user in self.users.copy():
            if not isinstance(user,OnlineUser):
                raise Exception("user must be Online user type")
            if nickname == user.nickname:
                self.users.remove(user)
                return True           
        return False

    def set_name(self, name:str):
        self.name = name

    def set_online(self, status:bool):
        self.online = status
