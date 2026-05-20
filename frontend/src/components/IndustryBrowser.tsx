import { useState, useEffect } from 'react';
import axios from 'axios';
import { MovieCard } from './MovieCard';

type IndustryMovie = Record<string, unknown>;

type IndustryEntry = {
  industry: typeof INDUSTRIES[number];
  movies: IndustryMovie[];
};

const INDUSTRIES = [
  { id: 'hollywood', label: 'Hollywood', flag: '🎬', color: 'from-blue-600' },
  { id: 'bollywood', label: 'Bollywood', flag: '🇮🇳', color: 'from-orange-600' },
  { id: 'tollywood', label: 'Tollywood', flag: '🇮🇳', color: 'from-green-600' },
  { id: 'kollywood', label: 'Kollywood', flag: '🇮🇳', color: 'from-red-600' },
  { id: 'sandalwood', label: 'Sandalwood', flag: '🇮🇳', color: 'from-yellow-600' },
  { id: 'mollywood', label: 'Mollywood', flag: '🇮🇳', color: 'from-pink-600' },
  { id: 'korean', label: 'Korean Cinema', flag: '🇰🇷', color: 'from-purple-600' },
  { id: 'japanese', label: 'Japanese Cinema', flag: '🇯🇵', color: 'from-red-500' },
  { id: 'anime', label: 'Anime', flag: '✨', color: 'from-violet-600' },
  { id: 'international', label: 'International', flag: '🌍', color: 'from-cyan-600' },
];

export default function IndustryBrowser() {
  const [industryData, setIndustryData] = useState<IndustryEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAllIndustries = async () => {
      setLoading(true);
      setIndustryData([]);
      try {
        for (const industry of INDUSTRIES) {
          try {
            const resp = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/industry/recommendations`, {
              industry: industry.id,
              query: `latest ${industry.id} movies`,
              top_k: 20,
            });
            const movies = resp.data.recommendations || resp.data || [];
            if (movies.length > 0) {
              setIndustryData(prev => [...prev, { industry, movies }]);
            }
          } catch (err) {
            console.error(`Failed to fetch ${industry.id} movies`, err);
          }
          // Small delay to prevent VoyageAI 429 Too Many Requests
          await new Promise(r => setTimeout(r, 250));
        }
      } catch (err) {
        console.error("Failed to fetch industries", err);
      } finally {
        setLoading(false);
      }
    };

    fetchAllIndustries();
  }, []);

  if (loading && industryData.length === 0) {
    return (
      <div className="w-full flex items-center justify-center py-20">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary mb-4" />
          <p className="text-gray-400">Loading industry catalogs...</p>
        </div>
      </div>
    );
  }

  if (!loading && industryData.length === 0) {
    return (
      <div className="w-full text-center py-20">
        <p className="text-gray-400">No movies found in any industry</p>
      </div>
    );
  }

  return (
    <div className="w-full space-y-12">
      {industryData.map(({ industry, movies }) => (
        <div key={industry.id} className="relative group">
          <div className="flex items-center gap-3 mb-6">
            <span className="text-3xl">{industry.flag}</span>
            <h2 className="text-2xl md:text-3xl font-bold text-white capitalize flex items-center">
              {industry.label} <span className="text-gray-400 text-lg ml-3 font-normal">({movies.length})</span>
            </h2>
          </div>
          
          <div className="flex overflow-x-auto gap-4 pb-6 snap-x [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
            {movies.map((movie, i) => (
              <div key={i} className="min-w-[240px] md:min-w-[280px] snap-start flex-shrink-0 transition-transform duration-300 hover:-translate-y-2">
                <MovieCard movie={movie} />
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
