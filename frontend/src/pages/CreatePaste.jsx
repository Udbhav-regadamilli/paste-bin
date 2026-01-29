import { useState } from "react";
import { createPaste } from "../api";

export default function CreatePaste() {
  const [content, setContent] = useState("");
  const [ttl, setTtl] = useState("");
  const [views, setViews] = useState("");
  const [link, setLink] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    const payload = {
      content,
      ttl_seconds: ttl ? Number(ttl) : undefined,
      max_views: views ? Number(views) : undefined,
    };

    const res = await createPaste(payload);
    setLink(res.url);
  }

  return (
    <div className="container">
      <h2>Create Paste</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
        />

        <input
          type="number"
          placeholder="TTL seconds (optional)"
          value={ttl}
          onChange={(e) => setTtl(e.target.value)}
        />

        <input
          type="number"
          placeholder="Max views (optional)"
          value={views}
          onChange={(e) => setViews(e.target.value)}
        />

        <button type="submit">Create</button>
      </form>

      {link && (
        <p>
          Share link: <a href={link}>{link}</a>
        </p>
      )}
    </div>
  );
}
