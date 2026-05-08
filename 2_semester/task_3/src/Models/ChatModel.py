from supabase import Client
from typing import List, Dict, Any
from postgrest import APIResponse

class ChatModel:
    def __init__(self, client: Client) -> None:
        self.client = client
        self.table_name = "chat"

    def create_empty_chat(self) -> int:
        result = self.client.table("chat").insert({"messeges": []}).execute()
        return result.data[0]["id"]

    def get_messages(self, chat_id: int) -> List[Dict[str, Any]]:
        result = (
            self.client
            .table(self.table_name)
            .select("messeges")
            .eq("id", chat_id)
            .single()
            .execute()
        )
        return result.data.get("messeges", [])

    def update_messages(self, chat_id: int, messages: List[Dict[str, Any]]) -> APIResponse:
        return (
            self.client
            .table(self.table_name)
            .update({"messeges": messages})
            .eq("id", chat_id)
            .execute()
        )

    def delete_user_chat(self, chat_id: int) -> APIResponse:
        return (
            self.client
            .table(self.table_name)
            .delete()
            .eq("id", chat_id)
            .execute()
        )