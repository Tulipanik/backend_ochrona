"use client";

const URL = "http://127.0.0.1:8000/";

export default function WriteLogin({ setUsername, submitUsername }) {
  return (
    <div>
      <form onSubmit={submitUsername} className="flex flex-col">
        <label className="text-4xl mb-10">Wpisz numer klienta:</label>
        <input
          className="p-5 text-2xl"
          type="text"
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          className="text-2xl mt-10 bg-yellow-400 py-4 drop-shadow-xl hover:bg-yellow-600 rounded-full"
          type="submit"
          value="Przejdź dalej"
        />
      </form>
    </div>
  );
}
