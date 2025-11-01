import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import ChangePasswordModal from "./ChangePasswordModal"; // 1. Import the new modal

const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false); // 2. Add state for the modal
  const navigate = useNavigate();

  const userRef = useRef(JSON.parse(localStorage.getItem("user")));
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  useEffect(scrollToBottom, [messages]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    const user = userRef.current;

    if (!token || !user) {
      navigate("/login");
    } else {
      setMessages([
        {
          from: "copilot",
          text: `Welcome, ${user.role} ${
            user.name || ""
          }! How can I help you today?`,
        },
      ]);
    }
  }, [navigate]);

  const handleSend = async () => {
    // (Your existing handleSend logic... no changes needed here)
    if (!input.trim() || isLoading) return;
    const userMessage = { from: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    try {
      const token = localStorage.getItem("token");
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/api/chat`,
        { message: input },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      const copilotMessage = { from: "copilot", text: response.data.reply };
      setMessages((prev) => [...prev, copilotMessage]);
    } catch (error) {
      let errorMessageText = "Sorry, I encountered an error.";
      if (error.response?.status === 401) {
        errorMessageText =
          "Your session has expired. Please log out and log in again.";
      }
      setMessages((prev) => [
        ...prev,
        { from: "copilot", text: errorMessageText },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  if (!userRef.current) return null;

  return (
    <>
      {" "}
      {/* 3. Use a React Fragment to wrap everything */}
      <div className="chat-container">
        <header className="chat-header">
          <h1>Campus Copilot</h1>
          <p>Logged in as: {userRef.current.email}</p>
          {/* 4. Add the new button to open the modal */}
          <button
            onClick={() => setIsModalOpen(true)}
            className="logout-button"
            style={{ marginLeft: "10px" }}
          >
            Change Password
          </button>
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        </header>
        <div className="message-list">
          {/* ... (your message mapping) ... */}
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.from}`}>
              {msg.text}
            </div>
          ))}
          {isLoading && (
            <div className="message copilot">Copilot is typing...</div>
          )}
          <div ref={messagesEndRef} />
        </div>
        <div className="input-area">
          {/* ... (your input form) ... */}
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask a question..."
            disabled={isLoading}
          />
          <button onClick={handleSend} disabled={isLoading}>
            {isLoading ? "..." : "Send"}
          </button>
        </div>
      </div>
      {/* 5. Conditionally render the modal */}
      {isModalOpen && (
        <ChangePasswordModal onClose={() => setIsModalOpen(false)} />
      )}
    </>
  );
};

export default ChatPage;
