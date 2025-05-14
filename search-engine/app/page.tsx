"use client";
import Image from "next/image";
import Logo from "./components/Logo";
import { AnimatePresence, motion } from "motion/react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";
import { Loader } from "lucide-react";

export default function Home() {
  let router = useRouter();
  let params = useSearchParams();
  let pathname = usePathname();
  let [searchResults, setSearchResults] = useState([]);
  let [isLoading, setIsLoading] = useState(false);

  let isFirstView = params.size === 0;

  function handleSearchFormSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const params = new URLSearchParams();
    params.set("q", (e.target as HTMLFormElement).search.value);
    router.push(`${pathname}?${params.toString()}`);
  }

  useEffect(
    function getSearchResults() {
      if (isFirstView) return;

      setIsLoading(true);
      async function fetchResults() {
        const url = process.env.NEXT_PUBLIC_URL;
        const query = params.get("q");
        console.log(url, query);
        const searchQuery = `url:${query}\\n`;

        const searchParams = new URLSearchParams({
          "q.op": "OR",
          q: `title:${query}\nurl:${query}\nheadings:${query}\ndescription:${query}\nparagraph:${query}`,
          sort: "page_rank desc",
          wt: "json",
        });

        console.log(searchParams.toString());

        let response = await fetch(
          `${url}/solr/main_core/select?${searchParams.toString()}`
        );
        let results = await response.json();
        console.log(results);

        setIsLoading(false);
      }

      fetchResults();
    },
    [params]
  );

  return (
    <div className="container mx-auto">
      <motion.header
        layout
        className={`flex flex-wrap items-center gap-2 p-4 w-full ${
          isFirstView
            ? "flex-col justify-center h-screen"
            : "h-min justify-between items-center"
        }`}
        transition={{
          type: "spring",
          visualDuration: 0.2,
          bounce: 0.2,
        }}
      >
        <Logo />

        {isFirstView && (
          <motion.p
            key="desc-box"
            exit={{ opacity: 0, scale: 0 }}
            className="text-base"
          >
            The next gen Search Engine.
          </motion.p>
        )}

        <form
          className={`w-full sm:w-4/5 md:w-3/5 lg:w-2/5 ${
            isFirstView && "mt-4"
          }`}
          onSubmit={handleSearchFormSubmit}
        >
          <label
            htmlFor="search"
            className="mb-2 text-sm font-medium text-gray-900 sr-only"
          >
            Search
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
              <svg
                className="w-4 h-4 text-gray-500"
                aria-hidden="true"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 20 20"
              >
                <path
                  stroke="currentColor"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
                />
              </svg>
            </div>
            <input
              type="search"
              id="search"
              name="search"
              className="block w-full p-3 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-primary focus:border-primary"
              placeholder="Search..."
              required
              defaultValue={params.get("q") ?? ""}
            />
          </div>
        </form>

        {!isFirstView && <span className="opacity-0">ASDFA</span>}
      </motion.header>
      <main className="p-4">
        {isLoading && (
          <div className="h-80 w-full flex justify-center items-center">
            <Loader className="animate-spin w-8 h-8 text-primary" />
          </div>
        )}
      </main>
      <footer className=""></footer>
    </div>
  );
}
