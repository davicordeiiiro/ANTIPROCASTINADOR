let localInterval = null;
let backgroundEndTime = 0;

const timerDisplay = document.getElementById('timerDisplay');
const btnStart = document.getElementById('btnStart');
const txtTarefa = document.getElementById('txtTarefa');
const txtTech = document.getElementById('txtTech');
const txtMinutos = document.getElementById('txtMinutos');
const containerTimer = document.querySelector('.container-timer');
const btnReset = document.getElementById('btnReset');
const tableBody = document.getElementById('tableBody');
const txtSites = document.getElementById('txtSites');
const btnSaveSites = document.getElementById('btnSaveSites');

document.addEventListener('DOMContentLoaded', () => {
  carregarRelatorio();
  syncWithBackground();
});

function formatTime(secs) {
  if (secs < 0) secs = 0;
  const m = Math.floor(secs / 60).toString().padStart(2, '0');
  const s = (Math.floor(secs) % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
}

function syncWithBackground() {
  chrome.runtime.sendMessage({ action: 'GET_STATE' }, (resp) => {
    if (resp) {
      if (resp.endTime > Date.now()) {
        // Timer is running
        backgroundEndTime = resp.endTime;
        setUiActive(true);
        startLocalTick();
      }
      if (resp.allowedSites) {
        txtSites.value = resp.allowedSites.join('\n');
      }
    }
  });
}

function setUiActive(isActive) {
  if (isActive) {
    btnStart.innerHTML = '<span class="icon">⏳</span> FOCO EM ANDAMENTO';
    btnStart.classList.add('active');
    containerTimer.classList.add('active');
    btnStart.disabled = true;
    txtTarefa.disabled = true;
    txtTech.disabled = true;
    txtMinutos.disabled = true;
  } else {
    btnStart.innerHTML = '<span class="icon">🚀</span> INICIAR CICLO DE FOCO';
    btnStart.classList.remove('active');
    containerTimer.classList.remove('active');
    btnStart.disabled = false;
    txtTarefa.disabled = false;
    txtTech.disabled = false;
    txtMinutos.disabled = false;
    timerDisplay.textContent = '00:00';
  }
}

function startLocalTick() {
  if (localInterval) clearInterval(localInterval);
  
  localInterval = setInterval(() => {
    const restante = (backgroundEndTime - Date.now()) / 1000;
    if (restante <= 0) {
      clearInterval(localInterval);
      setUiActive(false);
      carregarRelatorio(); // Refresh charts in case focus just ended
    } else {
      timerDisplay.textContent = formatTime(restante);
    }
  }, 1000);
}

btnStart.addEventListener('click', () => {
  const tarefa = txtTarefa.value.trim();
  const tech = txtTech.value.trim();
  const mins = parseInt(txtMinutos.value);

  if (!tarefa || !tech || isNaN(mins) || mins <= 0) {
    alert('Preencha a Tarefa e a Tecnologia, e informe os Minutos corretamente!');
    return;
  }

  const sitesRaw = txtSites.value.split('\n');
  const sites = sitesRaw.map(s => s.trim()).filter(s => s.length > 0);

  chrome.runtime.sendMessage({
    action: 'SET_SITES',
    sites: sites
  }, () => {
    // Now start timer
    chrome.runtime.sendMessage({
      action: 'START_TIMER',
      tech: tech,
      mins: mins
    }, (resp) => {
      if (resp && resp.success) {
        backgroundEndTime = resp.endTime;
        setUiActive(true);
        startLocalTick();
      }
    });
  });
});

btnSaveSites.addEventListener('click', () => {
  const sitesRaw = txtSites.value.split('\n');
  const sites = sitesRaw.map(s => s.trim()).filter(s => s.length > 0);
  
  chrome.runtime.sendMessage({
    action: 'SET_SITES',
    sites: sites
  }, () => {
    btnSaveSites.textContent = '✅';
    setTimeout(() => { btnSaveSites.textContent = '💾'; }, 2000);
  });
});

function carregarRelatorio() {
  chrome.storage.local.get(['historico'], (result) => {
    const relatorio = result.historico || {};
    tableBody.innerHTML = '';

    const techs = Object.keys(relatorio);
    if(techs.length === 0) {
      tableBody.innerHTML = '<tr><td colspan="2">Nenhum registro ainda.</td></tr>';
      return;
    }

    techs.forEach((tech) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${tech}</td>
        <td class="tech-val">${relatorio[tech]}m</td>
      `;
      tableBody.appendChild(tr);
    });
  });
}

btnReset.addEventListener('click', () => {
  if(confirm('Deseja zerar todo o histórico de desempenho?')) {
    chrome.storage.local.set({ historico: {} }, () => {
      carregarRelatorio();
    });
  }
});
