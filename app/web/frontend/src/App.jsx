import React, { useState, useEffect, useRef } from 'react';
import Navbar from './components/Navbar';
import GarmentCatalog from './components/GarmentCatalog';
import CadStudio from './components/CadStudio';
import ProfileManager from './components/ProfileManager';
import GuideView from './components/GuideView';
import { TRANSLATIONS } from './translations';

const DEFAULT_HOSEN_INPUTS = {
  title: 'Nohavice 15. století',
  VP: 175,
  OP: 98,
  OS: 116,
  BDK: 122,
  KD: 90,
  O_st: 61,
  O_nk: 46,
  O_l: 40,
  O_kot: 26
};

const DEFAULT_HOSEN_SLIDERS = {
  slider1: 5,
  slider2: 12,
  slider3: 5,
  slider4: 12,
  slider5: 0,
  slider6: 0,
  slider7: 0
};

const DEFAULT_BODICE_INPUTS = {
  title: 'Kabátec 15. století',
  OH: 100,
  OP: 80,
  DZ: 40,
  Szad: 42
};

const DEFAULT_BODICE_SLIDERS = {
  slider1: 12
};

const HOSEN_SLIDER_CONFIGS = [
  { id: 'slider1', labelKey: 'slider_slider1_hosen', min: 0, max: 25, unit: 'cm' },
  { id: 'slider5', labelKey: 'slider_slider5_hosen', min: -15, max: 10, unit: 'cm' },
  { id: 'slider4', labelKey: 'slider_slider4_hosen', min: 0, max: 24, unit: 'cm' },
  { id: 'slider6', labelKey: 'slider_slider6_hosen', min: -10, max: 15, unit: 'cm' },
  { id: 'slider7', labelKey: 'slider_slider7_hosen', min: -10, max: 15, unit: 'cm' },
  { id: 'slider3', labelKey: 'slider_slider3_hosen', min: 0, max: 10, unit: 'cm' },
  { id: 'slider2', labelKey: 'slider_slider2_hosen', min: 0, max: 24, unit: 'cm' },
];

const BODICE_SLIDER_CONFIGS = [
  { id: 'slider1', labelKey: 'slider_slider1_bodice', min: 5, max: 30, unit: 'cm' }
];

const INPUT_CONFIGS = [
  { id: 'title', label: 'Název střihu', type: 'text', placeholder: 'Název střihu', unit: '' },
  { id: 'VP', label: 'Celková výška (VP)', type: 'number', placeholder: '175', unit: 'cm' },
  { id: 'OP', label: 'Obvod pasu (OP)', type: 'number', placeholder: '98', unit: 'cm' },
  { id: 'OS', label: 'Obvod sedu (OS)', type: 'number', placeholder: '116', unit: 'cm' },
  { id: 'BDK', label: 'Boční délka (BDK)', type: 'number', placeholder: '122', unit: 'cm' },
  { id: 'KD', label: 'Kroková délka (KD)', type: 'number', placeholder: '90', unit: 'cm' },
  { id: 'O_st', label: 'Obvod stehna (Ost)', type: 'number', placeholder: '61', unit: 'cm' },
  { id: 'O_nk', label: 'Obvod nad kolenem (Onk)', type: 'number', placeholder: '46', unit: 'cm' },
  { id: 'O_l', label: 'Obvod lýtka (Ol)', type: 'number', placeholder: '40', unit: 'cm' },
  { id: 'O_kot', label: 'Obvod kotníku (Ok)', type: 'number', placeholder: '26', unit: 'cm' },
  { id: 'OH', label: 'Obvod hrudníku (OH)', type: 'number', placeholder: '100', unit: 'cm' },
  { id: 'DZ', label: 'Délka zad (DZ)', type: 'number', placeholder: '40', unit: 'cm' },
  { id: 'Szad', label: 'Šířka zad (Szad)', type: 'number', placeholder: '42', unit: 'cm' },
];

