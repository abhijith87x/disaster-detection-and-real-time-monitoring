import { useState, useRef, useEffect } from "react";
import "../style/ChatWidget.css";

/**
 * ChatWidget — drop-in floating chat button + popup interface.
 *
 * Usage:
 *   <ChatWidget endpoint="/api/chat" />
 *
 * Props:
 *   endpoint   (string)  - URL your backend chat endpoint. Receives POST
 *                          { message: string } and should respond with
 *                          { reply: string } (adjust parseResponse if your
 *                          backend's shape differs).
 *   title      (string)  - Header text. Default "Chat".
 *   placeholder(string)  - Input placeholder. Default "Type a message...".
 */
export default function ChatWidget({
  endpoint = "http://localhost:8000/chat",
  title = "Chat",
  placeholder = "Type a message...",
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  useEffect(() => {
    if (isOpen && !isLoading) {
      inputRef.current?.focus();
    }
  }, [isOpen, isLoading]);

  async function sendMessage() {
    const text = input.trim();
    if (!text || isLoading) return;

    const userMsg = { id: Date.now(), role: "user", text };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });

      if (!res.ok) throw new Error(`Request failed (${res.status})`);

      const data = await res.json();
      // Adjust this line if your backend returns a different field name.
      const replyText = data.reply ?? data.response ?? data.message ?? "";

      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, role: "bot", text: replyText || "..." },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: "bot",
          text: "Something went wrong. Please try again.",
          isError: true,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="cw-root">
      {isOpen && (
        <div className="cw-panel">
          <div className="cw-header">
            <span className="cw-header-title">{title}</span>
            <button
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
              className="cw-close-btn"
            >
              ✕
            </button>
          </div>

          <div ref={scrollRef} className="cw-message-area">
            {messages.length === 0 && !isLoading && (
              <div className="cw-empty-state">Say hello to start the conversation.</div>
            )}

            {messages.map((m) => (
              <div
                key={m.id}
                className={`cw-bubble-row ${m.role === "user" ? "cw-user" : "cw-bot"}`}
              >
                <div
                  className={[
                    "cw-bubble",
                    m.role === "user" ? "cw-bubble-user" : "cw-bubble-bot",
                    m.isError ? "cw-bubble-error" : "",
                  ]
                    .filter(Boolean)
                    .join(" ")}
                >
                  {m.text}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className="cw-bubble-row cw-bot">
                <div className="cw-bubble cw-bubble-bot cw-typing-bubble">
                  <span className="cw-dot" />
                  <span className="cw-dot" />
                  <span className="cw-dot" />
                </div>
              </div>
            )}
          </div>

          <div className="cw-input-row">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={placeholder}
              disabled={isLoading}
              className="cw-input"
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !input.trim()}
              aria-label="Send message"
              className="cw-send-btn"
            >
              <SendIcon />
            </button>
          </div>
        </div>
      )}

      <button
        onClick={() => setIsOpen((v) => !v)}
        aria-label={isOpen ? "Close chat" : "Open chat"}
        className="cw-fab"
      >
        {isOpen ? <CloseIcon /> : <ChatIcon />}
      </button>
    </div>
  );
}

function ChatIcon() {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <path
        d="M4 4h16v12H8l-4 4V4z"
        stroke="white"
        strokeWidth="2"
        strokeLinejoin="round"
        strokeLinecap="round"
      />
    </svg>
  );
}

function CloseIcon() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
      <path d="M6 6l12 12M18 6L6 18" stroke="white" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
}

function SendIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
      <path d="M3 11l18-8-8 18-2-8-8-2z" fill="currentColor" />
    </svg>
  );
}