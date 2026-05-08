from supabase import Client
from typing import List, Dict, Any
from postgrest import APIResponse

class UserChatModel:
    def __init__(self, client: Client) -> None:
        self.client = client
        self.table_name = "user_chat"

    def link_chat_to_user(self, user_id: str, chat_id: int, title: str = "Новый чат") -> APIResponse:
        data = {
            "user_id": user_id,
            "chat_id": chat_id,
            "title": title
        }
        return (
            self.client
            .table(self.table_name)
            .insert(data)
            .execute()
        )
    
    def get_user_chat_list(self, user_id: str) -> List[Dict[str, Any]]:
        result = (
            self.client
            .table(self.table_name)
            .select("id, chat_id, title")
            .eq("user_id", user_id)
            .order("id", desc=True)
            .execute()
        )
        return result.data
    
    def find_user_chat_by_title(self, user_id: str, title: str = "Новый чат") -> List[Dict[str, Any]]:
        result = (
            self.client
            .table(self.table_name)
            .select("id, chat_id, title")
            .eq("user_id", user_id)
            .eq("title", title)
            .execute()
        )
        return result.data
    
    def update_chat_title(self, user_chat_id: int, new_title: str) -> APIResponse:
        return (
            self.client
            .table(self.table_name)
            .update({"title": new_title})
            .eq("id", user_chat_id)
            .execute()
        )