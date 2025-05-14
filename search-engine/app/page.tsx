"use client";
import Logo from "./components/Logo";
import { motion } from "motion/react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { FormEvent, useEffect, useState } from "react";
import { Loader } from "lucide-react";

type SearchResult = {
  id: string;
  title: string;
  description?: string;
  url: string;
  headings: string[];
};

export default function Home() {
  const router = useRouter();
  const params = useSearchParams();
  const pathname = usePathname();
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [page, setPage] = useState(0);
  const [rows, setRows] = useState(10);
  const [totalFound, setTotalFound] = useState(0);
  const [searchTime, setSearchTime] = useState<number | null>(null);

  const isFirstView = params.size === 0;

  function handleSearchFormSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const params = new URLSearchParams();
    params.set("q", (e.target as HTMLFormElement).search.value);
    router.push(`${pathname}?${params.toString()}`);
  }

  useEffect(() => {
    if (isFirstView) return;

    setIsLoading(true);
    async function fetchResults() {
      const url = process.env.NEXT_PUBLIC_URL;
      const query = params.get("q") ?? "";
      const searchParams = new URLSearchParams({
        defType: "edismax",
        q: query,
        qf: "title^4 url^3 headings^2 description^1 paragraph^0.5 keywords^0.5",
        mm: "2<75%",
        spellcheck: "true",
        "spellcheck.q": query,
        // q: `title:${query}\nurl:${query}\nheadings:${query}\ndescription:${query}\nparagraph:${query}`,
        sort: "page_rank desc",
        wt: "json",
        start: "" + page,
        rows: "" + rows,
      });

      const start = performance.now();
      const response = await fetch(
        `${url}/solr/main_core/select?${searchParams.toString()}`
      );
      const end = performance.now();

      const results = await response.json();
      const data = results.response;

      setTotalFound(data.numFound);
      setSearchTime((end - start) / 1000);

      setSearchResults(
        data.docs.map(
          (doc: any): SearchResult => ({
            id: doc.id,
            title: doc.title?.join("").trim(),
            description: doc.description?.join("").trim() || undefined,
            url: doc.url?.join("").trim(),
            headings: doc.headings,
          })
        )
      );

      setIsLoading(false);
    }

    fetchResults();
  }, [params, page, rows]);

  return (
    <div className="container mx-auto px-4">
      <motion.header
        layout="position"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{
          type: "spring",
          duration: 0.6,
          bounce: 0.3,
        }}
        className={`flex flex-wrap items-center gap-2 p-4 w-full transition-all ${
          isFirstView
            ? "flex-col justify-center h-screen"
            : "h-min justify-between items-center"
        }`}
      >
        <Logo />

        {isFirstView && (
          <motion.p
            key="desc-box"
            exit={{ opacity: 0, scale: 0 }}
            className="text-base text-gray-500"
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
          <div className="relative">
            <input
              type="search"
              id="search"
              name="search"
              className="block w-full p-3 ps-10 text-sm text-gray-900 border border-gray-300 rounded-full bg-gray-50 focus:ring-accent focus:border-accent shadow-sm"
              placeholder="Search..."
              required
              defaultValue={params.get("q") ?? ""}
            />
            <div className="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
              <svg
                className="w-4 h-4 text-gray-400"
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
          </div>
        </form>

        {!isFirstView && <span className="opacity-0">placeholder</span>}
      </motion.header>

      <main className="p-4 space-y-6 w-full">
        {isLoading ? (
          <div className="h-80 w-full flex justify-center items-center">
            <Loader className="animate-spin w-8 h-8 text-primary" />
          </div>
        ) : (
          <div className="max-w-prose mx-auto">
            {searchResults.length !== 0 && (
              <p className="text-sm text-gray-500">
                About {totalFound.toLocaleString()} results
                {searchTime !== null && ` (${searchTime.toFixed(2)} seconds)`}
              </p>
            )}

            <div className="space-y-6">
              {searchResults.length === 0 && (
                <div className="text-center">No results found.</div>
              )}

              {searchResults.map((result) => (
                <a
                  key={result.id}
                  href={result.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block group transition-all hover:translate-x-0.5"
                >
                  <h2 className="text-lg font-semibold text-primary group-hover:underline max-w-prose">
                    {result.title}
                  </h2>
                  {result.description && (
                    <p className="text-sm text-gray-700 mt-1 line-clamp-3 max-w-prose">
                      {result.description}
                    </p>
                  )}

                  {result.headings?.length > 0 && (
                    <ul className="mt-1 text-sm text-gray-500 list-disc list-inside space-y-1">
                      {result.headings.slice(0, 3).map((heading, idx) => (
                        <li key={idx} className="line-clamp-1">
                          {heading}
                        </li>
                      ))}
                    </ul>
                  )}
                </a>
              ))}
            </div>

            <div className="flex justify-between items-center pt-6">
              <button
                onClick={() => setPage((prev) => Math.max(prev - rows, 0))}
                disabled={page === 0}
                className="px-4 py-2 rounded-full bg-accent/10 text-accent hover:bg-accent/20 disabled:opacity-50 transition"
              >
                Previous
              </button>

              <span className="text-sm text-gray-600">
                Page {Math.floor(page / rows) + 1} of{" "}
                {Math.ceil(totalFound / rows)}
              </span>

              <button
                onClick={() => setPage((prev) => prev + rows)}
                disabled={page + rows >= totalFound}
                className="px-4 py-2 rounded-full bg-accent/10 text-accent hover:bg-accent/20 disabled:opacity-50 transition"
              >
                Next
              </button>
            </div>
          </div>
        )}
      </main>

      <footer className="py-4 text-center text-xs text-gray-400">
        © {new Date().getFullYear()} Snapi Search. All rights reserved.
      </footer>
    </div>
  );
}
