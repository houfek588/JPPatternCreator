import React, { useState, useRef, useEffect } from 'react';
import { ZoomIn, ZoomOut, Maximize2, RotateCcw, AlertTriangle, Loader2 } from 'lucide-react';

export default function CadCanvas({ 
  svgString, 
  loading, 
  validationError, 
  t 
}) {
  const [scale, setScale] = useState(1.0);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const containerRef = useRef(null);

  // Handle Mouse Wheel Zooming
  const handleWheel = (e) => {
    e.preventDefault();
    const zoomFactor = e.deltaY < 0 ? 1.15 : 0.85;
    setScale((prevScale) => {
      const nextScale = prevScale * zoomFactor;
      return Math.min(Math.max(nextScale, 0.25), 4.5);
    });
  };

  // Mouse drag / panning handlers
  const handleMouseDown = (e) => {
    // Only drag with left mouse or middle mouse button
    if (e.button === 0 || e.button === 1) {
      setIsDragging(true);
      setDragStart({
        x: e.clientX - position.x,
        y: e.clientY - position.y
      });
    }
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    setPosition({
      x: e.clientX - dragStart.x,
      y: e.clientY - dragStart.y
    });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  // Reset view to center 100%
  const resetView = () => {
    setScale(1.0);
    setPosition({ x: 0, y: 0 });
  };

  const fitView = () => {
    setScale(0.8);
    setPosition({ x: 0, y: 0 });
  };

  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    el.addEventListener('wheel', handleWheel, { passive: false });
    return () => el.removeEventListener('wheel', handleWheel);
  }, []);

  return (
    <div 
      ref={containerRef}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      className={`flex-1 relative w-full h-full min-h-[500px] overflow-hidden bg-slate-100 dark:bg-slate-950/80 border-t md:border-t-0 md:border-l border-slate-200 dark:border-slate-800 flex items-center justify-center select-none cursor-${isDragging ? 'grabbing' : 'grab'} cad-grid transition-colors`}
    >
      {/* Floating Floating CAD Controls Overlay */}
      <div className="absolute bottom-6 left-6 z-20 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border border-slate-200 dark:border-slate-800 rounded-2xl p-1.5 shadow-lg flex items-center gap-1">
        <button
          onClick={() => setScale(s => Math.max(0.25, s - 0.2))}
          title={t.zoomOut}
          className="p-2 text-slate-600 dark:text-slate-300 hover:text-brand hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl transition-all"
        >
          <ZoomOut className="h-4 w-4" />
        </button>
        <span className="text-xs font-extrabold text-slate-700 dark:text-slate-200 px-2 min-w-14 text-center font-mono">
          {Math.round(scale * 100)}%
        </span>
        <button
          onClick={() => setScale(s => Math.min(4.5, s + 0.2))}
          title={t.zoomIn}
          className="p-2 text-slate-600 dark:text-slate-300 hover:text-brand hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl transition-all"
        >
          <ZoomIn className="h-4 w-4" />
        </button>
        <div className="h-4 w-[1px] bg-slate-200 dark:border-slate-700 mx-1" />
        <button
          onClick={resetView}
          title={t.zoom100}
          className="p-2 text-slate-600 dark:text-slate-300 hover:text-brand hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl transition-all text-[11px] font-bold"
        >
          1:1
        </button>
        <button
          onClick={fitView}
          title={t.zoomReset}
          className="p-2 text-slate-600 dark:text-slate-300 hover:text-brand hover:bg-slate-100 dark:hover:bg-slate-800 rounded-xl transition-all"
        >
          <Maximize2 className="h-4 w-4" />
        </button>
      </div>

      {/* 10 x 10 cm CAD Calibration Reference Box Badge */}
      <div className="absolute top-6 right-6 z-20 bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border border-slate-200 dark:border-slate-800 rounded-xl px-3 py-2 shadow-sm pointer-events-none hidden sm:flex items-center gap-2.5">
        <div className="w-5 h-5 border-2 border-brand dark:border-brand-light border-dashed rounded-xs flex items-center justify-center text-[7px] font-black text-brand">
          10
        </div>
        <div className="text-[10px] leading-tight font-medium text-slate-500 dark:text-slate-400">
          <span className="font-bold text-slate-800 dark:text-slate-200 block">CAD Reference 1:1</span>
          Kontrolní čtverec 10 × 10 cm
        </div>
      </div>

      {/* Validation Error Screen */}
      {validationError ? (
        <div className="max-w-md bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900/60 rounded-3xl p-6 text-center shadow-xl z-10 m-4">
          <AlertTriangle className="h-10 w-10 text-red-500 mx-auto mb-3" />
          <h3 className="text-red-700 dark:text-red-400 font-extrabold text-sm mb-1">
            Chyba v zadání tělesných rozměrů
          </h3>
          <p className="text-xs text-red-600 dark:text-red-300 leading-relaxed font-medium">
            {validationError}
          </p>
        </div>
      ) : svgString ? (
        /* Pattern Drawing Canvas Container */
        <div 
          style={{
            transform: `translate(${position.x}px, ${position.y}px) scale(${scale})`,
            transformOrigin: 'center center',
            transition: isDragging ? 'none' : 'transform 0.15s ease-out'
          }}
          className="shadow-2xl rounded-2xl bg-white border border-slate-200 dark:border-slate-800 p-6 relative max-w-full max-h-full flex items-center justify-center select-none"
        >
          <div 
            dangerouslySetInnerHTML={{ __html: svgString }} 
            className="w-auto h-auto flex items-center justify-center"
          />
        </div>
      ) : (
        /* Loading / Waiting Placeholder */
        <div className="text-center space-y-3 p-8 z-10">
          <Loader2 className="h-10 w-10 text-brand dark:text-brand-light animate-spin mx-auto opacity-70" />
          <p className="text-xs text-slate-500 dark:text-slate-400 font-semibold tracking-wide">
            {t.waiting}
          </p>
        </div>
      )}
    </div>
  );
}
