const socket = io();
const form = document.getElementById('transaction-form');
const chartCanvas = document.getElementById('chart');
const adviceText = document.getElementById('advice');

let chart;
let income = 0, expense = 0;

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const amount = parseFloat(document.getElementById('amount').value);
    const type = document.getElementById('type').value;

    const data = { name, amount, type };

    await fetch('/add_transaction', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    document.getElementById('name').value = '';
    document.getElementById('amount').value = '';
});

socket.on('new_transaction', data => {
    if (data.type === 'income') income += parseFloat(data.amount);
    else expense += parseFloat(data.amount);
    updateChart();
    fetchAdvice();
});

function updateChart() {
    if (chart) chart.destroy();
    chart = new Chart(chartCanvas, {
        type: 'pie',
        data: {
            labels: ['Income', 'Expense'],
            datasets: [{
                data: [income, expense],
                backgroundColor: ['green', 'red']
            }]
        }
    });
}

async function fetchAdvice() {
    const res = await fetch('/advice');
    const data = await res.json();
    adviceText.textContent = data.advice;
}