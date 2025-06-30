import React, { useState } from "react";
import styles from "@/styles/Chatbot.module.css";

const Chatbot: React.FC = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <>
      {/* Floating Chatbot Button */}
      <button className={styles.chatbotButton} onClick={() => setIsChatOpen(!isChatOpen)}>
        💬
      </button>

      {/* Chat Modal */}
      {isChatOpen && (
        <div className={styles.chatModal}>
          <div className={styles.chatHeader}>
            <span>AI Chatbot</span>
            <button className={styles.closeButton} onClick={() => setIsChatOpen(false)}>×</button>
          </div>
          <div className={styles.chatBody}>
            <p>Ask me anything about space biology and agriculture!</p>
          </div>
        </div>
      )}
    </>
  );
};

export default Chatbot;
