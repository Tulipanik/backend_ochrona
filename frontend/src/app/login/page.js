"use client";

import { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import WriteLogin from "@/components/WriteLogin";
import WritePassword from "@/components/WritePassword";
import { setCookie } from "@/utils/cookie";

export default function Login() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [passElements, setElements] = useState([]);

  const submitUsername = async (e) => {
    e.preventDefault();

    const response = await axios.post("http://127.0.0.1:8000/login-1", {
      login: username,
    });

    if (response.data.elements) {
      setElements(response.data.elements);
    } else if (response.data.message) {
      alert(response.data.message);
    } else {
      alert("networkError");
    }
  };

  const submitPassword = async (e, password) => {
    e.preventDefault();
    const response = await axios.post("http://127.0.0.1:8000/login-2", {
      login: username,
      password: password,
    });

    if (response.data.session_id) {
      await setCookie(response.data.session_id);
      router.push("/auth/start");
    } else if (response.data.message) {
      alert(response.data.message);
    } else {
      alert("networkError");
    }
  };

  return (
    <>
      {passElements.length === 0 ? (
        <div className="flex flex-col justify-center items-center h-screen w-screen ">
          <WriteLogin
            submitUsername={submitUsername}
            setUsername={setUsername}
          />
        </div>
      ) : (
        <WritePassword
          elements={passElements}
          submitPassword={submitPassword}
        />
      )}
    </>
  );
}
