const activeCharts = {};

function writeChart(ctx, list, _data, color, about ,type) {
    if (activeCharts[ctx.canvas.id]) {
        activeCharts[ctx.canvas.id].destroy();
    }
    const chart = new Chart(ctx, {
        type: type,
        data: {
            labels: list,
            datasets: [{
                label: about,
                data: _data,
                backgroundColor: color
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    activeCharts[ctx.canvas.id] = chart;
}

function processHiddenData() {
    const chartDataBlocks = document.querySelectorAll('.data');

    chartDataBlocks.forEach((block) => {
        const type_class = `.type_${block.id}`;
        let type = Array.from(document.querySelectorAll(type_class)).map(el => el.textContent.trim());
        if (type.length == 0) {
            type = ['bar', 'bar'];
        }
        let names = block.querySelectorAll('thead th');
        let num_of_columns = names.length;

        const values = Array.from(block.querySelectorAll('tbody th')).map(el => el.textContent.trim().replace(" %", ""));

        if (num_of_columns == 3) {
            
            let canvasId = `chart_${block.id}1`;
            let canvas1 = document.getElementById(canvasId);
            const ctx1 = canvas1.getContext('2d');
            
            canvasId = `chart_${block.id}2`;
            let canvas2 = document.getElementById(canvasId);
            const ctx2 = canvas2.getContext('2d');

            const headers = values.filter((_, index) => index % 3 == 0 && _ != 'Показать еще');
            const value1 = values.filter((_, index) => index % 3 !== 2).filter((_, index) => index % 2 !== 0 && _ != '').map(el => parseFloat(el));
            const value2 = values.filter((_, index) => index % 3 !== 0).filter((_, index) => index % 2 !== 0 && _ != '').map(el => parseFloat(el));

            writeChart(ctx1, headers, value1, undefined, names[1].innerText, type[0]);
            writeChart(ctx2, headers, value2, undefined, names[2].innerText, type[1]);
        } else {

            let canvasId = `chart_${block.id}`;
            let canvas = document.getElementById(canvasId);
            const ctx = canvas.getContext('2d');

            const headers = values.filter((_, index) => index % 2 == 0 && _ != 'Показать еще');
            const value1 = values.filter((_, index) => index % 2 == 1 && _ != '').map(el => parseFloat(el));
            writeChart(ctx, headers, value1, undefined, names[1].innerText, type[0]);
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    processHiddenData();
});