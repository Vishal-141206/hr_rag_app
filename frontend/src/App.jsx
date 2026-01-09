import { useState } from "react";

const API_BASE = "";

export default function App() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  const uploadFile = async () => {
    if (!file) {
      setUploadStatus("❌ No file selected");
      return;
    }

    setUploading(true);
    setUploadStatus("Uploading document…");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error();

      setUploadStatus(`✅ Uploaded: ${file.name}`);
    } catch {
      setUploadStatus("❌ Upload failed");
    }

    setUploading(false);
  };

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");
    setSources([]);

    const res = await fetch(`${API_BASE}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();
    setAnswer(data.answer);
    setSources(data.sources || []);
    setLoading(false);
  };

  return (
    <div style={styles.app}>
      {/* Sidebar */}
      <aside style={styles.sidebar}>
        <h2 style={styles.logo}>HR Assist</h2>
        <p style={styles.sideText}>Internal HR System</p>
      </aside>

      {/* Main */}
      <main style={styles.main}>
        <h1 style={styles.pageTitle}>AI-Powered HR Onboarding Assistant</h1>
        <p style={styles.pageSubtitle}>
          Ask accurate, document-verified questions about company policies.
        </p>

        {/* Upload */}
        <div style={styles.card}>
          <h3>Upload HR Policy Document</h3>
          <p style={styles.desc}>
            Supported formats: PDF, DOCX, TXT
          </p>

          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
          />

          {file && (
            <p style={styles.fileInfo}>
              Selected file: <strong>{file.name}</strong>
            </p>
          )}

          <button
            style={styles.primaryBtn}
            onClick={uploadFile}
            disabled={uploading}
          >
            {uploading ? "Uploading…" : "Upload Document"}
          </button>

          {uploadStatus && (
            <p style={styles.status}>{uploadStatus}</p>
          )}
        </div>

        {/* Ask */}
        <div style={styles.card}>
          <h3>Ask a Question</h3>

          <input
            style={styles.textInput}
            placeholder="e.g. How many vacation days do I get?"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />

          <button
            style={styles.primaryBtn}
            onClick={askQuestion}
          >
            Ask Assistant
          </button>
        </div>

        {/* Answer */}
        {loading && <p style={styles.loading}>Searching documents…</p>}

        {answer && (
          <div style={styles.answerCard}>
            <h3>Answer</h3>
            <p style={styles.answerText}>{answer}</p>

            {sources.length > 0 && (
              <>
                <h4>Sources</h4>
                <ul>
                  {sources.map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>
              </>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

/* ---------------- STYLES ---------------- */

const styles = {
  app: {
    display: "flex",
    minHeight: "100vh",
    background: "#f8fafc",
    fontFamily: "Inter, Segoe UI, sans-serif",
    color: "#0f172a",
  },
  sidebar: {
    width: 220,
    background: "#0f172a",
    color: "#ffffff",
    padding: 24,
  },
  logo: {
    marginBottom: 6,
  },
  sideText: {
    fontSize: 13,
    color: "#cbd5f5",
  },
  main: {
    flex: 1,
    padding: 40,
  },
  pageTitle: {
    marginBottom: 6,
  },
  pageSubtitle: {
    color: "#475569",
    marginBottom: 30,
  },
  card: {
    background: "#ffffff",
    padding: 24,
    borderRadius: 10,
    boxShadow: "0 4px 12px rgba(0,0,0,0.06)",
    marginBottom: 28,
  },
  desc: {
    fontSize: 14,
    color: "#475569",
    marginBottom: 10,
  },
  fileInfo: {
    marginTop: 8,
    fontSize: 14,
  },
  status: {
    marginTop: 10,
    fontSize: 14,
  },
  textInput: {
    width: "100%",
    padding: 10,
    borderRadius: 6,
    border: "1px solid #cbd5e1",
    marginBottom: 12,
    fontSize: 14,
  },
  primaryBtn: {
    background: "#2563eb",
    color: "#ffffff",
    border: "none",
    padding: "10px 18px",
    borderRadius: 6,
    cursor: "pointer",
    fontSize: 14,
  },
  loading: {
    color: "#475569",
    fontStyle: "italic",
  },
  answerCard: {
    background: "#eef2ff",
    padding: 24,
    borderRadius: 10,
    boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
  },
  answerText: {
    marginTop: 10,
    lineHeight: 1.6,
    color: "#0f172a",
  },
};
