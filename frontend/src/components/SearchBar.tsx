import { useState, useRef, useEffect, FormEvent } from 'react';
import axios from 'axios';
import { MovieCard } from './MovieCard';
import { Carousel } from './Carousel';

const LANGUAGES = [
  { code: '', label: 'All Languages', flag: '🌐' },
  { code: 'en', label: 'English', flag: '🇬🇧' },
  { code: 'hi', label: 'Hindi', flag: '🇮🇳' },
  { code: 'te', label: 'Telugu', flag: '🇮🇳' },

  { code: 'ko', label: 'Korean', flag: '🇰🇷' },



  { code: 'de', label: 'German', flag: '🇩🇪' },
  { code: 'it', label: 'Italian', flag: '🇮🇹' },

  { code: 'pt', label: 'Portuguese', flag: '🇵🇹' },
  { code: 'ru', label: 'Russian', flag: '🇷🇺' },

  { code: 'th', label: 'Thai', flag: '🇹🇭' },
  { code: 'tr', label: 'Turkish', flag: '🇹🇷' },
];

const EXAMPLE_QUERIES = [
  "A mind-bending sci-fi thriller about time",
  "Feel-good romantic comedy for a cozy night",
  "Intense action movie with stunning visuals",
  "A deep psychological drama about identity",
  "Animated adventure for the whole family",
  "Horror movie that keeps you on edge",
];

export default function SearchBar() {
  const [query, setQuery] = useState('');
  const [language, setLanguage] = useState('');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showResults, setShowResults] = useState(false);
  const [placeholderIdx, setPlaceholderIdx] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  // Cycling placeholder
  useEffect(() => {
    const interval = setInterval(() => {
      setPlaceholderIdx(prev => (prev + 1) % EXAMPLE_QUERIES.length);
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  const handleSearch = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setError('');
    setShowResults(false);
    try {
      const resp = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/recommend`, {
        query,
        language: language || undefined,
      });
      setResults(resp.data.recommendations || []);
      setShowResults(true);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch recommendations. Please ensure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (q: string) => {
    setQuery(q);
    inputRef.current?.focus();
  };

  return (
    <section className="w-full max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12 animate-fade-in-up">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/[0.08] border border-primary/[0.12] text-primary text-xs font-medium mb-6 animate-pulse-glow">
          <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
          Powered by Voyage AI
        </div>
        <h1 className="text-5xl md:text-7xl font-black font-display gradient-text-hero mb-6 leading-tight tracking-tight">
          What are you in<br />the mood for?
        </h1>
        <p className="text-gray-400 text-base md:text-lg max-w-2xl mx-auto leading-relaxed">
          Describe a feeling, a scenario, or simply what you want to watch — our AI finds the perfect movie in any language.
        </p>
      </div>

      {/* Search Form */}
      <form onSubmit={handleSearch} className="mb-8 animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
        <div className="search-glow">
          <div className="card-glass p-2 flex flex-col md:flex-row gap-2">
            {/* Language Selector */}
            <div className="relative flex-shrink-0">
              <select
                value={language}
                onChange={e => setLanguage(e.target.value)}
                className="appearance-none w-full md:w-44 h-full px-4 py-3.5 bg-white/[0.04] hover:bg-white/[0.06] rounded-xl text-sm text-white font-medium focus:outline-none focus:ring-1 focus:ring-primary/30 border border-white/[0.04] cursor-pointer transition-colors"
              >
                {LANGUAGES.map(l => (
                  <option key={l.code} value={l.code} className="bg-surface text-white">
                    {l.flag} {l.label}
                  </option>
                ))}
              </select>
              <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-gray-500">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>

            {/* Search Input */}
            <input
              ref={inputRef}
              className="flex-1 px-5 py-3.5 bg-transparent text-white placeholder-gray-500 focus:outline-none text-base"
              placeholder={EXAMPLE_QUERIES[placeholderIdx]}
              value={query}
              onChange={e => setQuery(e.target.value)}
              disabled={loading}
            />

            {/* Submit Button */}
            <button
              className="btn-primary px-8 py-3.5 rounded-xl flex items-center justify-center gap-2.5 text-sm font-semibold min-w-[140px]"
              type="submit"
              disabled={loading || !query.trim()}
            >
              {loading ? (
                <>
                  <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Searching...
                </>
              ) : (
                <>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  Discover
                </>
              )}
            </button>
          </div>
        </div>
      </form>

      {/* Quick Suggestions */}
      {!showResults && !loading && (
        <div className="flex flex-wrap justify-center gap-2 mb-12 animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
          {EXAMPLE_QUERIES.slice(0, 4).map((q, i) => (
            <button
              key={i}
              onClick={() => handleExampleClick(q)}
              className="px-4 py-2 rounded-full bg-white/[0.03] border border-white/[0.06] text-xs text-gray-400 hover:text-white hover:bg-white/[0.06] hover:border-white/[0.1] transition-all duration-300"
            >
              {q}
            </button>
          ))}
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="flex items-center justify-center gap-3 py-4 px-6 rounded-xl bg-red-500/10 border border-red-500/20 text-red-300 text-sm mb-8 animate-fade-in">
          <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          {error}
        </div>
      )}

      {/* Results */}
      {showResults && results.length > 0 && (
        <div className="animate-fade-in-up">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-1 h-8 rounded-full bg-gradient-to-b from-primary to-accent" />
            <h2 className="text-2xl font-bold font-display text-white">
              Top Matches
            </h2>
            <span className="px-2.5 py-0.5 rounded-full bg-white/[0.06] text-xs text-gray-400 font-medium">
              {results.length} found
            </span>
            {language && (
              <span className="px-2.5 py-0.5 rounded-full bg-primary/10 text-xs text-primary font-medium border border-primary/20">
                {LANGUAGES.find(l => l.code === language)?.flag} {LANGUAGES.find(l => l.code === language)?.label}
              </span>
            )}
          </div>

          <Carousel>
            {results.map((movie, i) => (
              <div key={movie.id || movie.title + i} className="snap-center">
                <MovieCard movie={movie} index={i} />
              </div>
            ))}
          </Carousel>
        </div>
      )}

      {/* No Results */}
      {showResults && results.length === 0 && !loading && (
        <div className="text-center py-16 animate-fade-in">
          <div className="text-6xl mb-4">🎬</div>
          <h3 className="text-xl font-bold text-gray-300 mb-2">No movies found</h3>
          <p className="text-gray-500">Try a different query or change the language filter.</p>
        </div>
      )}
    </section>
  );
}
