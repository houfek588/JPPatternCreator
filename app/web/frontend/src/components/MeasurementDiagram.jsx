import React from 'react';
import { Ruler, Info } from 'lucide-react';

const MEASUREMENT_INFO = {
  VP: {
    cz: "Celková výška postavy od temene hlavy k podlaze (bez bot).",
    en: "Total height from the crown of the head to the floor (barefoot)."
  },
  OP: {
    cz: "Obvod pasu v nejužším přirozeném místě nad boky (kde sedí pas kabátce/nohavic).",
    en: "Waist circumference at the narrowest natural point above hips."
  },
  OS: {
    cz: "Obvod sedu / boků přes nejvystouplejší část hýždí vodorovně.",
    en: "Hip / seat circumference measured horizontally around the fullest part of buttocks."
  },
  BDK: {
    cz: "Boční délka od linie pasu po vnější straně nohy až k podlaze.",
    en: "Outer side leg length from the waistline down to the ground."
  },
  KD: {
    cz: "Kroková délka (vnitřní délka nohy) od rozkroku k zemi.",
    en: "Inseam length from the crotch point down to the ground."
  },
  O_st: {
    cz: "Obvod stehna v nejširším horním místě těsně pod rozkrokem.",
    en: "Thigh circumference at the widest upper point just below crotch."
  },
  O_nk: {
    cz: "Obvod těsně nad kolenem (stěžejní pro anatomické přiléhání).",
    en: "Circumference measured immediately above the knee."
  },
  O_l: {
    cz: "Obvod lýtka v nejširším vyklenutém místě lýtkového svalu.",
    en: "Calf circumference at the fullest curve of the calf muscle."
  },
  O_kot: {
    cz: "Obvod kotníku přes kotníkové kosti (nejužší část nohy).",
    en: "Ankle circumference over the ankle bones."
  },
  OH: {
    cz: "Obvod hrudníku vodorovně přes nejširší část prsou pod pažemi.",
    en: "Chest circumference horizontally around the fullest part under armpits."
  },
  DZ: {
    cz: "Délka zad od 7. krčního obratle (týlu) k pasové linii.",
    en: "Back length from the prominent 7th cervical vertebra to the waist."
  },
  Szad: {
    cz: "Šířka zad mezi zadními úpony podpažních jamek přes lopatky.",
    en: "Back width measured across shoulder blades between armpits."
  }
};

