"use client";

import { useRouter } from "next/navigation";
import "./globals.css";

export default function Home() {
  const router = useRouter();
  return (
    <div className="flex flex-col justify-center items-center h-screen w-screen">
      <h1 className="text-center text-8xl mb-20">Witaj w BeeBanku!</h1>
      <button
        className="text-6xl text-yellow-900 bg-yellow-400 p-10 rounded-full drop-shadow-xl hover:bg-yellow-500"
        onClick={() => router.push("/login")}
      >
        Zaloguj się
      </button>
    </div>
  );
}
