import React, { useState, useEffect } from "react";
import styles from "@/styles/Library.module.css";

interface ResearchPaper {
  id: number;
  title: string;
  author: string;
  year: number;
  summary: string;
  link: string;
}

export default function Library() {
  const [search, setSearch] = useState("");
  const [filteredPapers, setFilteredPapers] = useState<ResearchPaper[]>([]);
  const [selectedPaper, setSelectedPaper] = useState<ResearchPaper | null>(null);

  const researchPapers: ResearchPaper[] = [
    {
      id: 1,
      title: "The Effects of Microgravity on Plant Growth",
      author: "Dr. John Doe",
      year: 2023,
      summary: "This study explores how microgravity impacts plant development...",
      link: "https://nasa.gov/research-paper-1",
    },
    {
      id: 2,
      title: "Space Farming: The Future of Agriculture",
      author: "Dr. Jane Smith",
      year: 2022,
      summary: "An analysis of crop growth in space habitats...",
      link: "https://nasa.gov/research-paper-2",
    },
    {
      id: 3,
      title: "AI-Powered Insights for Space Biology",
      author: "Dr. Alex Johnson",
      year: 2024,
      summary: "How AI is transforming space biology research...",
      link: "https://nasa.gov/research-paper-3",
    },
  ];

  useEffect(() => {
    setFilteredPapers(researchPapers);
  }, []);

  useEffect(() => {
    const results = researchPapers.filter(
      (paper) =>
        paper.title.toLowerCase().includes(search.toLowerCase()) ||
        paper.author.toLowerCase().includes(search.toLowerCase()) ||
        paper.year.toString().includes(search)
    );
    setFilteredPapers(results);
  }, [search]);

  return (
    <div className={styles.container}>
      <h1 className={styles.heading}>Research Library</h1>

      {/* Search Bar */}
      <input
        type="text"
        className={styles.searchBar}
        placeholder="Search by title, author, or year..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {/* Paper List */}
      <div className={styles.paperList}>
        {filteredPapers.map((paper) => (
          <div
            key={paper.id}
            className={styles.paperCard}
            onClick={() => setSelectedPaper(paper)}
          >
            <h2>{paper.title}</h2>
            <p><strong>Author:</strong> {paper.author}</p>
            <p><strong>Year:</strong> {paper.year}</p>
          </div>
        ))}
      </div>

      {/* Paper Details Modal */}
      {selectedPaper && (
        <div className={styles.modalOverlay} onClick={() => setSelectedPaper(null)}>
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <h2>{selectedPaper.title}</h2>
            <p><strong>Author:</strong> {selectedPaper.author}</p>
            <p><strong>Year:</strong> {selectedPaper.year}</p>
            <p>{selectedPaper.summary}</p>
            <a href={selectedPaper.link} target="_blank" rel="noopener noreferrer">
              Read Full Paper
            </a>
            <button className={styles.closeButton} onClick={() => setSelectedPaper(null)}>Close</button>
          </div>
        </div>
      )}
    </div>
  );
}
