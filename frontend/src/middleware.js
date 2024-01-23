import { NextResponse } from "next/server";
import { checkCookie, getCookie } from "@/utils/cookie";

export async function middleware(request) {
  if (checkCookie()) {
    const cookie = getCookie();
    let response = await fetch("http://127.0.0.1:8000/verify-session", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        session_id: cookie.value,
      }),
    });

    response = await response.json();

    if (!response.valid) {
      return NextResponse.redirect(new URL("/", request.url));
    }
  } else {
    return NextResponse.redirect(new URL("/", request.url));
  }
}

export const config = {
  matcher: ["/auth/:path*"],
};
