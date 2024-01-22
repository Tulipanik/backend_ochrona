"use client";

import { useState } from "react";
import axios from "axios";
import * as sessionCookie from "@/utils/cookie";

export default function CreateTransacion() {
  const [formData, setFormData] = useState({
    account: "",
    title: "",
    address: "",
    amount: 0,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const makeTransaction = async (e) => {
    e.preventDefault();

    const session_id = await sessionCookie.getCookie();

    const response = await axios.post(
      "http://127.0.0.1:8000/make-transaction",
      {
        ...formData,
        session_id: session_id.value,
      }
    );

    console.log(response);
  };
  return (
    <div>
      <form onSubmit={makeTransaction} className="flex flex-col ">
        <label for="account">Account number:</label>
        <input
          type="text"
          name="account"
          id="account"
          value={formData.account}
          onChange={handleChange}
        />
        <label for="title">Title:</label>
        <input
          type="text"
          name="title"
          id="title"
          value={formData.title}
          onChange={handleChange}
        />
        <label for="address">Address:</label>
        <textarea
          type="text"
          name="address"
          id="address"
          value={formData.address}
          onChange={handleChange}
        />
        <label for="amount">Amount:</label>
        <input
          type="numeric"
          name="amount"
          id="amount"
          value={formData.amount}
          onChange={handleChange}
        />
        <input type="submit" value="Make transaction" />
      </form>
    </div>
  );
}
