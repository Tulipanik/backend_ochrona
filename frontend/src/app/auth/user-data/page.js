"use client";

import * as sessionCookie from "@/utils/cookie";
import { useEffect, useState } from "react";
import axios from "axios";
import PasswordMeterInput from "@/components/PasswordStrength";

export default function UserData() {
  const [see, setSee] = useState(false);
  const [password, setPassword] = useState("");
  let formData = {
    password: "",
    password_change_1: password,
    password_change_2: "",
  };

  useEffect(() => {
    formData = { ...formData, password_change_1: password };
  }, [password]);

  const initialFragileData = {
    card_id: "",
    card_number: "",
  };

  const [fragileData, setFragileData] = useState(initialFragileData);

  const seeFragileData = async () => {
    const session_id = await sessionCookie.getCookie();

    const response = await axios.post(
      "http://127.0.0.1:8000/get-fragile-data",
      {
        session_id: session_id.value,
      }
    );

    if (response.data.message) {
      alert(response.data.message);
    } else if (response.data.card_id) {
      setFragileData(response.data);
      setTimeout(() => {
        setFragileData(initialFragileData);
      }, 30000);
    } else {
      alert("Network error");
    }
  };

  const handleChange = async (e) => {
    e.preventDefault();
    console.log(formData);
    const session_id = await sessionCookie.getCookie();

    const response = axios.post("http://127.0.0.1:8000/change-password", {
      ...formData,
      session_id: session_id.value,
    });

    if (response.data.message) {
      alert(response.data.message);
    }
  };

  return (
    <div className="flex flex-col w-screen">
      <button
        className="bg-yellow-400 py-3 px-6 mt-5 ml-10 rounded-full text-lg drop-shadow-lg mb-5 hover:bg-yellow-700 w-1/6"
        onClick={() => seeFragileData()}
      >
        See fragile Data
      </button>
      <div className="text-2xl">Id card: {fragileData.card_id}</div>
      <div className="text-2xl">Card number: {fragileData.card_number}</div>
      <button
        className="bg-yellow-400 py-3 px-6 mt-5 ml-10 rounded-full text-lg drop-shadow-lg mb-5 hover:bg-yellow-700  w-1/6"
        onClick={() => setSee(!see)}
      >
        Change password
      </button>
      {see && (
        <form
          className="flex flex-col [&_*]:w-3/4 [&_*]:m-2 [&_*]:p-2 [&_*]:text-xl [&_*]:rounded-lg"
          onSubmit={handleChange}
        >
          <input
            type="password"
            className="text-lg"
            placeholder="old password"
            onChange={(e) => (formData.password = e.target.value)}
          />
          <input
            type="password"
            placeholder="new password"
            onChange={(e) =>
              (formData.password_change_1 = setPassword(e.target.value))
            }
          />
          <PasswordMeterInput password={password} setPassword={setPassword} />
          <input
            type="password"
            placeholder="confirm new password"
            onChange={(e) => (formData.password_change_2 = e.target.value)}
          />
          <input
            className="bg-yellow-400 py-3 px-6 mt-5 ml-10 rounded-full text-lg drop-shadow-lg mb-5 hover:bg-yellow-700"
            type="submit"
            value="Change password"
          />
        </form>
      )}
    </div>
  );
}
