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
      <form
        className="flex flex-col [&_*]:w-3/4 [&_*]:m-2 [&_*]:p-2 [&_*]:text-xl [&_*]:rounded-lg"
        onSubmit={makeTransaction}
      >
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
        <input
          className="bg-yellow-400 py-3 px-6 mt-5 ml-10 rounded-full text-lg drop-shadow-lg mb-5 hover:bg-yellow-700"
          type="submit"
          value="Make transaction"
        />
      </form>
    </div>
  );
}
