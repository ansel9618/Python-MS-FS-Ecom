"use client";
import { useState } from "react";
import Link from "next/link"

export default function HomePage() {
  const [name, setName] = useState("");
  const [count, setCount] = useState(0);

  return (
    <main className="p-6">
      <h1 className="text-3xl font-bold">Hello, {name || "Stranger"}</h1>

      <input 
      type="text"
      placeholder="Enter your name"
      value={name}    
      onChange={(e) => setName(e.target.value)}
      className="border p-2 rounded"
       />
       <button
        className="mt-4 bg-blue-600 text-white px-4 py-2 rounded"
        onClick={() => setCount(count + 1)}
      >
        You clicked {count} times
      </button>
      <Link
        href={`/goodbye?name=${encodeURIComponent(name)}`}
        className="mt-4 inline-block text-blue-600 underline"
      >
        Say Goodbye
      </Link>
    </main>
  );
}