let timerInterval = null;
let segundosRestantes = 0;

const timerDisplay = document.getElementById('timerDisplay');
const btnStart = document.getElementById('btnStart');
const txtTarefa = document.getElementById('txtTarefa');
const txtTech = document.getElementById('txtTech');
const txtMinutos = document.getElementById('txtMinutos');
const containerTimer = document.querySelector('.container-timer');
const btnReset = document.getElementById('btnReset');
const tableBody = document.getElementById('tableBody');

// Inicialização e Carga de Dados
document.addEventListener('DOMContentLoaded', () => {
  carregarRelatorio();
});

function formatTime(secs) {
  const m = Math.floor(secs / 60).toString().padStart(2, '0');
  const s = (secs % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
}

btnStart.addEventListener('click', () => {
  if (timerInterval) return;

  const tarefa = txtTarefa.value.trim();
  const tech = txtTech.value.trim();
  const mins = parseInt(txtMinutos.value);

  if (!tarefa || !tech || isNaN(mins) || mins <= 0) {
    alert('Preencha a Tarefa e a Tecnologia, e informe os Minutos corretamente!');
    return;
  }

  // Configurações UI estado Inativo -> Iniciando
  btnStart.innerHTML = '<span class="icon">⏳</span> FOCO EM ANDAMENTO';
  btnStart.classList.add('active');
  containerTimer.classList.add('active');
  btnStart.disabled = true;
  txtTarefa.disabled = true;
  txtTech.disabled = true;
  txtMinutos.disabled = true;

  segundosRestantes = mins * 60;
  timerDisplay.textContent = formatTime(segundosRestantes);

  timerInterval = setInterval(() => {
    segundosRestantes--;
    timerDisplay.textContent = formatTime(segundosRestantes);

    if (segundosRestantes <= 0) {
      finalizarFoco(tarefa, tech, mins);
    }
  }, 1000);
});

function finalizarFoco(tarefa, tech, mins) {
  clearInterval(timerInterval);
  timerInterval = null;

  // Salva no Chrome Storage
  salvarProgresso(tech, mins);

  // Notificação web nativa
  chrome.notifications.create({
    type: 'basic',
    iconUrl: 'icon128.png', // Fallbacks no Manifest mas aceito se ausente internamente
    title: '🚀 Fim do Ciclo!',
    message: `Você concluiu ${mins} min em ${tech}.`
  });

  // Reset UI
  timerDisplay.textContent = '00:00';
  btnStart.innerHTML = '<span class="icon">🚀</span> INICIAR CICLO DE FOCO';
  btnStart.classList.remove('active');
  containerTimer.classList.remove('active');

  btnStart.disabled = false;
  txtTarefa.disabled = false;
  txtTech.disabled = false;
  txtMinutos.disabled = false;
}

function salvarProgresso(tech, mins) {
  chrome.storage.local.get(['historico'], (result) => {
    let relatorio = result.historico || {};
    relatorio[tech] = (relatorio[tech] || 0) + mins;
    
    chrome.storage.local.set({ historico: relatorio }, () => {
      carregarRelatorio();
    });
  });
}

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
