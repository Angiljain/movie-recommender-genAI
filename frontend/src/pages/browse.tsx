import Header from '@/components/Header';
import IndustryBrowser from '@/components/IndustryBrowser';

export default function Browse() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="relative z-10 container mx-auto pt-24 pb-16 px-4">
        {/* Page Title */}
        <div className="mb-12 animate-fade-in-up">
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Browse by Cinema Industry
          </h1>
          <p className="text-gray-400 text-lg">
            Explore movies from Hollywood, Bollywood, and cinemas around the world
          </p>
        </div>

        {/* Industry Browser */}
        <IndustryBrowser />
      </main>

      {/* Background decorations */}
      <div className="absolute top-0 -left-1/4 w-1/2 h-1/2 bg-primary/20 blur-[150px] rounded-full pointer-events-none"></div>
      <div className="absolute bottom-0 -right-1/4 w-1/2 h-1/2 bg-accent/20 blur-[150px] rounded-full pointer-events-none"></div>
    </div>
  );
}
