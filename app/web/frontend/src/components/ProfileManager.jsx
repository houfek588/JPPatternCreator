import React, { useState, useRef } from 'react';
import { 
  Users, Download, Upload, Trash2, ArrowRight, 
  PlusCircle, UserCheck, ShieldCheck, FileJson 
} from 'lucide-react';

export default function ProfileManager({ 
  profiles, 
  setProfiles, 
  activeProfile, 
  setActiveProfile, 
  inputs, 
  sliders, 
  patternType, 
  setInputs, 
  setSliders, 
  setPatternType, 
  setCurrentTab, 
  t, 
  lang 
}) {
  const [newProfileName, setNewProfileName] = useState('');
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  // Save current studio inputs as a new profile
  const handleSaveProfile = () => {
    const name = newProfileName.trim() || inputs.title || (lang === 'CZ' ? 'Nový profil' : 'New Profile');
    const updated = {
      ...profiles,
      [patternType]: {
        ...(profiles[patternType] || {}),
        [name]: { inputs, sliders }
      }
    };
    setProfiles(updated);
    localStorage.setItem('jppattern_profiles_v2', JSON.stringify(updated));
    setActiveProfile(name);
    setNewProfileName('');
  };

  // Load selected profile into CAD Studio
  const handleLoadProfile = (type, name) => {
    const profileData = profiles[type]?.[name];
    if (profileData) {
      setPatternType(type);
      setInputs(profileData.inputs);
      setSliders(profileData.sliders);
      setActiveProfile(name);
      setCurrentTab('studio');
    }
  };

  // Delete profile
  const handleDeleteProfile = (type, name) => {
    if (!window.confirm(t.confirmDelete)) return;
    const updated = { ...profiles };
    if (updated[type]) {
      delete updated[type][name];
      setProfiles(updated);
      localStorage.setItem('jppattern_profiles_v2', JSON.stringify(updated));
      if (activeProfile === name) setActiveProfile('');
    }
  };

  // Export all profiles as a single backup JSON
  const exportAllProfiles = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(profiles, null, 2));
    const a = document.createElement('a');
    a.href = dataStr;
    a.download = `jppattern_atelier_backup_${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
  };

  // Process JSON file from upload or drag & drop
  const handleFileDrop = (file) => {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const parsed = JSON.parse(e.target.result);
        if (parsed && typeof parsed === 'object') {
          // Merge imported profiles with existing
          const merged = {
            hosen: { ...(profiles.hosen || {}), ...(parsed.hosen || {}) },
            bodice: { ...(profiles.bodice || {}), ...(parsed.bodice || {}) }
          };
          setProfiles(merged);
          localStorage.setItem('jppattern_profiles_v2', JSON.stringify(merged));
          alert(lang === 'CZ' ? 'Profily byly úspěšně importovány!' : 'Profiles imported successfully!');
        }
      } catch (err) {
        alert(lang === 'CZ' ? 'Chyba: Neplatný formát JSON souboru.' : 'Error: Invalid JSON profile format.');
      }
    };
    reader.readAsText(file);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-8">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pb-6 border-b border-slate-200 dark:border-slate-800">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white flex items-center gap-3">
            <Users className="h-7 w-7 text-brand dark:text-brand-light" />
            <span>{t.profilesTitle}</span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1 font-medium">
            {t.profilesSubtitle}
          </p>
        </div>

        {/* Global Action Buttons */}
        <div className="flex items-center gap-2.5">
          <button
            onClick={exportAllProfiles}
            className="px-4 py-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 text-xs font-bold transition-all flex items-center gap-2 border border-slate-300 dark:border-slate-700/60"
          >
            <Download className="h-4 w-4" />
            <span>{t.btnExportAll}</span>
          </button>

          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={(e) => handleFileDrop(e.target.files[0])} 
            accept=".json" 
            className="hidden" 
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            className="px-4 py-2.5 rounded-xl bg-brand hover:bg-brand-hover text-white text-xs font-bold transition-all flex items-center gap-2 shadow-md"
          >
            <Upload className="h-4 w-4" />
            <span>{t.btnImportJson}</span>
          </button>
        </div>
      </div>

      {/* Quick Save Card & Drag & Drop Zone */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Save Current Studio Measurement */}
        <div className="lg:col-span-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm">
          <h2 className="text-sm font-extrabold text-slate-900 dark:text-white mb-2 flex items-center gap-2">
            <PlusCircle className="h-4 w-4 text-brand dark:text-brand-light" />
            <span>{t.newProfileTitle}</span>
          </h2>
          <p className="text-xs text-slate-500 dark:text-slate-400 mb-4 font-medium">
            Uloží právě nastavené tělesné rozměry ze studia ({patternType === 'hosen' ? t.garmentHosenTitle : t.garmentBodiceTitle}) pod zadaným jménem zákazníka.
          </p>

          <div className="flex gap-2.5">
            <input
              type="text"
              placeholder={t.profileNamePlaceholder}
              value={newProfileName}
              onChange={(e) => setNewProfileName(e.target.value)}
              className="glass-input flex-1 text-xs py-2.5 bg-slate-50 dark:bg-slate-950/60 text-slate-900 dark:text-slate-100"
            />
            <button
              onClick={handleSaveProfile}
              className="px-5 py-2.5 rounded-xl bg-brand hover:bg-brand-hover text-white text-xs font-bold shadow-md transition-all cursor-pointer shrink-0"
            >
              {t.btnSaveProfile}
            </button>
          </div>
        </div>

        {/* Drag & Drop Zone */}
        <div 
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={(e) => {
            e.preventDefault();
            setDragOver(false);
            if (e.dataTransfer.files?.[0]) handleFileDrop(e.dataTransfer.files[0]);
          }}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-3xl p-6 flex flex-col items-center justify-center text-center cursor-pointer transition-all ${
            dragOver 
              ? 'border-brand bg-brand/10' 
              : 'border-slate-300 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-950/30 hover:border-brand/50'
          }`}
        >
          <FileJson className="h-8 w-8 text-slate-400 mb-2" />
          <p className="text-xs font-bold text-slate-700 dark:text-slate-300">
            {t.dropzoneTitle}
          </p>
          <span className="text-[10px] text-slate-400 mt-1">.JSON zálohy</span>
        </div>

      </div>

      {/* Customer List Database */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl p-6 shadow-sm space-y-6">
        <h2 className="text-base font-black text-slate-900 dark:text-white flex items-center gap-2">
          <span>{t.clientListTitle}</span>
        </h2>

        {/* Both Types Listing */}
        {['hosen', 'bodice'].map((type) => {
          const typeProfiles = profiles[type] || {};
          const names = Object.keys(typeProfiles);

          return (
            <div key={type} className="space-y-3">
              <div className="text-xs font-black uppercase tracking-wider text-slate-400 flex items-center justify-between pb-1 border-b border-slate-100 dark:border-slate-800">
                <span>{type === 'hosen' ? t.garmentHosenTitle : t.garmentBodiceTitle} ({names.length})</span>
              </div>

              {names.length === 0 ? (
                <div className="text-xs text-slate-400 italic py-2">
                  Žádné profily pro tento oděv.
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  {names.map((name) => {
                    const data = typeProfiles[name];
                    const isCurrent = activeProfile === name && patternType === type;

                    return (
                      <div 
                        key={name}
                        className={`p-4 rounded-2xl border transition-all flex flex-col justify-between ${
                          isCurrent 
                            ? 'border-brand bg-brand/5 shadow-xs' 
                            : 'border-slate-200 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-950/40 hover:border-slate-300'
                        }`}
                      >
                        <div>
                          <div className="flex items-center justify-between mb-2">
                            <span className="font-extrabold text-xs text-slate-900 dark:text-white truncate">
                              {name}
                            </span>
                            {isCurrent && (
                              <span className="text-[9px] font-black uppercase px-2 py-0.5 rounded bg-brand text-white">
                                Aktivní
                              </span>
                            )}
                          </div>

                          {/* Quick Specs Snippet */}
                          <div className="text-[10px] text-slate-500 font-mono space-x-2 mb-4">
                            {type === 'hosen' ? (
                              <>
                                <span>VP: {data.inputs?.VP || '-'}</span>
                                <span>OP: {data.inputs?.OP || '-'}</span>
                                <span>OS: {data.inputs?.OS || '-'}</span>
                              </>
                            ) : (
                              <>
                                <span>OH: {data.inputs?.OH || '-'}</span>
                                <span>OP: {data.inputs?.OP || '-'}</span>
                                <span>DZ: {data.inputs?.DZ || '-'}</span>
                              </>
                            )}
                          </div>
                        </div>

                        <div className="flex items-center justify-between pt-2 border-t border-slate-100 dark:border-slate-800/80">
                          <button
                            onClick={() => handleLoadProfile(type, name)}
                            className="text-xs font-bold text-brand dark:text-brand-light hover:underline flex items-center gap-1 cursor-pointer"
                          >
                            <span>{t.btnLoadInStudio}</span>
                            <ArrowRight className="h-3.5 w-3.5" />
                          </button>
                          
                          <button
                            onClick={() => handleDeleteProfile(type, name)}
                            className="p-1.5 text-slate-400 hover:text-red-500 transition-colors cursor-pointer"
                            title={t.btnDeleteProfile}
                          >
                            <Trash2 className="h-3.5 w-3.5" />
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}

      </div>

    </div>
  );
}
