import Image from 'next/image';
import Link from 'next/link';

const LANG_NAMES: Record<string, string> = {
  en: 'English', hi: 'Hindi', es: 'Spanish', fr: 'French',
  ja: 'Japanese', ko: 'Korean', de: 'German', it: 'Italian',
  zh: 'Chinese', pt: 'Portuguese', ru: 'Russian', ar: 'Arabic',
  te: 'Telugu', ta: 'Tamil', ml: 'Malayalam', bn: 'Bengali',
  th: 'Thai', tr: 'Turkish', pl: 'Polish', nl: 'Dutch',
  sv: 'Swedish', da: 'Danish', no: 'Norwegian', fi: 'Finnish',
  id: 'Indonesian', ms: 'Malay', vi: 'Vietnamese', tl: 'Filipino',
  uk: 'Ukrainian', cs: 'Czech', ro: 'Romanian', hu: 'Hungarian',
  el: 'Greek', he: 'Hebrew', fa: 'Persian', ur: 'Urdu',
  kn: 'Kannada', mr: 'Marathi', gu: 'Gujarati', pa: 'Punjabi',
};

const LANG_BADGE_CLASSES: Record<string, string> = {
  en: 'lang-badge-en', hi: 'lang-badge-hi', es: 'lang-badge-es',
  fr: 'lang-badge-fr', ja: 'lang-badge-ja', ko: 'lang-badge-ko',
  de: 'lang-badge-de', it: 'lang-badge-it', zh: 'lang-badge-zh',
  te: 'lang-badge-te', ta: 'lang-badge-ta', ml: 'lang-badge-ml',
};

type Props = {
  movie: {
    title: string;
    overview: string;
    poster_url: string;
    rating: number;
    score: number;
    reason: string;
    id?: number;
    language?: string;
    genres?: string;
    year?: string;
  };
  index?: number;
};

export function MovieCard({ movie, index = 0 }: Props) {
  const matchPercent = Math.round(movie.score * 100);
  const lang = movie.language || 'en';
  const langName = LANG_NAMES[lang] || lang.toUpperCase();
  const badgeClass = LANG_BADGE_CLASSES[lang] || 'lang-badge-default';

  return (
    <div
      className="card-glass-hover w-[280px] flex flex-col flex-shrink-0 overflow-hidden snap-center"
      style={{ animationDelay: `${index * 0.08}s` }}
    >
      {/* Poster */}
      <div className="relative w-full aspect-[2/3] overflow-hidden group/poster">
        {movie.poster_url ? (
          <>
            <Image
              src={movie.poster_url}
              alt={movie.title}
              fill
              sizes="280px"
              className="object-cover transition-transform duration-700 ease-out group-hover/poster:scale-110"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-surface via-surface/20 to-transparent opacity-60 group-hover/poster:opacity-40 transition-opacity duration-500" />
          </>
        ) : (
          <div className="w-full h-full bg-surface-light flex items-center justify-center">
            <svg className="w-16 h-16 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        )}

        {/* Match Score Badge */}
        <div className="absolute top-3 right-3 z-10">
          <div className={`px-2.5 py-1 rounded-lg text-xs font-bold backdrop-blur-xl shadow-lg ${
            matchPercent >= 80
              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-400/30'
              : matchPercent >= 60
              ? 'bg-amber-500/20 text-amber-300 border border-amber-400/30'
              : 'bg-white/10 text-gray-300 border border-white/10'
          }`}>
            {matchPercent}% match
          </div>
        </div>

        {/* Language Badge */}
        <div className="absolute top-3 left-3 z-10">
          <span className={`lang-badge ${badgeClass}`}>
            {langName}
          </span>
        </div>

        {/* Hover Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-surface via-transparent to-transparent opacity-0 group-hover/poster:opacity-100 transition-opacity duration-500 flex items-end p-4">
          <Link
            href={`/movie/${movie.id || movie.title}`}
            className="btn-primary w-full text-center text-sm py-2.5"
          >
            View Details →
          </Link>
        </div>
      </div>

      {/* Content */}
      <div className="p-4 flex flex-col flex-1">
        <h3 className="text-base font-bold text-white mb-1 line-clamp-1 font-display">
          {movie.title}
        </h3>

        <div className="flex items-center gap-2 mb-3">
          {movie.year && (
            <span className="text-xs text-gray-500">{movie.year}</span>
          )}
          <span className="text-xs text-gray-500">•</span>
          <span className="text-xs text-amber-400 font-medium">⭐ {movie.rating?.toFixed(1) ?? 'N/A'}</span>
        </div>

        <p className="text-xs text-gray-400 line-clamp-2 mb-3 leading-relaxed">
          {movie.overview}
        </p>

        {/* AI Reason */}
        <div className="mt-auto">
          <div className="flex items-start gap-2 p-2.5 rounded-xl bg-primary/[0.06] border border-primary/[0.08]">
            <span className="text-primary text-sm mt-0.5 flex-shrink-0">✦</span>
            <p className="text-[11px] text-gray-300 line-clamp-2 leading-relaxed italic">
              {movie.reason}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
