import Image from "next/image";
import Logo from "./components/Logo";

export default function Home() {
  return (
    <div className="">
      <header className="flex flex-col">
        <Logo />
        <p className="">The next gen Search Engine.</p>
      </header>
      <main className=""></main>
      <footer className=""></footer>
    </div>
  );
}
