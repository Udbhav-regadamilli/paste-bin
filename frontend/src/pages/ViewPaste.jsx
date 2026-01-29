import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchPaste } from "../api";

export default function ViewPaste() {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchPaste(id)
      .then(setData)
      .catch(() => setError("Paste unavailable"));
  }, [id]);

  if (error) return <h2>{error}</h2>;
  if (!data) return <h2>Loading...</h2>;

  return (
    <div className="container">
      <h2>Paste</h2>
      <pre>{data.content}</pre>
      {data.remaining_views !== null && (
        <p>Remaining views: {data.remaining_views}</p>
      )}
    </div>
  );
}
