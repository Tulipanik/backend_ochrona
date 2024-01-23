"use client";

import * as sessionCookie from "@/utils/cookie";
import { useEffect, useState } from "react";
import axios from "axios";
import PasswordMeterInput from "@/components/PasswordStrength";

export default function UserData() {
  const [see, setSee] = useState(false);
  cosnt[(password, setPassword)] = useState("");
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

    console.log(response);

    if (response.data.message) {
      alert(response.data.message);
    }
  };

  return (
    <div>
      <button onClick={() => seeFragileData()}>See fragile Data</button>
      <div>Id card: {fragileData.card_id}</div>
      <div>Card number: {fragileData.card_number}</div>
      <button onClick={() => setSee(!see)}>Change password</button>
      {see && (
        <form onSubmit={handleChange}>
          <input
            type="text"
            placeholder="old password"
            onChange={(e) => (formData.password = e.target.value)}
          />
          <input
            type="text"
            placeholder="new password"
            onChange={(e) => (formData.password_change_1 = password)}
          />
          <PasswordMeterInput password={password} />
          <input
            type="text"
            placeholder="confirm new password"
            onChange={(e) => (formData.password_change_2 = e.target.value)}
          />
          <input type="submit" value="Change password" />
        </form>
      )}
    </div>
  );
}
