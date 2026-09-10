import React from 'react';
import { 
  Scissors, Compass, Layers, Users, BookOpen, 
  Sun, Moon, Globe, ShieldCheck, User 
} from 'lucide-react';

export default function Navbar({ 
  currentTab, 
  setCurrentTab, 
  lang, 
  setLang, 
  darkMode, 
  setDarkMode, 
  activeProfile, 
  t 
}) {
  return (
    <header className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 sticky top-0 z-40 shadow-sm transition-colors duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Brand Logo & Studio title */}
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setCurrentTab('studio')}>
            <div className="bg-brand text-white p-2.5 rounded-xl shadow-md transition-transform hover:scale-105">
              <Scissors className="h-5 w-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-base font-extrabold tracking-wide text-slate-900 dark:text-white">
                  JPPatternCreator
                </span>
                <span className="text-[10px] uppercase font-black px-2 py-0.5 rounded bg-brand/10 text-brand dark:text-brand-light border border-brand/20">
                  CAD STUDIO 15C
                </span>
              </div>
              <p className="text-[10px] text-slate-500 dark:text-slate-400 font-medium hidden sm:block">
                Historické krejčovství • Pozdní středověk
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="hidden md:flex items-center space-x-1">
            <button
              onClick={() => setCurrentTab('catalog')}
              className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
                currentTab === 'catalog'
                  ? 'bg-brand text-white shadow-sm'
                  : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
              }`}
            >
              <Layers className="h-4 w-4" />
              {t.navCatalog}
            </button>

            <button
              onClick={() => setCurrentTab('studio')}
              className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
                currentTab === 'studio'
                  ? 'bg-brand text-white shadow-sm'
                  : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
              }`}
            >
              <Compass className="h-4 w-4" />
              {t.navStudio}
            </button>

            <button
              onClick={() => setCurrentTab('profiles')}
              className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
                currentTab === 'profiles'
                  ? 'bg-brand text-white shadow-sm'
                  : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
              }`}
            >
              <Users className="h-4 w-4" />
              {t.navProfiles}
            </button>

            <button
              onClick={() => setCurrentTab('guide')}
              className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-2 ${
                currentTab === 'guide'
                  ? 'bg-brand text-white shadow-sm'
                  : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'
              }`}
            >
              <BookOpen className="h-4 w-4" />
              {t.navGuide}
            </button>
          </nav>

          {/* Right Controls: Active profile, Privacy badge, Theme & Lang toggles */}
          <div className="flex items-center gap-2.5">
            {activeProfile && (
              <div 
                onClick={() => setCurrentTab('profiles')}
                title={t.activeProfile}
                className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-bold bg-slate-100 dark:bg-slate-800/80 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700/60 cursor-pointer hover:border-brand/40"
              >
                <User className="h-3 w-3 text-brand dark:text-brand-light" />
                <span className="max-w-28 truncate">{activeProfile}</span>
              </div>
            )}

            <div className="hidden xl:flex items-center gap-1 text-[11px] font-semibold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/50 px-2 py-0.5 rounded-md">
              <ShieldCheck className="h-3.5 w-3.5" />
              <span>{t.privacyBadge}</span>
            </div>

            {/* Language Selector */}
            <button
              onClick={() => setLang(lang === 'CZ' ? 'EN' : 'CZ')}
              className="p-2 rounded-xl border border-slate-200 dark:border-slate-700/60 text-xs font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors flex items-center gap-1.5"
              title="Přepnout jazyk / Switch Language"
            >
              <Globe className="h-3.5 w-3.5 text-brand dark:text-brand-light" />
              <span>{lang}</span>
            </button>

            {/* Dark / Light Toggle */}
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="p-2 rounded-xl border border-slate-200 dark:border-slate-700/60 text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
              title={darkMode ? t.themeLight : t.themeDark}
            >
              {darkMode ? <Sun className="h-4 w-4 text-amber-400" /> : <Moon className="h-4 w-4 text-slate-600" />}
            </button>
          </div>

        </div>

        {/* Mobile Navigation Bar */}
        <div className="md:hidden flex items-center justify-around py-2 border-t border-slate-100 dark:border-slate-800 text-[11px] font-bold">
          <button
            onClick={() => setCurrentTab('catalog')}
            className={`flex items-center gap-1 py-1 px-2 rounded-lg ${currentTab === 'catalog' ? 'text-brand dark:text-brand-light' : 'text-slate-500'}`}
          >
            <Layers className="h-4 w-4" /> {t.navCatalog}
          </button>
          <button
            onClick={() => setCurrentTab('studio')}
            className={`flex items-center gap-1 py-1 px-2 rounded-lg ${currentTab === 'studio' ? 'text-brand dark:text-brand-light' : 'text-slate-500'}`}
          >
            <Compass className="h-4 w-4" /> {t.navStudio}
          </button>
          <button
            onClick={() => setCurrentTab('profiles')}
            className={`flex items-center gap-1 py-1 px-2 rounded-lg ${currentTab === 'profiles' ? 'text-brand dark:text-brand-light' : 'text-slate-500'}`}
          >
            <Users className="h-4 w-4" /> {t.navProfiles}
          </button>
          <button
            onClick={() => setCurrentTab('guide')}
            className={`flex items-center gap-1 py-1 px-2 rounded-lg ${currentTab === 'guide' ? 'text-brand dark:text-brand-light' : 'text-slate-500'}`}
          >
            <BookOpen className="h-4 w-4" /> {t.navGuide}
          </button>
        </div>
      </div>
    </header>
  );
}
