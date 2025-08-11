from langchain_core.chat_history import InMemoryChatMessageHistory

_global_chat_memory = InMemoryChatMessageHistory()

def get_chat_history(session_id: str):
    return _global_chat_memory