export default function App() {
  // Navigation: 'catalog' | 'studio' | 'profiles' | 'guide'
  const [currentTab, setCurrentTab] = useState('studio');

  // Garment & Pattern selection
  const [patternType, setPatternType] = useState('hosen');
  const [part, setPart] = useState('all');
  const [inputs, setInputs] = useState(DEFAULT_HOSEN_INPUTS);
  const [sliders, setSliders] = useState(DEFAULT_HOSEN_SLIDERS);

  // Language & Theme
  const [lang, setLang] = useState(() => {
    const saved = localStorage.getItem('jppattern_lang');
    return (saved === 'EN' || saved === 'CZ') ? saved : 'CZ';
  });

  const [darkMode, setDarkMode] = useState(() => {
    try {
      const saved = localStorage.getItem('jppattern_dark');
      return saved !== null ? JSON.parse(saved) : true;
    } catch {
      return true;
    }
  });

  // Client Profiles (LocalStorage)
  const [profiles, setProfiles] = useState(() => {
    const defaultVal = { hosen: {}, bodice: {} };
    try {
      const saved = localStorage.getItem('jppattern_profiles_v2');
      if (saved) {
        const parsed = JSON.parse(saved);
        if (parsed && typeof parsed === 'object') {
          return {
            hosen: parsed.hosen || {},
            bodice: parsed.bodice || {}
          };
        }
      }
    } catch (e) {
      console.error('Profiles parse error', e);
    }
    return defaultVal;
  });

  const [activeProfile, setActiveProfile] = useState('');

  // Drafting State
  const [svgString, setSvgString] = useState('');
  const [loading, setLoading] = useState(false);
  const [exportingPdf, setExportingPdf] = useState(false);
  const [exportingPng, setExportingPng] = useState(false);
  const [exportingSvg, setExportingSvg] = useState(false);
  const [validationError, setValidationError] = useState('');

  const debounceTimer = useRef(null);
  const t = TRANSLATIONS[lang] || TRANSLATIONS.CZ;

  // Dark mode effect
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('jppattern_dark', JSON.stringify(darkMode));
  }, [darkMode]);

  // Language change effect
  useEffect(() => {
    localStorage.setItem('jppattern_lang', lang);
  }, [lang]);

  // Garment switch handler
  const handleGarmentSelect = (type) => {
    setPatternType(type);
    setValidationError('');
    setActiveProfile('');
    setPart('all');
    if (type === 'hosen') {
      setInputs(DEFAULT_HOSEN_INPUTS);
      setSliders(DEFAULT_HOSEN_SLIDERS);
    } else {
      setInputs(DEFAULT_BODICE_INPUTS);
      setSliders(DEFAULT_BODICE_SLIDERS);
    }
    setCurrentTab('studio');
  };

  // Debounced Drafting calculation
  useEffect(() => {
    if (debounceTimer.current) clearTimeout(debounceTimer.current);

    // Local input validation
    const invalidKey = Object.keys(inputs).find(
      k => k !== 'title' && (isNaN(parseFloat(inputs[k])) || parseFloat(inputs[k]) <= 0)
    );

    if (invalidKey) {
      const label = t[`input_${invalidKey}`] || invalidKey;
      setValidationError(`${t.validationErrorPrefix} "${label}" ${t.validationErrorPositive}`);
      return;
    }
    setValidationError('');

    debounceTimer.current = setTimeout(() => {
      generatePattern();
    }, 400);

    return () => clearTimeout(debounceTimer.current);
  }, [inputs, sliders, patternType, part]);

  const generatePattern = async () => {
    setLoading(true);
    try {
      const res = await fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sliders, inputs, patternType, part })
      });
      const data = await res.json();
      if (res.ok) {
        setSvgString(data.svg);
      } else {
        setValidationError(data.message || 'Drafting error.');
      }
    } catch {
      setValidationError('Server connection failed.');
    } finally {
      setLoading(false);
    }
  };

  // Export handlers
  const exportPDF = async () => {
    setExportingPdf(true);
    try {
      const res = await fetch('/export/pdf', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sliders, inputs, patternType, part })
      });
      if (!res.ok) throw new Error('Export failed');
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const safeTitle = (inputs.title || 'pattern').replace(/\s+/g, '_');
      a.download = `${safeTitle}_pattern.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      alert(lang === 'CZ' ? 'Chyba při exportu PDF.' : 'PDF Export failed.');
    } finally {
      setExportingPdf(false);
    }
  };

  const exportPNG = async () => {
    setExportingPng(true);
    try {
      const res = await fetch('/export/png', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sliders, inputs, patternType, part })
      });
      if (!res.ok) throw new Error('Export failed');
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const safeTitle = (inputs.title || 'pattern').replace(/\s+/g, '_');
      a.download = `${safeTitle}_pattern.png`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      alert(lang === 'CZ' ? 'Chyba při exportu PNG.' : 'PNG Export failed.');
    } finally {
      setExportingPng(false);
    }
  };

  const exportSVG = () => {
    if (!svgString) return;
    setExportingSvg(true);
    try {
      const blob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const safeTitle = (inputs.title || 'pattern').replace(/\s+/g, '_');
      a.download = `${safeTitle}_pattern.svg`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('SVG Export error', err);
      alert(lang === 'CZ' ? 'Chyba při exportu SVG.' : 'SVG Export failed.');
    } finally {
      setExportingSvg(false);
    }
  };

  const currentSliderConfigs = patternType === 'hosen' ? HOSEN_SLIDER_CONFIGS : BODICE_SLIDER_CONFIGS;
  const currentInputConfigs = INPUT_CONFIGS.filter(item => Object.keys(inputs).includes(item.id));

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 flex flex-col transition-colors duration-200">
      
      {/* Top Main Navigation Bar */}
      <Navbar
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        lang={lang}
        setLang={setLang}
        darkMode={darkMode}
        setDarkMode={setDarkMode}
        activeProfile={activeProfile}
        t={t}
      />

      {/* Main View Router */}
      <main className="flex-1 flex flex-col">
        {currentTab === 'catalog' && (
          <GarmentCatalog 
            onSelectGarment={handleGarmentSelect} 
            t={t} 
            lang={lang} 
          />
        )}

        {currentTab === 'studio' && (
          <CadStudio
            patternType={patternType}
            setPatternType={handleGarmentSelect}
            inputs={inputs}
            setInputs={setInputs}
            sliders={sliders}
            setSliders={setSliders}
            part={part}
            setPart={setPart}
            svgString={svgString}
            loading={loading}
            validationError={validationError}
            activeProfile={activeProfile}
            t={t}
            lang={lang}
            exportPDF={exportPDF}
            exportPNG={exportPNG}
            exportSVG={exportSVG}
            exportingPdf={exportingPdf}
            exportingPng={exportingPng}
            exportingSvg={exportingSvg}
            sliderConfigs={currentSliderConfigs}
            inputConfigs={currentInputConfigs}
          />
        )}

        {currentTab === 'profiles' && (
          <ProfileManager
            profiles={profiles}
            setProfiles={setProfiles}
            activeProfile={activeProfile}
            setActiveProfile={setActiveProfile}
            inputs={inputs}
            sliders={sliders}
            patternType={patternType}
            setInputs={setInputs}
            setSliders={setSliders}
            setPatternType={setPatternType}
            setCurrentTab={setCurrentTab}
            t={t}
            lang={lang}
          />
        )}

        {currentTab === 'guide' && (
          <GuideView 
            t={t} 
            lang={lang} 
          />
        )}
      </main>

    </div>
  );
}
