import { Inter } from "next/font/google";
import "./globals.css";
import Strip from "@/components/Strip";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "BeeBank",
  description: "Welcome to BeeBank",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Strip />
        {children}
      </body>
    </html>
  );
}
