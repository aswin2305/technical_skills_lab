function startTimer(deadlineISO) {
    const timerEl = document.getElementById('timer');
    const deadline = new Date(deadlineISO).getTime();

    const interval = setInterval(function () {
        const now = new Date().getTime();
        const distance = deadline - now;

        if (distance <= 0) {
            clearInterval(interval);
            timerEl.textContent = "00:00";
            alert("Time's up! Submitting your test automatically.");
            syncAllEditorsToTextareas();
            document.getElementById('testForm').submit();
            return;
        }

        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        timerEl.textContent =
            String(minutes).padStart(2, '0') + ":" + String(seconds).padStart(2, '0');
    }, 1000);
}

startTimer(deadlineISO);