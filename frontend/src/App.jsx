import { useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  const sendMessage = async () => {
    const res = await fetch("http://localhost:8000/webhook/360dialog", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: "971501234567",
        text: message
      }),
    });
  
    const data = await res.json();
  
    setResponse(data.next_question);
    setMessage(""); // clear input
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>Real Estate Chat</h1>

      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type your answer..."
      />

      <button onClick={sendMessage}>Send</button>

      <p>Response: {response}</p>
    </div>
  );
}

export default App;