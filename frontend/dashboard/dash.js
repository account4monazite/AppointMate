document.addEventListener('DOMContentLoaded', () => {
    loadAppointments();
    loadTests();
    updateCounters();

    document.getElementById('appointmentsContainer').style.display = 'block';
    document.getElementById('testsContainer').style.display = 'none';
    document.getElementById('prescriptionsContainer').style.display = 'none';
});

function loadAppointments() {
    let appts = JSON.parse(localStorage.getItem("appointments")) || [];
    if (!Array.isArray(appts)) appts = [appts];

    const container = document.getElementById('appointmentsContainer');
    container.innerHTML = '';

    if (appts.length === 0) {
        container.innerHTML = `<p style="text-align:center; color:#666;">No appointments yet.</p>`;
        return;
    }

    appts.sort((a, b) => new Date(a.date) - new Date(b.date));

    appts.forEach(a => {
        const card = document.createElement('div');
        card.className = 'appt';
        card.innerHTML = `
            <div class="doctor-info">
                <h3>${a.doc}</h3>
                <p>${a.date} | ${a.time}</p>
            </div>
            <div class="status confirmed">Confirmed</div>
        `;
        container.appendChild(card);
    });
}

function loadTests() {
    let tests = JSON.parse(localStorage.getItem("tests")) || [];
    if (!Array.isArray(tests)) tests = [tests];

    const container = document.getElementById('testsContainer');
    container.innerHTML = '';

    if (tests.length === 0) {
        container.innerHTML = `<p style="text-align:center; color:#666;">No tests booked yet.</p>`;
        return;
    }

    tests.sort((a, b) => new Date(a.date) - new Date(b.date));

    tests.forEach(t => {
        const card = document.createElement('div');
        card.className = 'appt';
        card.innerHTML = `
            <div class="doctor-info">
                <h3>${t.test}</h3>
                <p>${t.date} | ${t.time}</p>
            </div>
            <div class="status confirmed">Confirmed</div>
        `;
        container.appendChild(card);
    });
}

function updateCounters() {
    const appts = JSON.parse(localStorage.getItem("appointments")) || [];
    const tests = JSON.parse(localStorage.getItem("tests")) || [];
    document.getElementById('apptCount').innerText = Array.isArray(appts) ? appts.length : 1;
    document.getElementById('testCount').innerText = Array.isArray(tests) ? tests.length : 1;
}

document.querySelector('[data-page="book"]').addEventListener('click', () => {
    document.getElementById('appointmentsContainer').style.display = 'block';
    document.getElementById('testsContainer').style.display = 'none';
    document.getElementById('prescriptionsContainer').style.display = 'none';
    loadAppointments();
});

document.querySelector('[data-page="tests"]').addEventListener('click', () => {
    document.getElementById('appointmentsContainer').style.display = 'none';
    document.getElementById('testsContainer').style.display = 'block';
    document.getElementById('prescriptionsContainer').style.display = 'none';
    loadTests();
});

document.querySelector('[data-page="prescription"]').addEventListener('click', () => {
    document.getElementById('appointmentsContainer').style.display = 'none';
    document.getElementById('testsContainer').style.display = 'none';
    document.getElementById('prescriptionsContainer').style.display = 'block';
});

document.getElementById('logout')?.addEventListener('click', () => {
    if (confirm('Are you sure you want to log out?')) {
        sessionStorage.clear();
        window.location.href = '/login_signup/Log-in.html';
    }
});
