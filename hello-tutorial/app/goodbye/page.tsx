"use client";
import { useSearchParams } from "next/navigation";

export default function GoodbyePage() {
    const params = useSearchParams();
    const name = params.get("name") || "friend";


    return (
      <main className="p-6">
        <h1 className="text-3xl font-bold">
            Goodbye, {name} 👋
        </h1>
      </main>
    );
  }