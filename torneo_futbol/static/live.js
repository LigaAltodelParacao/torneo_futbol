document.addEventListener('DOMContentLoaded', () => {
  const teamSelect = document.getElementById('teamSelect');
  const playerSelect = document.getElementById('playerSelect');
  if (teamSelect && playerSelect) {
    const syncPlayers = () => {
      const team = teamSelect.value;
      for (const opt of playerSelect.options) {
        if (!opt.dataset.team) continue;
        opt.hidden = opt.dataset.team !== team;
      }
      // if currently selected player is hidden, clear selection
      if (playerSelect.selectedOptions.length === 0 || playerSelect.selectedOptions[0].hidden) {
        playerSelect.value = '';
      }
    };
    teamSelect.addEventListener('change', syncPlayers);
    syncPlayers();
  }

  const timer = document.getElementById('timer');
  if (timer) {
    const status = timer.dataset.status;
    // only start ticking when match status is 'live'
    if (status === 'live') {
      let seconds = 0;
      const startedAt = timer.dataset.startedAt;
      if (startedAt) {
        const diff = Date.now() - Date.parse(startedAt);
        if (!isNaN(diff) && diff > 0) seconds = Math.floor(diff / 1000);
      }
      const limit = 30 * 60; // 30 minutes per half
      const updateTimer = () => {
        const mm = Math.floor(seconds / 60).toString().padStart(2, '0');
        const ss = (seconds % 60).toString().padStart(2, '0');
        timer.textContent = `${timer.dataset.half}°T ${mm}:${ss}`;
      };
      updateTimer();
      const h = setInterval(() => {
        seconds++;
        updateTimer();
        if (seconds >= limit) clearInterval(h);
      }, 1000);
    } else {
      // show initial static time
      timer.textContent = `${timer.dataset.half}°T 00:00`;
    }
  }

  // set minute from timer when submitting event form
  const addEventForm = document.querySelector('.add-event form');
  if (addEventForm) {
    addEventForm.addEventListener('submit', (ev) => {
      const minuteInput = addEventForm.querySelector('input[name="minute"]');
      const playerSel = addEventForm.querySelector('select[name="player_id"]');
      if (playerSel && !playerSel.value) {
        ev.preventDefault();
        alert('Seleccione un jugador (obligatorio).');
        return false;
      }
      if (timer && minuteInput) {
        const txt = timer.textContent.trim();
        const m = txt.match(/(\d+)°T\s(\d{2}):(\d{2})/);
        let minutes = 0;
        if (m) {
          minutes = parseInt(m[2], 10);
        } else {
          minutes = parseInt(minuteInput.value || '0', 10) || 0;
        }
        minuteInput.value = minutes;
      }
    });
  }

});
