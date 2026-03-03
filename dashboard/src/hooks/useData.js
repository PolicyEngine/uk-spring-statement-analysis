import { useState, useEffect } from "react";

export default function useData(url) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(url)
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to fetch ${url}`);
        return res.json();
      })
      .then(setData)
      .catch(setError);
  }, [url]);

  return { data, error };
}
