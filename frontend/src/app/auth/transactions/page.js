"use client";

import axios from "axios";
import { useEffect, useState } from "react";
import * as sessionCookie from "@/utils/cookie";
import Table from "@/components/Table";
import { useRouter } from "next/navigation";

export default function Transactions() {
  const router = useRouter();
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    async function getData() {
      const session_id = await sessionCookie.getCookie();
      const response = await axios.post(
        "http://127.0.0.1:8000/get-transactions",
        {
          session_id: session_id.value,
        }
      );

      if (response.data.list) {
        setTransactions(response.data.list);
      }
    }
    getData();
  }, []);
  return (
    <div>
      <button
        className="bg-yellow-400 py-3 px-6 mt-5 ml-10 rounded-full text-lg drop-shadow-lg mb-10 hover:bg-yellow-700"
        onClick={() => {
          router.push("/auth/create-transaction");
        }}
      >
        Create new transaction
      </button>
      <Table tableData={transactions} />
    </div>
  );
}
