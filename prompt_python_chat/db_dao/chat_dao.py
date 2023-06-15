from typing import Optional,List
from prompt_python_chat.db_models import ChatMessage
from .base_dao import BaseDao
from prompt_python_chat.constants import ColorType
from sqlalchemy import select,desc,delete


class ChatDao(BaseDao):
    
     def _return_message(self,chat_message:ChatMessage) -> dict:
          return {
               "id":chat_message.id,
               "user_id":chat_message.user_id,
               "channel_id":chat_message.channel_id,
               "nickname":chat_message.nickname,
               "content":chat_message.content,
               "color":chat_message.color.value,
               "index":chat_message.channel_msg_index,
               "timestamp":str(chat_message.timestamp)
          }
     
     def get_message_object_by_id(self,message_id:int) -> Optional[ChatMessage]:
          return self.get_session().scalars(select(ChatMessage).where(ChatMessage.id == message_id)).one_or_none()
          
     def post_message(self,channel_id:int , user_id:int ,nickname:str, content:str,color:ColorType) -> Optional[dict]:
          msg_id = self.generate_id()
          last_msg = self.get_session().scalar(select(ChatMessage).order_by(desc(ChatMessage.channel_msg_index)).limit(1))
          last_index = 0
          if last_msg:
               last_index = last_msg.channel_msg_index + 1
          new_msg = ChatMessage(id=msg_id,channel_msg_index=last_index,channel_id=channel_id,user_id=user_id,nickname=nickname,content=content,color=color)
          self.get_session().add(new_msg)
          self.get_session().commit()
          msg = self.get_message_object_by_id(msg_id)
          if msg:
               return self._return_message(msg)

     def get_channel_object_messages(self, channel_id:int) -> List[ChatMessage]:
          return list(self.get_session().scalars(select(ChatMessage).where(ChatMessage.channel_id == channel_id).order_by(ChatMessage.channel_msg_index)).all())

     def get_channel_messages(self, channel_id:int) -> List[dict]:
          return [self._return_message(message) for message in self.get_channel_object_messages(channel_id)]
    
     def delete_all_message(self) -> Optional[List[ChatMessage]]:
          msgs = list(self.get_session().scalars(select(ChatMessage)).all())
          msgs_ids = []
          deleted_msgs = []
          for msg in msgs:
              deleted_msgs.append(msg)
              msgs_ids.append(msg.id)
              self.get_session().delete(msg)
          self.get_session().commit()     
          for msg_id in msgs_ids:
               if self.get_message_object_by_id(msg_id):
                    #self.get_session().rollback()
                    return 
          return deleted_msgs

     def delete_channel_messages(self,channel_id:int):
          result = self.get_session().execute(delete(ChatMessage).where(ChatMessage.channel_id == channel_id).returning(ChatMessage.id))
          return result




chat_dao = ChatDao()