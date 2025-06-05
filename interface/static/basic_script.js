function getValues() {
            const sliders = {
                slider1: document.getElementById('slider1').value,
                slider2: document.getElementById('slider2').value,
                slider3: document.getElementById('slider3').value,
                slider4: document.getElementById('slider4').value
            };
            const inputs = {};
            ['vp','oh','op','os','dz','db','bdk','kd','ost','onk','ul','ok'].forEach(id => {
                inputs[id] = document.getElementById(id).value;
            });
            return { sliders, inputs };
        }

function generate() {
        const values = getValues();
            fetch('/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(values)
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('view').innerHTML = data.svg;
                const [a, b, c, d] = data.scaled;
                document.getElementById('slider1_val').textContent = a.toFixed(2);
                document.getElementById('slider2_val').textContent = b.toFixed(2);
                document.getElementById('slider3_val').textContent = c.toFixed(2);
                document.getElementById('slider4_val').textContent = d.toFixed(2);
            });
        }

//            fetch('/generate', {
//                method: 'POST',
//                headers: { 'Content-Type': 'application/json' },
//                body: JSON.stringify(getValues())
//            })
//            .then(res => res.json())
//            .then(data => {
//                document.getElementById('view').innerHTML = data.svg;
//            });
//        }

//        ['slider1','slider2','slider3','slider4'].forEach(id => {
//            document.getElementById(id).addEventListener('input', generate);
//        });


function exportPDF() {
            const { sliders, inputs } = getValues();
            const svg = document.getElementById('view').innerHTML;
            fetch('/export/pdf', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ svg, sliders, inputs })
            })
            .then(res => res.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'pattern.pdf';
                a.click();
                URL.revokeObjectURL(url);
            });
        }



function exportPNG() {
            const svg = document.getElementById('view').innerHTML;
            fetch('/export/png', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ svg })
            })
            .then(res => res.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'pattern.png';
                a.click();
                URL.revokeObjectURL(url);
            });
        }

function saveInputs() {
            const values = getValues();
            fetch('/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(values)
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === "ok") alert("Data saved.");
                else alert("Error: " + data.message);
            });
        }

function updateSliderDisplays() {
    ['slider1','slider2','slider3','slider4'].forEach(id => {
        document.getElementById(`${id}_val`).textContent = document.getElementById(id).value;
    });
}

['slider1','slider2','slider3','slider4'].forEach(id => {
    const el = document.getElementById(id);
    el.addEventListener('input', () => {
        updateSliderDisplays();
        generate();
    });
});

window.onload = updateSliderDisplays;