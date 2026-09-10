import React, { useState, useRef, useEffect, useCallback } from 'react';
import { 
  ZoomIn, ZoomOut, Maximize2, AlertTriangle, Loader2, 
  Crosshair, RotateCcw, X
} from 'lucide-react';

export default function CadCanvas({ 
  svgString, 
  handles = [],
  sliders = {},
  setSliders,
  patternType = 'hosen',
  loading, 
  validationError, 
  t,
  lang = 'CZ'
}) {
  const [scale, setScale] = useState(1.0);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  
  // CAD Smart Handles state
  const [showHandles, setShowHandles] = useState(true);
  const [activeDrag, setActiveDrag] = useState(null);
  const [hoveredHandleId, setHoveredHandleId] = useState(null);
  const [selectedHandleId, setSelectedHandleId] = useState(null);

  const getHandleAngle = useCallback((h) => {
    if (!h) return 0;
    if (h.angle !== undefined) return h.angle;
    return (h.direction === 'vertical' || h.direction === 'vertical_invert') ? 90 : 0;
  }, []);

  const handleDirectValueChange = (handleId, rawVal, min, max) => {
    if (!setSliders) return;
    const num = parseFloat(rawVal);
    if (!isNaN(num)) {
      const clamped = Math.min(Math.max(num, min), max);
      setSliders(prev => ({ ...prev, [handleId]: clamped }));
    }
  };

  const stepHandleValue = (handleId, delta, min, max, step = 0.5) => {
    if (!setSliders) return;
    setSliders(prev => {
      const cur = prev[handleId] ?? 0;
      const next = Math.min(Math.max(Math.round((cur + delta) / step) * step, min), max);
      return { ...prev, [handleId]: next };
    });
  };

  const resetHandleToDefault = (handle) => {
    if (!setSliders || !handle) return;
    const defaultMap = {
      slider1: patternType === 'bodice' ? 12 : 5,
      slider2: 12,
      slider3: 5,
      slider4: 12,
      slider5: 0,
      slider6: 0,
      slider7: 0
    };
    const def = defaultMap[handle.id] ?? handle.min ?? 0;
    setSliders(prev => ({ ...prev, [handle.id]: def }));
  };

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

  // Canvas pan / drag handlers
  const handleMouseDown = (e) => {
    // Only drag with left mouse or middle mouse button if not clicking a handle
    if ((e.button === 0 || e.button === 1) && !activeDrag) {
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

  // Window-level mouse listeners for smooth 60 FPS handle dragging
  useEffect(() => {
    if (!activeDrag) return;

    const onWindowMouseMove = (e) => {
      const dx = e.clientX - activeDrag.mouseX;
      const dy = e.clientY - activeDrag.mouseY;

      // Adjust for canvas scale
      const svgDx = dx / scale;
      const svgDy = dy / scale;

      // In SVG coordinates, SVG_SCALE = 4 px per cm
      const cmDx = svgDx / 4;
      const cmDy = svgDy / 4;

      const h = activeDrag.handle;
      const angle = getHandleAngle(h);
      const rad = (angle * Math.PI) / 180;
      const ux = Math.cos(rad);
      const uy = Math.sin(rad);

      // Project movement vector onto angle vector
      let delta = cmDx * ux + cmDy * uy;

      if (h.id === 'slider2') {
        delta *= 2;
      } else if (h.id === 'slider5' || h.id === 'slider6' || h.invert) {
        delta = -delta;
      }

      let newVal = activeDrag.initialVal + delta;
      newVal = Math.min(Math.max(newVal, h.min), h.max);
      
      const step = h.step || 0.5;
      newVal = Math.round(newVal / step) * step;

      if (setSliders) {
        setSliders(prev => {
          if (prev[h.id] === newVal) return prev;
          return { ...prev, [h.id]: newVal };
        });
      }
    };

    const onWindowMouseUp = () => {
      setActiveDrag(null);
    };

    window.addEventListener('mousemove', onWindowMouseMove);
    window.addEventListener('mouseup', onWindowMouseUp);

    return () => {
      window.removeEventListener('mousemove', onWindowMouseMove);
      window.removeEventListener('mouseup', onWindowMouseUp);
    };
  }, [activeDrag, scale, setSliders, getHandleAngle]);

  // Handle Drag Start
  const handleHandleMouseDown = (e, handle) => {
    e.stopPropagation();
    e.preventDefault();
    setSelectedHandleId(handle.id);
    const currentVal = sliders[handle.id] ?? handle.value;
    setActiveDrag({
      id: handle.id,
      mouseX: e.clientX,
      mouseY: e.clientY,
      initialVal: currentVal,
      handle
    });
  };

  // Handle Reset on Double Click
  const handleHandleDoubleClick = (e, handle) => {
    e.stopPropagation();
    const defaultMap = {
      slider1: patternType === 'bodice' ? 12 : 5,
      slider2: 12,
      slider3: 5,
      slider4: 12,
      slider5: 0,
      slider6: 0,
      slider7: 0
    };
    const def = defaultMap[handle.id] ?? handle.min;
    if (setSliders) {
      setSliders(prev => ({ ...prev, [handle.id]: def }));
    }
  };

  // Active, Selected or Hovered handle description
  const currentInspectHandle = activeDrag?.handle || handles.find(h => h.id === selectedHandleId || h.id === hoveredHandleId);

  return (
    <div 
      ref={containerRef}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseUp}
      className={`flex-1 relative w-full h-full min-h-[500px] overflow-hidden bg-slate-100 dark:bg-slate-950/80 border-t md:border-t-0 md:border-l border-slate-200 dark:border-slate-800 flex items-center justify-center select-none cursor-${isDragging ? 'grabbing' : activeDrag ? 'crosshair' : 'grab'} cad-grid transition-colors`}
    >
      {/* Top Left: Active / Selected Handle Live Inspector Pill with Direct Value Controls */}
      {currentInspectHandle && (
        <div 
          onMouseDown={(e) => e.stopPropagation()}
          className="absolute top-6 left-6 z-30 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-xl w-72 sm:w-80 flex flex-col gap-3 animate-in fade-in slide-in-from-top-2 duration-150"
        >
          {/* Header with Title, Description and Close Button */}
          <div className="flex items-start justify-between gap-2">
            <div className="flex items-center gap-2.5 min-w-0">
              <div 
                className="w-3.5 h-3.5 rounded-full ring-4 ring-opacity-30 shrink-0"
                style={{ 
                  backgroundColor: currentInspectHandle.color || '#e11d48',
                  boxShadow: `0 0 10px ${currentInspectHandle.color || '#e11d48'}`
                }} 
              />
              <div className="min-w-0">
                <span className="text-xs font-extrabold text-slate-800 dark:text-slate-100 block truncate">
                  {lang === 'CZ' ? (currentInspectHandle.name_cz || currentInspectHandle.title_cz) : (currentInspectHandle.name_en || currentInspectHandle.title_en)}
                </span>
                <span className="text-[10px] text-slate-500 dark:text-slate-400 block truncate">
                  {lang === 'CZ' ? currentInspectHandle.description_cz : currentInspectHandle.description_en}
                </span>
              </div>
            </div>

            {selectedHandleId === currentInspectHandle.id && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setSelectedHandleId(null);
                }}
                className="text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 p-1 rounded-md transition-colors shrink-0"
                title="Zavřít panel táhla"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          {/* Direct Value Input & Quick Step Row */}
          <div className="pt-2 border-t border-slate-100 dark:border-slate-800/80 flex flex-col gap-2.5">
            <div className="flex items-center justify-between gap-2">
              <span className="text-[11px] font-bold text-slate-600 dark:text-slate-300">
                {t.handleValue || 'Hodnota táhla'}:
              </span>

              {/* Direct numeric input with unit & reset button */}
              <div className="flex items-center gap-1.5">
                <div className="relative flex items-center">
                  <input
                    type="number"
                    min={currentInspectHandle.min}
                    max={currentInspectHandle.max}
                    step={currentInspectHandle.step || 0.5}
                    value={sliders[currentInspectHandle.id] ?? currentInspectHandle.value}
                    onChange={(e) => handleDirectValueChange(
                      currentInspectHandle.id, 
                      e.target.value, 
                      currentInspectHandle.min, 
                      currentInspectHandle.max,
                      currentInspectHandle.step || 0.5
                    )}
                    className="w-20 text-xs font-black font-mono px-2 py-1 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-900 dark:text-slate-100 text-right focus:outline-none focus:ring-2 focus:ring-brand"
                  />
                  <span className="text-[10px] font-bold text-slate-400 dark:text-slate-500 ml-1.5">
                    {currentInspectHandle.unit}
                  </span>
                </div>

                <button
                  onClick={() => resetHandleToDefault(currentInspectHandle)}
                  title={t.defaultValue || 'Obnovit výchozí hodnotu'}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-brand hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            {/* Range Slider for Live Dragging */}
            <div className="space-y-1">
              <input
                type="range"
                min={currentInspectHandle.min}
                max={currentInspectHandle.max}
                step={currentInspectHandle.step || 0.5}
                value={sliders[currentInspectHandle.id] ?? currentInspectHandle.value}
                onChange={(e) => {
                  const val = parseFloat(e.target.value);
                  if (setSliders) {
                    setSliders(prev => ({ ...prev, [currentInspectHandle.id]: val }));
                  }
                }}
                className="w-full h-2 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-brand"
              />
              <div className="flex items-center justify-between text-[9px] font-mono text-slate-400 dark:text-slate-500 px-0.5">
                <span>{currentInspectHandle.min} {currentInspectHandle.unit}</span>
                <span>{currentInspectHandle.max} {currentInspectHandle.unit}</span>
              </div>
            </div>

            {/* Quick Step Adjustment Buttons */}
            <div className="flex items-center justify-between gap-1 pt-0.5">
              <div className="flex items-center gap-1">
                <button
                  onClick={() => stepHandleValue(currentInspectHandle.id, -1.0, currentInspectHandle.min, currentInspectHandle.max, currentInspectHandle.step)}
                  className="px-2 py-1 text-[10px] font-bold font-mono rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition-colors"
                  title="-1 cm"
                >
                  -1 cm
                </button>
                <button
                  onClick={() => stepHandleValue(currentInspectHandle.id, -0.5, currentInspectHandle.min, currentInspectHandle.max, currentInspectHandle.step)}
                  className="px-2 py-1 text-[10px] font-bold font-mono rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition-colors"
                  title="-0.5 cm"
                >
                  -0.5
                </button>
              </div>

              <div className="flex items-center gap-1">
                <button
                  onClick={() => stepHandleValue(currentInspectHandle.id, 0.5, currentInspectHandle.min, currentInspectHandle.max, currentInspectHandle.step)}
                  className="px-2 py-1 text-[10px] font-bold font-mono rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition-colors"
                  title="+0.5 cm"
                >
                  +0.5
                </button>
                <button
                  onClick={() => stepHandleValue(currentInspectHandle.id, 1.0, currentInspectHandle.min, currentInspectHandle.max, currentInspectHandle.step)}
                  className="px-2 py-1 text-[10px] font-bold font-mono rounded-lg bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition-colors"
                  title="+1 cm"
                >
                  +1 cm
                </button>
              </div>
            </div>

            {/* Footer info: orientation angle & reset hint */}
            <div className="text-[9px] text-slate-400 dark:text-slate-500 pt-1 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between">
              <span className="opacity-80 font-mono">📐 {Math.round(getHandleAngle(currentInspectHandle))}°</span>
              <span className="opacity-75">{t.resetHandle}</span>
            </div>
          </div>
        </div>
      )}

      {/* Floating CAD Viewport Toolbar */}
      <div className="absolute bottom-6 left-6 z-20 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border border-slate-200 dark:border-slate-800 rounded-2xl p-1.5 shadow-lg flex items-center gap-1">
        {/* Toggle Smart Handles Button */}
        <button
          onClick={() => setShowHandles(prev => !prev)}
          title={t.cadHandlesToggle}
          className={`px-2.5 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
            showHandles 
              ? 'bg-brand/10 text-brand dark:text-brand-light border border-brand/20 shadow-xs' 
              : 'text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
          }`}
        >
          <Crosshair className={`h-3.5 w-3.5 ${showHandles ? 'animate-pulse' : ''}`} />
          <span className="hidden sm:inline">{t.cadHandlesToggle}</span>
          <span className={`w-1.5 h-1.5 rounded-full ${showHandles ? 'bg-emerald-500 ring-2 ring-emerald-400/40' : 'bg-slate-300 dark:bg-slate-700'}`} />
        </button>

        <div className="h-4 w-[1px] bg-slate-200 dark:bg-slate-800 mx-1" />

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

        <div className="h-4 w-[1px] bg-slate-200 dark:bg-slate-800 mx-1" />

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

      {/* 10 x 10 cm CAD Calibration Reference Box */}
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
            transition: (isDragging || activeDrag) ? 'none' : 'transform 0.15s ease-out'
          }}
          className="shadow-2xl rounded-2xl bg-white border border-slate-200 dark:border-slate-800 p-6 relative max-w-full max-h-full flex items-center justify-center select-none"
        >
          {/* Exact Pattern Bounds Container (480 x 640 SVG space) */}
          <div className="relative w-[480px] h-[640px] flex items-center justify-center overflow-visible">
            {/* SVG Render Layer */}
            <div 
              dangerouslySetInnerHTML={{ __html: svgString }} 
              className="w-full h-full flex items-center justify-center pointer-events-none"
            />

            {/* Smart Handles Overlay */}
            {showHandles && handles && handles.length > 0 && (
              <div className="absolute inset-0 w-[480px] h-[640px] pointer-events-none overflow-visible">
                
                {/* SVG Visual Guidelines Layer */}
                <svg className="absolute inset-0 w-[480px] h-[640px] overflow-visible pointer-events-none">
                  {handles.map(h => {
                    const isSelected = selectedHandleId === h.id;
                    const isActive = activeDrag?.id === h.id || hoveredHandleId === h.id || isSelected;
                    const color = h.color || '#e11d48';
                    const angle = getHandleAngle(h);
                    const rad = (angle * Math.PI) / 180;
                    const len = isActive ? 45 : 28;
                    const dx = Math.cos(rad) * len;
                    const dy = Math.sin(rad) * len;

                    return (
                      <g key={`guide-${h.id}`} opacity={isActive ? 0.95 : 0.4}>
                        <line
                          x1={h.x - dx}
                          y1={h.y - dy}
                          x2={h.x + dx}
                          y2={h.y + dy}
                          stroke={color}
                          strokeWidth={isActive ? 2 : 1.5}
                          strokeDasharray={isActive ? "4,3" : "3,3"}
                        />
                        {isActive && (
                          <circle
                            cx={h.x}
                            cy={h.y}
                            r={len}
                            fill="none"
                            stroke={color}
                            strokeWidth="0.75"
                            strokeDasharray="2,4"
                            opacity="0.35"
                          />
                        )}
                      </g>
                    );
                  })}
                </svg>

                {/* Interactive CAD Handle Knobs & Floating Badges */}
                {handles.map(h => {
                  const currentVal = sliders[h.id] ?? h.value;
                  const isSelected = selectedHandleId === h.id;
                  const isActive = activeDrag?.id === h.id;
                  const isHovered = hoveredHandleId === h.id;
                  const isHighlighted = isActive || isHovered || isSelected;
                  const color = h.color || '#e11d48';
                  const title = lang === 'CZ' ? (h.name_cz || h.title_cz) : (h.name_en || h.title_en);
                  const angle = getHandleAngle(h);

                  // Dynamic cursor based on angle
                  const rad = (angle * Math.PI) / 180;
                  const absSin = Math.abs(Math.sin(rad));
                  const absCos = Math.abs(Math.cos(rad));
                  const cursorClass = absSin > 0.8
                    ? 'cursor-ns-resize'
                    : absCos > 0.8
                    ? 'cursor-ew-resize'
                    : 'cursor-move';

                  return (
                    <div
                      key={h.id}
                      style={{
                        left: `${h.x}px`,
                        top: `${h.y}px`,
                        zIndex: isActive ? 40 : isSelected ? 35 : isHovered ? 30 : 20
                      }}
                      className="absolute -translate-x-1/2 -translate-y-1/2 pointer-events-auto flex items-center justify-center"
                      onMouseEnter={() => setHoveredHandleId(h.id)}
                      onMouseLeave={() => setHoveredHandleId(null)}
                      onMouseDown={(e) => handleHandleMouseDown(e, h)}
                      onDoubleClick={(e) => handleHandleDoubleClick(e, h)}
                    >
                      {/* Outer target pulse ring */}
                      <div 
                        className={`absolute -inset-2.5 rounded-full transition-all pointer-events-none ${
                          isActive 
                            ? 'scale-125 opacity-100' 
                            : isHighlighted 
                            ? 'scale-110 opacity-75' 
                            : 'scale-90 opacity-0 group-hover:opacity-60'
                        }`}
                        style={{
                          backgroundColor: `${color}25`,
                          border: `1.5px dashed ${color}`
                        }}
                      />

                      {/* Center Grip Knob */}
                      <div 
                        className={`w-6 h-6 rounded-full flex items-center justify-center shadow-lg transition-transform ${cursorClass} ${
                          isActive ? 'scale-125 shadow-2xl' : isHighlighted ? 'scale-110' : 'hover:scale-105'
                        }`}
                        style={{
                          backgroundColor: color,
                          border: isSelected ? '2.5px solid #38bdf8' : '2.5px solid white',
                          boxShadow: `0 2px 10px ${color}80`
                        }}
                      >
                        {/* Center White Target Dot */}
                        <div className="w-1.5 h-1.5 rounded-full bg-white shadow-xs" />
                      </div>

                      {/* Directional Indicator Cues (Arrows rotated by handle angle) */}
                      <div 
                        className="absolute pointer-events-none flex items-center justify-between w-9 text-[9px] font-black text-slate-800 dark:text-slate-100 transition-transform duration-75 select-none"
                        style={{ transform: `rotate(${angle}deg)` }}
                      >
                        <span className="-ml-3.5 leading-none opacity-85 select-none drop-shadow-xs">◀</span>
                        <span className="-mr-3.5 leading-none opacity-85 select-none drop-shadow-xs">▶</span>
                      </div>

                      {/* Attached Live Measurement Badge Pill */}
                      <div
                        className={`absolute whitespace-nowrap px-2 py-0.5 rounded-lg text-[10px] font-extrabold flex items-center gap-1.5 shadow-md backdrop-blur-md border transition-all pointer-events-none ${
                          isActive 
                            ? 'scale-110 z-50 bg-slate-900 text-white border-white/60 shadow-xl' 
                            : 'bg-white/95 dark:bg-slate-900/95 text-slate-800 dark:text-slate-100 border-slate-200 dark:border-slate-800'
                        } ${
                          h.id === 'slider3'
                            ? 'top-5' // below toe
                            : h.id === 'slider1'
                            ? '-top-7' // above waist
                            : h.id === 'slider6'
                            ? '-top-7' // above left thigh
                            : h.id === 'slider5'
                            ? '-left-24' // left of hip divide
                            : 'left-5' // to the right of instep, crotch, collar, right inseam
                        }`}
                        style={{
                          borderColor: isHighlighted ? color : undefined
                        }}
                      >
                        <span className="text-[9px] opacity-75 uppercase tracking-wide">
                          {title}
                        </span>
                        <span 
                          className="font-mono font-black"
                          style={{ color: isActive ? '#38bdf8' : color }}
                        >
                          {currentVal} {h.unit}
                        </span>
                      </div>
                    </div>
                  );
                })}

              </div>
            )}
          </div>
        </div>
      ) : loading ? (
        /* Loading Placeholder */
        <div className="text-center space-y-3 p-8 z-10">
          <Loader2 className="h-10 w-10 text-brand dark:text-brand-light animate-spin mx-auto opacity-70" />
          <p className="text-xs text-slate-500 dark:text-slate-400 font-semibold tracking-wide">
            {t.drafting}
          </p>
        </div>
      ) : (
        /* Waiting Placeholder */
        <div className="text-center space-y-3 p-8 z-10">
          <p className="text-xs text-slate-500 dark:text-slate-400 font-semibold tracking-wide">
            {t.waiting}
          </p>
        </div>
      )}
    </div>
  );
}
