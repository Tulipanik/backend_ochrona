import "./../globals.css";
import Strip from "@/components/Strip";
import Navbar from "@/components/Navbar";

export default function Layout({ children }) {
  return (
    <div>
      <Navbar />
      {children}
    </div>
  );
}
