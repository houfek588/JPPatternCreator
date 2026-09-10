import React from 'react';
import { BookOpen, Ruler, Printer, Info, CheckCircle2, Scissors, HelpCircle } from 'lucide-react';

export default function GuideView({ t }) {
  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-12">
      
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-extrabold bg-brand/10 text-brand dark:text-brand-light border border-brand/20">
          <BookOpen className="h-3.5 w-3.5" />
          <span>Krejčovská metodika 15. století</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-black text-slate-900 dark:text-white tracking-tight">
          {t.guideTitle}
        </h1>
        <p className="text-sm text-slate-600 dark:text-slate-400 font-medium leading-relaxed">
          {t.guideSubtitle}
        </p>
      </div>

      {/* Section 1: How to measure */}
      <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8 shadow-sm space-y-6">
        <div className="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">
          <div className="p-2.5 rounded-2xl bg-brand text-white shadow-md">
            <Ruler className="h-5 w-5" />
          </div>
          <div>
            <h2 className="text-lg font-black text-slate-900 dark:text-white">
              {t.guideHowToMeasureTitle}
            </h2>
            <p className="text-xs text-slate-500 font-medium">Základní zásady pro dosažení padnoucího historického střihu</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs text-slate-600 dark:text-slate-300">
          
          <div className="space-y-3 bg-slate-50 dark:bg-slate-950/60 p-5 rounded-2xl border border-slate-200/80 dark:border-slate-800/80">
            <h3 className="font-extrabold text-sm text-slate-900 dark:text-white flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-500" />
              1. Správný oděv při měření
            </h3>
            <p className="leading-relaxed font-medium">
              Vždy se měřte v tenkém spodním prádle nebo lněné spodní košili a spodkách (*braies*), které budete skutečně nosit pod zhotovovaným oděvem. Měření přes džíny nebo svetr povede k deformaci střihu.
            </p>
          </div>

          <div className="space-y-3 bg-slate-50 dark:bg-slate-950/60 p-5 rounded-2xl border border-slate-200/80 dark:border-slate-800/80">
            <h3 className="font-extrabold text-sm text-slate-900 dark:text-white flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-500" />
              2. Přirozený postoj těla
            </h3>
            <p className="leading-relaxed font-medium">
              Stůjte rovně, vzpřímeně s uvolněnými rameny a nohama rozkročenýma na šířku pánve. Nezatahujte břicho ani nevypínejte nepřirozeně hrudník – oděv 15. století musí umožňovat volný pohyb a šerm.
            </p>
          </div>

          <div className="space-y-3 bg-slate-50 dark:bg-slate-950/60 p-5 rounded-2xl border border-slate-200/80 dark:border-slate-800/80">
            <h3 className="font-extrabold text-sm text-slate-900 dark:text-white flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-500" />
              3. Rozdíl mezi BDK a KD
            </h3>
            <p className="leading-relaxed font-medium">
              <strong>BDK (Boční délka)</strong> je měřena od pasu po vnějším boku až k zemi. <strong>KD (Kroková délka)</strong> je měřena od nejvyššího bodu vnitřního rozkroku po kotník/zem. Rozdíl těchto měr přesně určuje hloubku a poloměr sedové křivky nohavic.
            </p>
          </div>

          <div className="space-y-3 bg-slate-50 dark:bg-slate-950/60 p-5 rounded-2xl border border-slate-200/80 dark:border-slate-800/80">
            <h3 className="font-extrabold text-sm text-slate-900 dark:text-white flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-500" />
              4. Zádová křivka kabátce (DZ a Szad)
            </h3>
            <p className="leading-relaxed font-medium">
              Kabátec 15. století těsně obepíná trup a lopatky. Míra <strong>DZ (Délka zad)</strong> od vystouplého 7. krčního obratle po linii pasu garantuje, že vázací dírky na nohavice (*points*) budou sedět přesně na úrovni kyčlí a nebudou táhnout.
            </p>
          </div>

        </div>
      </div>

      {/* Section 2: Printing & Assembly */}
      <div className="bg-white dark:bg-slate-900 rounded-3xl border border-slate-200 dark:border-slate-800 p-8 shadow-sm space-y-6">
        <div className="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">
          <div className="p-2.5 rounded-2xl bg-brand text-white shadow-md">
            <Printer className="h-5 w-5" />
          </div>
          <div>
            <h2 className="text-lg font-black text-slate-900 dark:text-white">
              {t.guidePrintingTitle}
            </h2>
            <p className="text-xs text-slate-500 font-medium">Jak správně vytisknout a zkontrolovat střih před stříháním látky</p>
          </div>
        </div>

        <div className="space-y-4 text-xs text-slate-600 dark:text-slate-300">
          <div className="flex items-start gap-4 p-4 rounded-2xl bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900/40">
            <Info className="h-5 w-5 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
            <div className="space-y-1">
              <span className="font-bold text-slate-900 dark:text-white">
                Kontrola kalibračního čtverce 10 × 10 cm
              </span>
              <p className="leading-relaxed font-medium">
                V každém vygenerovaném PDF je v rohu umístěn kontrolní čtverec o rozměru přesně 10 × 10 cm. Po vytištění jej změřte pravítkem. Pokud čtverec neodpovídá přesně 10 cm, zkontrolujte nastavení tiskárny – měřítko tisku musí být nastaveno na <strong>100 % (Skutečná velikost / Actual Size)</strong>, nikoliv „Přizpůsobit stránce“ (*Fit to Page*).
              </p>
            </div>
          </div>
        </div>
      </div>

    </div>
  );
}