export default function MeasurementDiagram({ activeField, patternType, lang = 'CZ' }) {
  const isHosen = patternType === 'hosen';
  const info = activeField && MEASUREMENT_INFO[activeField] 
    ? (lang === 'CZ' ? MEASUREMENT_INFO[activeField].cz : MEASUREMENT_INFO[activeField].en)
    : null;

  return (
    <div className="bg-slate-50 dark:bg-slate-950/60 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 relative overflow-hidden transition-all">
      <div className="flex items-center justify-between mb-2 pb-2 border-b border-slate-200 dark:border-slate-800/80">
        <div className="flex items-center gap-1.5 text-xs font-bold text-slate-700 dark:text-slate-300">
          <Ruler className="h-3.5 w-3.5 text-brand dark:text-brand-light" />
          <span>{lang === 'CZ' ? 'Vizuální průvodce mírou' : 'Visual Measurement Guide'}</span>
        </div>
        {activeField && (
          <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded bg-brand text-white shadow-xs">
            {activeField}
          </span>
        )}
      </div>

      <div className="flex items-center justify-center py-2">
        <svg viewBox="0 0 160 260" className="w-32 h-52 select-none">
          {/* Stylized Human Silhouette */}
          <g className="fill-slate-200 dark:fill-slate-800 stroke-slate-300 dark:stroke-slate-700" strokeWidth="1.5">
            {/* Head */}
            <ellipse cx="80" cy="22" rx="12" ry="15" />
            {/* Neck & Shoulders */}
            <path d="M74,37 L86,37 L98,48 L104,80 L96,85 L90,60 L70,60 L64,85 L56,80 L62,48 Z" />
            {/* Torso */}
            <path d="M68,58 L92,58 L90,95 L88,110 L72,110 L70,95 Z" />
            {/* Pelvis & Hips */}
            <path d="M72,110 L88,110 L94,130 L82,145 L78,145 L66,130 Z" />
            {/* Left Leg */}
            <path d="M66,132 L77,143 L74,185 L73,215 L71,240 L64,242 L65,215 L66,185 L60,140 Z" />
            {/* Right Leg */}
            <path d="M94,132 L83,143 L86,185 L87,215 L89,240 L96,242 L95,215 L94,185 L100,140 Z" />
          </g>

          {/* Measurement Lines (dynamic glow based on activeField) */}
          
          {/* VP: Total Height */}
          <g opacity={activeField === 'VP' ? 1 : 0.2}>
            <line x1="30" y1="7" x2="30" y2="242" stroke="#e11d48" strokeWidth={activeField === 'VP' ? "2.5" : "1"} strokeDasharray="3,2" />
            <line x1="25" y1="7" x2="35" y2="7" stroke="#e11d48" strokeWidth="2" />
            <line x1="25" y1="242" x2="35" y2="242" stroke="#e11d48" strokeWidth="2" />
          </g>

          {/* OH: Chest */}
          <g opacity={activeField === 'OH' ? 1 : 0.2}>
            <line x1="64" y1="65" x2="96" y2="65" stroke="#e11d48" strokeWidth={activeField === 'OH' ? "3" : "1.5"} />
            <circle cx="80" cy="65" r={activeField === 'OH' ? "3" : "1.5"} fill="#e11d48" />
          </g>

          {/* OP: Waist */}
          <g opacity={activeField === 'OP' ? 1 : 0.2}>
            <line x1="70" y1="95" x2="90" y2="95" stroke="#e11d48" strokeWidth={activeField === 'OP' ? "3" : "1.5"} />
            <circle cx="80" cy="95" r={activeField === 'OP' ? "3" : "1.5"} fill="#e11d48" />
          </g>

          {/* OS: Hips */}
          <g opacity={activeField === 'OS' ? 1 : 0.2}>
            <line x1="66" y1="128" x2="94" y2="128" stroke="#e11d48" strokeWidth={activeField === 'OS' ? "3" : "1.5"} />
            <circle cx="80" cy="128" r={activeField === 'OS' ? "3" : "1.5"} fill="#e11d48" />
          </g>

          {/* BDK: Side Length */}
          <g opacity={activeField === 'BDK' ? 1 : 0.2}>
            <line x1="108" y1="95" x2="108" y2="242" stroke="#e11d48" strokeWidth={activeField === 'BDK' ? "2.5" : "1"} strokeDasharray="3,2" />
            <line x1="103" y1="95" x2="113" y2="95" stroke="#e11d48" strokeWidth="2" />
            <line x1="103" y1="242" x2="113" y2="242" stroke="#e11d48" strokeWidth="2" />
          </g>

          {/* KD: Inseam / Crotch */}
          <g opacity={activeField === 'KD' ? 1 : 0.2}>
            <line x1="80" y1="145" x2="80" y2="242" stroke="#e11d48" strokeWidth={activeField === 'KD' ? "2.5" : "1"} strokeDasharray="3,2" />
            <line x1="76" y1="145" x2="84" y2="145" stroke="#e11d48" strokeWidth="2" />
            <line x1="76" y1="242" x2="84" y2="242" stroke="#e11d48" strokeWidth="2" />
          </g>

          {/* O_st: Thigh */}
          <g opacity={activeField === 'O_st' ? 1 : 0.2}>
            <line x1="60" y1="152" x2="77" y2="152" stroke="#e11d48" strokeWidth={activeField === 'O_st' ? "3" : "1.5"} />
          </g>

          {/* O_nk: Above Knee */}
          <g opacity={activeField === 'O_nk' ? 1 : 0.2}>
            <line x1="65" y1="180" x2="75" y2="180" stroke="#e11d48" strokeWidth={activeField === 'O_nk' ? "3" : "1.5"} />
          </g>

          {/* O_l: Calf */}
          <g opacity={activeField === 'O_l' ? 1 : 0.2}>
            <line x1="64" y1="210" x2="74" y2="210" stroke="#e11d48" strokeWidth={activeField === 'O_l' ? "3" : "1.5"} />
          </g>

          {/* O_kot: Ankle */}
          <g opacity={activeField === 'O_kot' ? 1 : 0.2}>
            <line x1="64" y1="235" x2="72" y2="235" stroke="#e11d48" strokeWidth={activeField === 'O_kot' ? "3" : "1.5"} />
          </g>

          {/* DZ: Back length */}
          <g opacity={activeField === 'DZ' ? 1 : 0.2}>
            <line x1="79" y1="38" x2="79" y2="95" stroke="#e11d48" strokeWidth={activeField === 'DZ' ? "2.5" : "1"} strokeDasharray="2,2" />
          </g>

          {/* Szad: Back width */}
          <g opacity={activeField === 'Szad' ? 1 : 0.2}>
            <line x1="66" y1="52" x2="94" y2="52" stroke="#e11d48" strokeWidth={activeField === 'Szad' ? "3" : "1.5"} />
          </g>
        </svg>
      </div>

      {/* Dynamic guidance explanation text */}
      <div className="mt-2 text-[11px] text-slate-600 dark:text-slate-400 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-2.5 flex items-start gap-2 shadow-xs">
        <Info className="h-4 w-4 text-brand dark:text-brand-light shrink-0 mt-0.5" />
        <p className="leading-tight">
          {info || (lang === 'CZ' 
            ? "Klikněte do jakéhokoliv pole míry vlevo – diagram zvýrazní, kde přesně na těle měřit." 
            : "Click into any measurement input field on the left – the diagram will highlight where to measure.")}
        </p>
      </div>
    </div>
  );
}
