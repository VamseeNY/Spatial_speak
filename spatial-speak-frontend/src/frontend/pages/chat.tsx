import React, { useState, useEffect } from "react";
import styles from "@/styles/Chat.module.css";

interface ChatMessage {
  id: number;
  text: string;
  sender: "user" | "bot";
}

interface ChatSession {
  id: number;
  title: string;
  messages: ChatMessage[];
}

export default function Chat() {
  const [chatSessions, setChatSessions] = useState<ChatSession[]>([]);
  const [currentChat, setCurrentChat] = useState<ChatSession | null>(null);
  const [input, setInput] = useState("");

  // Load chat sessions from local storage on page load
  useEffect(() => {
    const savedChats = localStorage.getItem("chatSessions");
    if (savedChats) {
      setChatSessions(JSON.parse(savedChats));
    }
  }, []);

  // Save chat sessions to local storage whenever they update
  useEffect(() => {
    localStorage.setItem("chatSessions", JSON.stringify(chatSessions));
  }, [chatSessions]);

  const startNewChat = () => {
    const newChat: ChatSession = {
      id: chatSessions.length + 1,
      title: `Chat ${chatSessions.length + 1}`,
      messages: [],
    };
    setChatSessions((prev) => [...prev, newChat]);
    setCurrentChat(newChat);
  };

  const sendMessage = () => {
    if (!input.trim() || !currentChat) return;

    const userMessage: ChatMessage = {
      id: currentChat.messages.length + 1,
      text: input,
      sender: "user",
    };

    const updatedChat = {
      ...currentChat,
      messages: [...currentChat.messages, userMessage],
    };

    setCurrentChat(updatedChat);
    setChatSessions((prev) =>
      prev.map((chat) => (chat.id === currentChat.id ? updatedChat : chat))
    );

    setTimeout(() => {
      const botResponse: ChatMessage = {
        id: updatedChat.messages.length + 1,
        text: `You asked: "${input}" (AI response goes here)`,
        sender: "bot",
      };

      const updatedWithBot = {
        ...updatedChat,
        messages: [...updatedChat.messages, botResponse],
      };

      setCurrentChat(updatedWithBot);
      setChatSessions((prev) =>
        prev.map((chat) => (chat.id === currentChat.id ? updatedWithBot : chat))
      );
    }, 1000);

    setInput("");
  };

  return (
    <div className={styles.chatContainer}>
      {/* Sidebar with Previous Chat Sessions */}
      <div className={styles.sidebar}>
        <h2>Previous Chats</h2>
        <button className={styles.newChatButton} onClick={startNewChat}>
          + New Chat
        </button>
        <ul>
          {chatSessions.length > 0 ? (
            chatSessions.map((chat) => (
              <li
                key={chat.id}
                onClick={() => setCurrentChat(chat)}
                className={currentChat?.id === chat.id ? styles.activeChat : ""}
              >
                {chat.title}
              </li>
            ))
          ) : (
            <p>No previous chats</p>
          )}
        </ul>
      </div>

      {/* Main Chat Window */}
      <div className={styles.chatWindow}>
        <div className={styles.chatHeader}>
          {currentChat ? currentChat.title : "Start a New Chat"}
        </div>
        <div className={styles.chatMessages}>
          {currentChat?.messages.map((msg) => (
            <div key={msg.id} className={msg.sender === "user" ? styles.userMessage : styles.botMessage}>
              {msg.text}
            </div>
          ))}
        </div>

        {/* Search Bar (Input Area) */}
        {currentChat && (
          <div className={styles.inputContainer}>
            <input
              type="text"
              placeholder="Ask something..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            />
            <button onClick={sendMessage}>Send</button>
          </div>
        )}
      </div>
    </div>
  );
}
