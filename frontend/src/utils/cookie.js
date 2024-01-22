"use server";

import { cookies } from "next/headers";

export const setCookie = (value) => {
  cookies().set("session", value, {
    // secure: true,
    maxAge: 60 * 5,
    sameSite: "strict",
    httpOnly: true,
  });
};

export const checkCookie = () => {
  if (cookies().has("session")) {
    return true;
  } else {
    false;
  }
};

export const getCookie = () => {
  return cookies().get("session");
};

export const deleteCookie = () => {
  cookies().delete("session");
};
