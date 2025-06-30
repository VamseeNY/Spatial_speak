import React from "react";
import Link from "next/link";
import styles from "@/styles/Navbar.module.css";

const Navbar = () => {
  return (
    <nav className={styles.navbar}>
      <Link href="/" className={styles.navLink}>Home</Link>
      <Link href="/dashboard" className={styles.navLink}>Dashboard</Link>
      <Link href="/chat" className={styles.navLink}>Chatbot</Link>
      <Link href="/library" className={styles.navLink}>Research Library</Link> {/* ✅ Added Library Link */}

    </nav>
  );
};

export default Navbar;
