import React, { useState, useRef, useEffect } from 'react';
import { 
  ChevronDown, ChevronRight, Layers, 
  Ruler, Scissors, Download, Printer, Image, FileCode, 
  Loader2, Sparkles, CheckCircle2 
} from 'lucide-react';
import MeasurementDiagram from './MeasurementDiagram';
import CadCanvas from './CadCanvas';

export default function CadStudio({
  patternType,
  setPatternType,
  inputs,
  setInputs,
  sliders,
  setSliders,
  part,
  setPart,
  svgString,
  handles,
  loading,
  validationError,
  activeProfile,
  t,
  lang,
  exportPDF,
  exportPNG,
  exportSVG,
  exportingPdf,
  exportingPng,
  exportingSvg,
  inputConfigs
}) {
  // Accordion Step State: 'variant' | 'measurements' | 'cad'
  const [openStep, setOpenStep] = useState('measurements');
  const [activeField, setActiveField] = useState('VP');
  const [exportDropdownOpen, setExportDropdownOpen] = useState(false);
  const exportDropdownRef = useRef(null);

  // CAD Options state
  const [seamAllowance, setSeamAllowance] = useState(false);
  const [seamWidth, setSeamWidth] = useState(1.0);
  const [showGrainline, setShowGrainline] = useState(true);
  const [showPoints, setShowPoints] = useState(true);

  // Click outside to close export dropdown
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (exportDropdownRef.current && !exportDropdownRef.current.contains(e.target)) {
        setExportDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleInputChange = (id, val) => {
    setInputs(prev => ({
      ...prev,
      [id]: id === 'title' ? val : (val === '' ? '' : parseFloat(val))
    }));
  };

  return (
    <div className="flex-1 flex flex-col min-h-screen overflow-hidden">
      
      {/* Top Workspace Bar */}
      <div className="bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-6 py-3.5 flex flex-col md:flex-row justify-between items-center gap-3 transition-colors shadow-xs z-30">
        
        {/* Title & Status */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <h2 className="text-sm font-extrabold text-slate-800 dark:text-white tracking-wide">
              {inputs.title || (lang === 'CZ' ? 'Střih bez názvu' : 'Untitled Pattern')}
            </h2>
            <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700/60">
              {patternType === 'hosen' ? t.garmentHosenTitle : t.garmentBodiceTitle}
            </span>
          </div>

          {activeProfile && (
            <span className="text-[10px] bg-brand/10 border border-brand/20 text-brand dark:text-brand-light px-2.5 py-0.5 rounded-full font-bold">
              {t.activeProfile}: {activeProfile}
            </span>
          )}

          {loading && (
            <div className="flex items-center gap-1.5 text-xs text-brand dark:text-brand-light font-extrabold animate-pulse">
              <Loader2 className="h-3.5 w-3.5 animate-spin" /> {t.drafting}
            </div>
          )}
        </div>

        {/* Center: Segmented Part Selector */}
        <div className="bg-slate-100 dark:bg-slate-950 p-1 rounded-xl border border-slate-200 dark:border-slate-800/80 flex items-center gap-1 text-[11px] font-bold">
          <button
            onClick={() => setPart('all')}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              part === 'all'
                ? 'bg-brand text-white shadow-sm font-extrabold'
                : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
            }`}
          >
            {t.partAll}
          </button>

          {patternType === 'hosen' ? (
            <>
              <button
                onClick={() => setPart('front')}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  part === 'front'
                    ? 'bg-brand text-white shadow-sm font-extrabold'
                    : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
                }`}
              >
                {t.partFront}
              </button>
              <button
                onClick={() => setPart('back')}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  part === 'back'
                    ? 'bg-brand text-white shadow-sm font-extrabold'
                    : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
                }`}
              >
                {t.partBack}
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => setPart('back')}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  part === 'back'
                    ? 'bg-brand text-white shadow-sm font-extrabold'
                    : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
                }`}
              >
                {t.partBack}
              </button>
              <button
                onClick={() => setPart('collar')}
                className={`px-3 py-1.5 rounded-lg transition-all ${
                  part === 'collar'
                    ? 'bg-brand text-white shadow-sm font-extrabold'
                    : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
                }`}
              >
                {t.partCollar}
              </button>
            </>
          )}
        </div>

        {/* Right: Unified Dropdown Export */}
        <div className="relative w-full md:w-auto" ref={exportDropdownRef}>
          <button 
            type="button"
            onClick={() => setExportDropdownOpen(prev => !prev)}
            disabled={exportingPdf || exportingPng || exportingSvg || loading}
            className="w-full sm:w-auto bg-brand hover:bg-brand-hover disabled:bg-slate-300 dark:disabled:bg-slate-800 text-white font-bold text-xs px-5 py-2.5 rounded-xl flex items-center justify-between sm:justify-center gap-2.5 transition-all shadow-md active:scale-95 cursor-pointer select-none"
          >
            <div className="flex items-center gap-2">
              {(exportingPdf || exportingPng || exportingSvg) ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Download className="h-4 w-4" />
              )}
              <span>{t.exportBtn}</span>
            </div>
            <ChevronDown className={`h-4 w-4 transition-transform duration-200 ${exportDropdownOpen ? 'rotate-180' : ''}`} />
          </button>

          {exportDropdownOpen && (
            <div className="absolute right-0 top-full mt-2 w-72 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-xl p-2 z-50 animate-in fade-in slide-in-from-top-2 duration-150">
              <div className="px-3 py-1.5 text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 border-b border-slate-100 dark:border-slate-800/80 mb-1">
                {t.exportOptionsTitle}
              </div>

              {/* PDF Option */}
              <button
                type="button"
                onClick={() => { setExportDropdownOpen(false); exportPDF(); }}
                disabled={exportingPdf || loading}
                className="w-full text-left px-3 py-2.5 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800/80 transition-colors flex items-center gap-3 cursor-pointer group disabled:opacity-50"
              >
                <div className="p-2 rounded-lg bg-red-100 dark:bg-red-950/50 text-red-600 dark:text-red-400 group-hover:scale-105 transition-transform">
                  <Printer className="h-4 w-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-xs font-bold text-slate-800 dark:text-slate-100">
                    {t.exportPdfOption}
                  </div>
                  <div className="text-[10px] text-slate-500 dark:text-slate-400 truncate">
                    {t.exportPdfDesc}
                  </div>
                </div>
              </button>

              {/* PNG Option */}
              <button
                type="button"
                onClick={() => { setExportDropdownOpen(false); exportPNG(); }}
                disabled={exportingPng || loading}
                className="w-full text-left px-3 py-2.5 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800/80 transition-colors flex items-center gap-3 cursor-pointer group disabled:opacity-50"
              >
                <div className="p-2 rounded-lg bg-sky-100 dark:bg-sky-950/50 text-sky-600 dark:text-sky-400 group-hover:scale-105 transition-transform">
                  <Image className="h-4 w-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-xs font-bold text-slate-800 dark:text-slate-100">
                    {t.exportPngOption}
                  </div>
                  <div className="text-[10px] text-slate-500 dark:text-slate-400 truncate">
                    {t.exportPngDesc}
                  </div>
                </div>
              </button>

              {/* SVG Option */}
              <button
                type="button"
                onClick={exportSVG}
                disabled={!svgString || loading}
                className="w-full text-left px-3 py-2.5 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800/80 transition-colors flex items-center gap-3 cursor-pointer group disabled:opacity-50"
              >
                <div className="p-2 rounded-lg bg-emerald-100 dark:bg-emerald-950/50 text-emerald-600 dark:text-emerald-400 group-hover:scale-105 transition-transform">
                  <FileCode className="h-4 w-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-xs font-bold text-slate-800 dark:text-slate-100">
                    {t.exportSvgOption}
                  </div>
                  <div className="text-[10px] text-slate-500 dark:text-slate-400 truncate">
                    {t.exportSvgDesc}
                  </div>
                </div>
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Studio Workspace Layout */}
      <div className="flex-1 flex flex-col md:flex-row overflow-hidden">
        
        {/* Left Control Panel: Stepper / Accordion */}
        <aside className="w-full md:w-[480px] bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col max-h-[calc(100vh-120px)] overflow-y-auto">
          
          <div className="p-5 space-y-4">
            
            {/* Step 1: Garment Archetype & Variant */}
            <div className="border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden transition-all shadow-xs">
              <button
                type="button"
                onClick={() => setOpenStep(openStep === 'variant' ? '' : 'variant')}
                className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-950/60 flex items-center justify-between font-bold text-xs text-slate-800 dark:text-slate-200"
              >
                <div className="flex items-center gap-2">
                  <Layers className="h-4 w-4 text-brand dark:text-brand-light" />
                  <span>{t.step1Variant}</span>
                </div>
                {openStep === 'variant' ? <ChevronDown className="h-4 w-4 text-slate-400" /> : <ChevronRight className="h-4 w-4 text-slate-400" />}
              </button>

              {openStep === 'variant' && (
                <div className="p-4 space-y-3 bg-white dark:bg-slate-900 border-t border-slate-100 dark:border-slate-800">
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      type="button"
                      onClick={() => setPatternType('hosen')}
                      className={`p-3 rounded-xl border text-left font-bold text-xs transition-all flex flex-col justify-between ${
                        patternType === 'hosen'
                          ? 'border-brand bg-brand/10 text-brand dark:text-brand-light shadow-xs'
                          : 'border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:border-slate-300'
                      }`}
                    >
                      <span className="font-extrabold">{t.garmentHosenTitle}</span>
                      <span className="text-[10px] text-slate-400 mt-1 font-normal">Nohavice pozdního středověku</span>
                    </button>

                    <button
                      type="button"
                      onClick={() => setPatternType('bodice')}
                      className={`p-3 rounded-xl border text-left font-bold text-xs transition-all flex flex-col justify-between ${
                        patternType === 'bodice'
                          ? 'border-brand bg-brand/10 text-brand dark:text-brand-light shadow-xs'
                          : 'border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:border-slate-300'
                      }`}
                    >
                      <span className="font-extrabold">{t.garmentBodiceTitle}</span>
                      <span className="text-[10px] text-slate-400 mt-1 font-normal">Kabátec / Doublet 15. stol.</span>
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Step 2: Body Measurements */}
            <div className="border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden transition-all shadow-xs">
              <button
                type="button"
                onClick={() => setOpenStep(openStep === 'measurements' ? '' : 'measurements')}
                className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-950/60 flex items-center justify-between font-bold text-xs text-slate-800 dark:text-slate-200"
              >
                <div className="flex items-center gap-2">
                  <Ruler className="h-4 w-4 text-brand dark:text-brand-light" />
                  <span>{t.step2Measurements}</span>
                </div>
                {openStep === 'measurements' ? <ChevronDown className="h-4 w-4 text-slate-400" /> : <ChevronRight className="h-4 w-4 text-slate-400" />}
              </button>

              {openStep === 'measurements' && (
                <div className="p-4 space-y-4 bg-white dark:bg-slate-900 border-t border-slate-100 dark:border-slate-800">
                  
                  {/* Dynamic Anatomical Guide Component */}
                  <MeasurementDiagram 
                    activeField={activeField} 
                    patternType={patternType} 
                    lang={lang} 
                  />

                  {/* Input Fields Grid */}
                  <div className="grid grid-cols-2 gap-3.5 pt-2">
                    {inputConfigs.map(item => (
                      <div key={item.id} className={item.id === 'title' ? 'col-span-2' : 'col-span-1'}>
                        <label className="block text-[11px] font-semibold text-slate-600 dark:text-slate-400 mb-1">
                          {t[`input_${item.id}`] || item.label}
                        </label>
                        <div className="relative">
                          <input
                            type={item.type}
                            placeholder={item.placeholder}
                            value={inputs[item.id] ?? ''}
                            onFocus={() => setActiveField(item.id)}
                            onChange={e => handleInputChange(item.id, e.target.value)}
                            className="glass-input w-full text-xs py-2 bg-white dark:bg-slate-950/60 border-slate-300 dark:border-slate-800 text-slate-900 dark:text-slate-100 focus:ring-brand focus:border-brand"
                          />
                          {item.unit && (
                            <span className="absolute right-3 top-2 text-[10px] text-slate-400 font-bold">
                              {item.unit}
                            </span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Interactive CAD Smart Handles Hint */}
                  <div className="bg-brand/5 dark:bg-brand/10 border border-brand/20 rounded-xl p-3 flex items-start gap-2.5 text-[11px] text-slate-600 dark:text-slate-300">
                    <Sparkles className="h-4 w-4 text-brand dark:text-brand-light shrink-0 mt-0.5" />
                    <div className="leading-snug">
                      <span className="font-extrabold text-slate-800 dark:text-slate-100 block mb-0.5">{t.cadHandlesToggle}</span>
                      {t.cadHandlesHelp}
                    </div>
                  </div>

                </div>
              )}
            </div>

            {/* Step 3: Tailoring CAD Options */}
            <div className="border border-slate-200 dark:border-slate-800 rounded-2xl overflow-hidden transition-all shadow-xs">
              <button
                type="button"
                onClick={() => setOpenStep(openStep === 'cad' ? '' : 'cad')}
                className="w-full px-4 py-3 bg-slate-50 dark:bg-slate-950/60 flex items-center justify-between font-bold text-xs text-slate-800 dark:text-slate-200"
              >
                <div className="flex items-center gap-2">
                  <Scissors className="h-4 w-4 text-brand dark:text-brand-light" />
                  <span>{t.step3CadOptions}</span>
                </div>
                {openStep === 'cad' ? <ChevronDown className="h-4 w-4 text-slate-400" /> : <ChevronRight className="h-4 w-4 text-slate-400" />}
              </button>

              {openStep === 'cad' && (
                <div className="p-4 space-y-4 bg-white dark:bg-slate-900 border-t border-slate-100 dark:border-slate-800 text-xs">
                  
                  {/* Seam Allowance */}
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="font-bold text-slate-800 dark:text-slate-200">{t.seamAllowanceTitle}</div>
                      <div className="text-[10px] text-slate-500">{t.seamAllowanceDesc}</div>
                    </div>
                    <input 
                      type="checkbox" 
                      checked={seamAllowance} 
                      onChange={e => setSeamAllowance(e.target.checked)} 
                      className="rounded accent-brand w-4 h-4 cursor-pointer"
                    />
                  </div>

                  {seamAllowance && (
                    <div className="flex items-center justify-between pl-3 border-l-2 border-brand/40">
                      <span className="text-slate-600 dark:text-slate-400">{t.seamAllowanceWidth}</span>
                      <div className="flex gap-1">
                        {[1.0, 1.5, 2.0].map(w => (
                          <button
                            key={w}
                            type="button"
                            onClick={() => setSeamWidth(w)}
                            className={`px-2 py-1 rounded text-[10px] font-bold ${seamWidth === w ? 'bg-brand text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400'}`}
                          >
                            {w} cm
                          </button>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Grainline */}
                  <div className="flex items-center justify-between pt-2 border-t border-slate-100 dark:border-slate-800">
                    <div>
                      <div className="font-bold text-slate-800 dark:text-slate-200">{t.grainlineTitle}</div>
                      <div className="text-[10px] text-slate-500">{t.grainlineDesc}</div>
                    </div>
                    <input 
                      type="checkbox" 
                      checked={showGrainline} 
                      onChange={e => setShowGrainline(e.target.checked)} 
                      className="rounded accent-brand w-4 h-4 cursor-pointer"
                    />
                  </div>

                  {/* Doublet Points / Lacing */}
                  <div className="flex items-center justify-between pt-2 border-t border-slate-100 dark:border-slate-800">
                    <div>
                      <div className="font-bold text-slate-800 dark:text-slate-200">{t.doubletPointsTitle}</div>
                      <div className="text-[10px] text-slate-500">{t.doubletPointsDesc}</div>
                    </div>
                    <input 
                      type="checkbox" 
                      checked={showPoints} 
                      onChange={e => setShowPoints(e.target.checked)} 
                      className="rounded accent-brand w-4 h-4 cursor-pointer"
                    />
                  </div>

                </div>
              )}
            </div>

          </div>

        </aside>

        {/* Right Canvas: Interactive CAD Viewport */}
        <CadCanvas
          svgString={svgString}
          handles={handles}
          sliders={sliders}
          setSliders={setSliders}
          patternType={patternType}
          loading={loading}
          validationError={validationError}
          t={t}
          lang={lang}
        />

      </div>
    </div>
  );
}
