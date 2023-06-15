from prompt_python_chat.db_models import Permission,Role,User,Channel,ChatMessage
from prompt_python_chat.constants import RoleType,ColorType
from uuid import uuid4 as v4
import bcrypt
class MetaData():
    DB_DELETE_CHATS = "db_delete_chats" 
    DB_DELETE_CHANNEL_MSGS = "db_delete_channel_msgs"
    DB_GET_USERS = "db_get_all_users"
    DB_UPDATE_USER_ROLE = "db_update_user_role"
    DB_DELETE_USER = "db_delete_user"
    DB_POST_BLOCK = "db_create_block"
    DB_DELETE_BLOCK = "db_delete_block"
    DB_POST_CHANNEL = "db_create_channel"
    DB_DELETE_CHANNEL = "db_delete_channel"
    DB_UPDATE_CHANNEL_NAME = "db_update_channel_name"
    DB_UPDATE_CHANNEL_ROLE = "db_update_channel_role"
    DB_CLEAR = "db_delete_all_msgs"


    def _generate_id(self) -> int:
        return int(str(v4().int)[:16])

    
    def __init__(self,session) -> None:
        self._session = session
        self.admin_role_id = self._generate_id()
        self.mod_role_id = self._generate_id()
        self.user_role_id = self._generate_id()
        self.guest_role_id = self._generate_id()


    def __init_admin_permissions(self):
        p1 = Permission(id=self._generate_id(),name=self.DB_DELETE_CHATS,role_id=self.admin_role_id)
        p2 = Permission(id=self._generate_id(),name=self.DB_DELETE_CHANNEL_MSGS,role_id=self.admin_role_id)
        p3 = Permission(id=self._generate_id(),name=self.DB_GET_USERS,role_id = self.admin_role_id)
        p4 = Permission(id=self._generate_id(),name=self.DB_UPDATE_USER_ROLE,require_target=True,role_id = self.admin_role_id)
        p5 = Permission(id=self._generate_id(),name=self.DB_DELETE_USER,require_target=True,role_id = self.admin_role_id)
        p6 = Permission(id=self._generate_id(),name=self.DB_CLEAR,role_id=self.admin_role_id)
        self._session.add_all([p1,p2,p3,p4,p5,p6])

    def __init_moderator_permissions(self):
        p6 = Permission(id=self._generate_id(),name=self.DB_POST_BLOCK,role_id=self.mod_role_id)
        p7 = Permission(id=self._generate_id(),name=self.DB_DELETE_BLOCK,role_id=self.mod_role_id)
        p8 = Permission(id=self._generate_id(),name=self.DB_POST_CHANNEL,role_id=self.mod_role_id)
        p9 = Permission(id=self._generate_id(),name=self.DB_DELETE_CHANNEL,role_id=self.mod_role_id)
        p10 = Permission(id=self._generate_id(),name=self.DB_UPDATE_CHANNEL_NAME,role_id=self.mod_role_id)
        p11 = Permission(id=self._generate_id(),name=self.DB_UPDATE_CHANNEL_ROLE,role_id=self.mod_role_id)
        
        self._session.add_all([p6,p7,p8,p9,p10,p11])

    def __init_user_permissions(self):
        pass

    def __init_guest_permissions(self):
        pass

    def _init_permissions(self):
        self.__init_admin_permissions()
        self.__init_moderator_permissions()
        self.__init_user_permissions()
        self.__init_guest_permissions()

    def _init_roles(self):
        AdminRole = Role(id=self.admin_role_id,name=RoleType.ADMIN.value,color=ColorType.RED)    
        ModeratorRole = Role(id=self.mod_role_id,name=RoleType.MOD.value, child_role_id=self.admin_role_id,color=ColorType.BLUE)    
        UserRole = Role(id=self.user_role_id,name=RoleType.USER.value,child_role_id=self.mod_role_id,color=ColorType.PINK) 
        GuestRole = Role(id=self.guest_role_id,name=RoleType.GUEST.value,child_role_id=self.user_role_id,color=ColorType.WHITE)
        self._session.add(AdminRole)
        self._session.add(UserRole)
        self._session.add(ModeratorRole)
        self._session.add(GuestRole)
        self._session.commit()        

        
    def _init_channels(self):
        all_channel = Channel(id=self._generate_id(),name="all",role_id=self.guest_role_id,color=ColorType.WHITE)
        user_channel = Channel(id=self._generate_id(),name="user_only",role_id=self.mod_role_id,color=ColorType.PINK)
        mod_channel = Channel(id=self._generate_id(),name="mod_only",role_id=self.mod_role_id,color=ColorType.BLUE)
        admin_channel = Channel(id=self._generate_id(),name="admin_only",role_id= self.admin_role_id,color=ColorType.RED)
        self._session.add_all([all_channel,user_channel,mod_channel,admin_channel])

    def _encrypt_pass(self,password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def _init_admins(self):
        admin_user = User(id=self._generate_id(),username="admin",password=self._encrypt_pass("admin"),nickname="admin1",role_id=self.admin_role_id)
        self._session.add(admin_user)

    def _init_moderators(self):
        moderator_user = User(id=self._generate_id(),username="mod",password=self._encrypt_pass("mod"),nickname="mod1",role_id = self.mod_role_id)
        self._session.add(moderator_user)
    
    def _init_users(self):
        normal_user = User(id=self._generate_id(),username="user",password=self._encrypt_pass("user"),nickname="user1",role_id=self.user_role_id)
        self._session.add(normal_user)

    def init_data(self):
        self._init_roles()
        self._init_permissions()
        self._init_admins()
        self._init_moderators()
        self._init_users()
        self._init_channels()
        self._session.commit()

