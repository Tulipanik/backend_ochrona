"use client";

import axios from "axios";
import { useEffect, useState } from "react";
import * as sessionCookie from "@/utils/cookie";

export default function StartPage() {
  const [userData, setUserData] = useState({});

  useEffect(() => {
    async function getData() {
      const session_id = await sessionCookie.getCookie();

      const response = await axios.post("http://127.0.0.1:8000/get-user-data", {
        session_id: session_id.value,
      });
      console.log(response);
      if (response.data.account) {
        setUserData({
          ...response.data,
          money: response.data.money.toFixed(2),
        });
      }
    }
    getData();
  }, []);
  return (
    <div className="flex flex-col justify-center items-center h-max">
      <h1 className="text-6xl mt-10">Witaj w BeeBank!</h1>
      <h3 className="text-4xl mt-10">
        Twój stan konta: <span>{userData.money}</span>
      </h3>
      <p className="flex flex-col text-4xl mt-10">
        Twój numer konta: <span className="block">{userData.account}</span>
      </p>
    </div>
  );
}
