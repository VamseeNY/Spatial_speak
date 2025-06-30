import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import styles from "@/styles/Home.module.css";
import Chatbot from "@/components/Chatbot";

// Define types for SpeechRecognition and SpeechRecognitionEvent
interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  lang: string;
  start: () => void;
  stop: () => void;
  onstart: () => void;
  onend: () => void;
  onresult: (event: SpeechRecognitionEvent) => void;
}

interface SpeechRecognitionEvent extends Event {
  results: Array<{ transcript: string }[]>;
}

export default function Home() {
  const [isListening, setIsListening] = useState(false);
  const [message, setMessage] = useState("Try saying 'Show me space data'");

  useEffect(() => {
    const SpeechRecognitionClass =
      (window as unknown as { SpeechRecognition: new () => SpeechRecognition }).SpeechRecognition ||
      (window as unknown as { webkitSpeechRecognition: new () => SpeechRecognition }).webkitSpeechRecognition;

    if (!SpeechRecognitionClass) {
      console.error("Speech Recognition not supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognitionClass();
    recognition.continuous = true;
    recognition.lang = "en-US";

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onresult = (event: SpeechRecognitionEvent) => {
      const transcript = event.results[event.results.length - 1][0].transcript;
      setMessage(`You said: "${transcript}"`);
    };

    if (isListening) {
      recognition.start();
    } else {
      recognition.stop();
    }

    return () => recognition.stop();
  }, [isListening]);

  return (
    <div className={styles.container} style={{ backgroundColor: "#0a192f", minHeight: "100vh", width: "100vw" }}>
      {/* Navigation Bar */}
      <nav className={styles.navbar}>
        <Link href="/" className={styles.navLink}>Home</Link>
        <Link href="/dashboard" className={styles.navLink}>Dashboard</Link>
        
        <Link href="/chat" className={styles.navLink}>Chatbot</Link>
        <Link href="/library" className={styles.navLink}>Research Library</Link> {/* ✅ Added Library Link */}

      </nav>

      {/* Animated Heading */}
      <motion.h1
        className={styles.heading}
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
      >
        Spatial Speak
      </motion.h1>

      <motion.p
        className={styles.subheading}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1.5 }}
      >
        Navigate Space Biology & Agriculture with AI
      </motion.p>

      {/* Animated Buttons */}
      <motion.div 
        className={styles.buttonContainer}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1.5 }}
      >
        <button className={styles.primaryButton}>Explore Data</button>
        <button className={styles.secondaryButton} onClick={() => setIsListening(!isListening)}>
          {isListening ? "Stop Listening" : "Use Voice Search"}
        </button>
      </motion.div>

      {/* Display Voice Input Message */}
      <motion.div 
        className={styles.messageContainer}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 2 }}
      >
        <p className={styles.voiceMessage}>{message}</p>
      </motion.div>
      {/* Info Boxes */}
      <div className={styles.cardContainer}>
        <div className={styles.card}>
          <h2>Space Agriculture</h2>
          <p>Discover how plants grow in microgravity.</p>
        </div>
        <div className={styles.card}>
          <h2>Space Biology</h2>
          <p>Understand genetic changes in space.</p>
        </div>
        <div className={styles.card}>
          <h2>AI-Powered Insights</h2>
          <p>Use AI to analyze space research data.</p>
        </div>
      </div>


      {/* Floating Chatbot */}
      <Chatbot />
    </div>
  );
}
