import React from 'react';
import { Layers, ArrowRight, CheckCircle, Sparkles, Clock, Shield } from 'lucide-react';

export default function GarmentCatalog({ onSelectGarment, t, lang }) {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      
      {/* Header Banner */}
      <div className="text-center max-w-3xl mx-auto mb-12 space-y-3">
        <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full text-xs font-extrabold bg-brand/10 text-brand dark:text-brand-light border border-brand/20">
          <Sparkles className="h-3.5 w-3.5" />
          <span>{t.historicalPeriod}</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-black text-slate-900 dark:text-white tracking-tight">
          {t.catalogTitle}
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400 font-medium leading-relaxed">
          {t.catalogSubtitle}
        </p>
      </div>

      {/* Garments Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        
        {/* Card 1: Hosen / Nohavice */}
        <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-7 shadow-sm hover:shadow-xl hover:border-brand/40 transition-all flex flex-col justify-between group">
          <div>
            <div className="flex justify-between items-start mb-4">
              <span className="text-[10px] font-black tracking-wider uppercase px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/50">
                15. Století • Living History
              </span>
              <div className="p-3 rounded-2xl bg-brand/10 text-brand dark:text-brand-light group-hover:scale-110 transition-transform">
                <Layers className="h-6 w-6" />
              </div>
            </div>

            <h2 className="text-xl font-black text-slate-900 dark:text-white mb-2">
              {t.garmentHosenTitle}
            </h2>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed mb-6 font-medium">
              {t.garmentHosenDesc}
            </p>

            <div className="space-y-2 mb-8">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                {lang === 'CZ' ? 'Dostupné prvky střihu:' : 'Available Pattern Elements:'}
              </span>
              {t.garmentHosenVariants.map((item, i) => (
                <div key={i} className="flex items-center gap-2 text-xs font-semibold text-slate-700 dark:text-slate-300">
                  <CheckCircle className="h-3.5 w-3.5 text-brand dark:text-brand-light" />
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </div>

          <button
            onClick={() => onSelectGarment('hosen')}
            className="w-full py-3 px-4 rounded-xl bg-brand hover:bg-brand-hover text-white font-bold text-xs flex items-center justify-center gap-2 shadow-md active:scale-95 transition-all cursor-pointer"
          >
            <span>{t.openInStudio}</span>
            <ArrowRight className="h-4 w-4" />
          </button>
        </div>

        {/* Card 2: Doublet / Pourpoint (Kabátec) */}
        <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-7 shadow-sm hover:shadow-xl hover:border-brand/40 transition-all flex flex-col justify-between group">
          <div>
            <div className="flex justify-between items-start mb-4">
              <span className="text-[10px] font-black tracking-wider uppercase px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/50">
                15. Století • Anatomický základ
              </span>
              <div className="p-3 rounded-2xl bg-brand/10 text-brand dark:text-brand-light group-hover:scale-110 transition-transform">
                <Shield className="h-6 w-6" />
              </div>
            </div>

            <h2 className="text-xl font-black text-slate-900 dark:text-white mb-2">
              {t.garmentBodiceTitle}
            </h2>
            <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed mb-6 font-medium">
              {t.garmentBodiceDesc}
            </p>

            <div className="space-y-2 mb-8">
              <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                {lang === 'CZ' ? 'Dostupné prvky střihu:' : 'Available Pattern Elements:'}
              </span>
              {t.garmentBodiceVariants.map((item, i) => (
                <div key={i} className="flex items-center gap-2 text-xs font-semibold text-slate-700 dark:text-slate-300">
                  <CheckCircle className="h-3.5 w-3.5 text-brand dark:text-brand-light" />
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </div>

          <button
            onClick={() => onSelectGarment('bodice')}
            className="w-full py-3 px-4 rounded-xl bg-brand hover:bg-brand-hover text-white font-bold text-xs flex items-center justify-center gap-2 shadow-md active:scale-95 transition-all cursor-pointer"
          >
            <span>{t.openInStudio}</span>
            <ArrowRight className="h-4 w-4" />
          </button>
        </div>

        {/* Card 3: Linen Shirt (V přípravě) */}
        <div className="bg-slate-50 dark:bg-slate-950/40 rounded-3xl border border-slate-200 dark:border-slate-800 p-7 flex flex-col justify-between opacity-80">
          <div>
            <div className="flex justify-between items-start mb-4">
              <span className="text-[10px] font-black tracking-wider uppercase px-2.5 py-1 rounded-lg bg-amber-50 text-amber-700 dark:bg-amber-950/50 dark:text-amber-300 border border-amber-200 dark:border-amber-800/50 flex items-center gap-1">
                <Clock className="h-3 w-3" />
                {t.garmentShirtComingSoon}
              </span>
            </div>

            <h2 className="text-xl font-black text-slate-700 dark:text-slate-300 mb-2">
              {t.garmentShirtTitle}
            </h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed mb-6 font-medium">
              {t.garmentShirtDesc}
            </p>

            <div className="bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 text-xs text-slate-500">
              Připravujeme deklarativní šablonu geometrie podle archeologických nálezů z hradu Lengberg.
            </div>
          </div>

          <div className="pt-8">
            <button
              disabled
              className="w-full py-3 px-4 rounded-xl bg-slate-200 dark:bg-slate-800 text-slate-400 font-bold text-xs cursor-not-allowed"
            >
              {t.garmentShirtComingSoon}
            </button>
          </div>
        </div>

      </div>

    </div>
  );
}
