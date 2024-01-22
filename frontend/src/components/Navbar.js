import Link from "next/link";

export default function Navbar() {
  return (
    <ul className="flex w-screen bg-yellow-400 [&_li]:py-5 [&_li]:px-5 [&_li]:text-lg">
      <li className="hover:bg-yellow-700">
        <Link href="/auth/start">Home</Link>
      </li>
      <li className="hover:bg-yellow-700">
        <Link href="/auth/transactions">Transactions</Link>
      </li>
      <li className="hover:bg-yellow-700">
        <Link href="/auth/user-data">User data</Link>
      </li>
    </ul>
  );
}
