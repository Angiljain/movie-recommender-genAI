import Header from '@/components/Header';
import SearchBar from '@/components/SearchBar';
import Head from 'next/head';

export default function Home() {
  return (
    <>
      <Head>
        <title>MovieGenAI — AI-Powered Movie Recommendations</title>
        <meta name="description" content="Discover your next favorite movie with AI-powered semantic recommendations. Search by mood, theme, language or feeling." />
      </Head>

      <div className="min-h-screen relative overflow-hidden bg-background">
        <Header />

        {/* Background Orbs */}
        <div className="absolute top-[-20%] left-[-10%] w-[600px] h-[600px] bg-primary/[0.07] blur-[180px] rounded-full pointer-events-none animate-orb-drift" />
        <div className="absolute top-[20%] right-[-15%] w-[500px] h-[500px] bg-accent/[0.05] blur-[150px] rounded-full pointer-events-none animate-orb-drift" style={{ animationDelay: '-7s' }} />
        <div className="absolute bottom-[-10%] left-[20%] w-[400px] h-[400px] bg-primary/[0.04] blur-[120px] rounded-full pointer-events-none animate-orb-drift" style={{ animationDelay: '-14s' }} />

        {/* Grid Pattern */}
        <div
          className="absolute inset-0 pointer-events-none opacity-[0.015]"
          style={{
            backgroundImage: `linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)`,
            backgroundSize: '60px 60px',
          }}
        />

        <main className="relative z-10 min-h-screen pt-32 md:pt-40 pb-20 container mx-auto px-4 flex flex-col items-center">
          <SearchBar />
        </main>

        {/* Bottom Gradient */}
        <div className="absolute bottom-0 inset-x-0 h-32 bg-gradient-to-t from-background to-transparent pointer-events-none" />
      </div>
    </>
  );
}
