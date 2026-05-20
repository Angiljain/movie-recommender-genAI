import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import axios from 'axios';
import Header from '@/components/Header';
import Image from 'next/image';
import Head from 'next/head';

const LANG_NAMES: Record<string, string> = {
  en: 'English', hi: 'Hindi', es: 'Spanish', fr: 'French',
  ja: 'Japanese', ko: 'Korean', de: 'German', it: 'Italian',
  zh: 'Chinese', pt: 'Portuguese', ru: 'Russian', ar: 'Arabic',
  te: 'Telugu', ta: 'Tamil', ml: 'Malayalam', bn: 'Bengali',
  th: 'Thai', tr: 'Turkish',
};

export default function MovieDetail() {
  const router = useRouter();
  const { id } = router.query;
  const [movie, setMovie] = useState<any | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (!id) return;
    axios
      .get(`${process.env.NEXT_PUBLIC_API_URL}/movie/${id}`)
      .then(res => setMovie(res.data))
      .catch(err => {
        console.error(err);
        setError(true);
      });
  }, [id]);

  if (error) return (
    <>
      <Head><title>Movie Not Found — MovieGenAI</title></Head>
      <div className="min-h-screen bg-background">
        <Header />
        <div className="flex flex-col items-center justify-center min-h-screen gap-4">
          <div className="text-6xl">😕</div>
          <p className="text-xl text-gray-300 font-medium">Movie not found</p>
          <button
            onClick={() => router.push('/')}
            className="btn-primary mt-4"
          >
            ← Back to Discover
          </button>
        </div>
      </div>
    </>
  );

  if (!movie) return (
    <div className="min-h-screen bg-background flex justify-center items-center">
      <div className="flex flex-col items-center gap-4">
        <svg className="animate-spin h-10 w-10 text-primary" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
        <span className="text-gray-500 text-sm">Loading movie details...</span>
      </div>
    </div>
  );

  const lang = movie.original_language || 'en';
  const langName = LANG_NAMES[lang] || lang.toUpperCase();

  return (
    <>
      <Head>
        <title>{movie.title} — MovieGenAI</title>
        <meta name="description" content={movie.overview?.slice(0, 160)} />
      </Head>

      <div className="min-h-screen bg-background relative">
        <Header />

        {/* Hero Backdrop */}
        {movie.backdrop_url && (
          <div className="absolute top-0 inset-x-0 h-[70vh] z-0">
            <Image
              src={movie.backdrop_url}
              alt="Backdrop"
              fill
              className="object-cover"
              priority
            />
            <div className="absolute inset-0 bg-gradient-to-b from-background/30 via-background/60 to-background" />
            <div className="absolute inset-0 bg-gradient-to-r from-background/50 to-transparent" />
          </div>
        )}

        <main className="relative z-10 container mx-auto pt-32 md:pt-40 px-6 pb-20 flex flex-col md:flex-row gap-10 lg:gap-16 items-start max-w-6xl">
          {/* Poster */}
          {movie.poster_url && (
            <div className="w-full md:w-[300px] lg:w-[350px] flex-shrink-0 animate-fade-in-up">
              <div className="rounded-2xl overflow-hidden shadow-2xl shadow-black/50 border border-white/[0.06]">
                <Image
                  src={movie.poster_url}
                  alt={movie.title}
                  width={500}
                  height={750}
                  className="w-full h-auto"
                />
              </div>
            </div>
          )}

          {/* Details */}
          <section className="flex-1 space-y-6 animate-fade-in-up" style={{ animationDelay: '0.15s' }}>
            {/* Title */}
            <div>
              <h1 className="text-4xl md:text-6xl font-black font-display gradient-text-hero leading-tight mb-3">
                {movie.title}
              </h1>
              {movie.release_date && (
                <span className="text-lg text-gray-400">
                  {movie.release_date.split('-')[0]}
                </span>
              )}
            </div>

            {/* Badges */}
            <div className="flex flex-wrap gap-2">
              {movie.genres_text?.split(',').map((genre: string) => (
                <span
                  key={genre}
                  className="px-3.5 py-1.5 rounded-xl bg-white/[0.06] text-sm font-medium text-gray-300 border border-white/[0.06] hover:bg-white/[0.1] transition-colors"
                >
                  {genre.trim()}
                </span>
              ))}
              <span className="px-3.5 py-1.5 rounded-xl bg-primary/[0.1] text-sm font-medium text-primary border border-primary/[0.15]">
                🌐 {langName}
              </span>
            </div>

            {/* Stats */}
            <div className="flex items-center gap-8 py-4">
              <div className="flex flex-col">
                <span className="text-xs text-gray-500 uppercase tracking-wider mb-1">Rating</span>
                <div className="flex items-center gap-2">
                  <span className="text-3xl font-bold text-amber-400">⭐</span>
                  <span className="text-2xl font-bold text-white">
                    {movie.vote_average?.toFixed(1) || 'N/A'}
                  </span>
                  <span className="text-sm text-gray-500">/ 10</span>
                </div>
              </div>
              <div className="w-px h-12 bg-white/10" />
              <div className="flex flex-col">
                <span className="text-xs text-gray-500 uppercase tracking-wider mb-1">Popularity</span>
                <span className="text-2xl font-bold text-white">
                  {movie.popularity?.toFixed(0) || 'N/A'}
                </span>
              </div>
              {movie.runtime && (
                <>
                  <div className="w-px h-12 bg-white/10" />
                  <div className="flex flex-col">
                    <span className="text-xs text-gray-500 uppercase tracking-wider mb-1">Runtime</span>
                    <span className="text-2xl font-bold text-white">
                      {Math.floor(movie.runtime / 60)}h {movie.runtime % 60}m
                    </span>
                  </div>
                </>
              )}
            </div>

            {/* Overview */}
            <div className="pt-4 border-t border-white/[0.06]">
              <h2 className="text-lg font-bold font-display text-white mb-3 flex items-center gap-2">
                <div className="w-1 h-5 rounded-full bg-gradient-to-b from-primary to-accent" />
                Overview
              </h2>
              <p className="text-base text-gray-300 leading-relaxed">
                {movie.overview}
              </p>
            </div>

            {/* Back button */}
            <button
              onClick={() => router.push('/')}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white/[0.04] border border-white/[0.06] text-sm text-gray-400 hover:text-white hover:bg-white/[0.08] transition-all duration-300 mt-4"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              Back to Discover
            </button>
          </section>
        </main>
      </div>
    </>
  );
}
