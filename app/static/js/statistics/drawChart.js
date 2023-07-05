class DrawCharts {
    static drawSingleChart(
        $targetChart, chartType, xData, yData, label,
        color, title, subtitle, options,
    ) {
        const dataset = {
            labels: xData,
            datasets: [{
                label: label,
                data: yData,
                borderColor: color
            }],
        };

        const defaultOptions = {
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 6.5,
            scales: {
                x: {
                    title: {display: true, font: {size: 16}},
                    ticks: {display: true, font: {size: 16}}
                },
                y: {
                    title: {display: true, font: {size: 16}},
                    ticks: {display: true, font: {display: true, size: 16}}
                }
            },
            plugins: {
                legend: {
                    display: false,
                    labels: {font: {size: 16}}
                },
                title: {
                    display: true, text: title ? title: 'Title',
                    padding: {top: 0, bottom: 0},
                    font: {size: 16}
                },
                subtitle: {
                    display: true, text: subtitle ? subtitle: 'Subtitle',
                    padding: {top: 0, bottom: 10},
                    font: {size: 16}
                }
            },
            elements: {point:{radius: 3}}
        };
        options = Object.assign(defaultOptions, options);
        const config = {
            type: chartType,
            data: dataset,
            options: options
        };

        const chart = new Chart($targetChart.get(0).getContext("2d"), config);
    };
}
