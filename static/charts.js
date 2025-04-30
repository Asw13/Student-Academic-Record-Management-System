document.addEventListener('DOMContentLoaded', () => {
    // Helper function to bin GPA data for histogram
    function binData(data, binSize = 0.5, min = 0, max = 4.0) {
        const bins = [];
        for (let i = min; i <= max; i += binSize) {
            bins.push({ x: i, y: 0 });
        }
        data.forEach(gpa => {
            const binIndex = Math.floor((gpa - min) / binSize);
            if (binIndex >= 0 && binIndex < bins.length) {
                bins[binIndex].y += 1;
            }
        });
        return bins.filter(bin => bin.y > 0); // Remove empty bins
    }

    try {
        // GPA Distribution Histogram
        const gpaCtx = document.getElementById('gpaChart');
        if (!gpaCtx) {
            console.error('GPA chart canvas not found');
            return;
        }
        if (!gpaData || gpaData.length === 0) {
            console.warn('No GPA data available');
            gpaCtx.parentElement.innerHTML += '<p class="text-red-500">No GPA data available</p>';
            return;
        }

        const binnedGpaData = binData(gpaData, 0.5, 0, 4.0);
        new Chart(gpaCtx.getContext('2d'), {
            type: 'bar',
            data: {
                datasets: [{
                    label: 'GPA Distribution',
                    data: binnedGpaData,
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1,
                    barPercentage: 1.0,
                    categoryPercentage: 1.0
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'linear',
                        title: { display: true, text: 'GPA' },
                        min: 0,
                        max: 4.0,
                        ticks: { stepSize: 0.5 }
                    },
                    y: {
                        title: { display: true, text: 'Count' },
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: { display: true }
                }
            }
        });

        // Attendance vs. GPA Scatter Plot
        const attendanceGpaCtx = document.getElementById('attendanceGpaChart');
        if (!attendanceGpaCtx) {
            console.error('Attendance GPA chart canvas not found');
            return;
        }
        if (!attendanceGpa || attendanceGpa.length === 0) {
            console.warn('No Attendance vs. GPA data available');
            attendanceGpaCtx.parentElement.innerHTML += '<p class="text-red-500">No Attendance vs. GPA data available</p>';
            return;
        }

        new Chart(attendanceGpaCtx.getContext('2d'), {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Attendance vs. GPA',
                    data: attendanceGpa,
                    backgroundColor: 'rgba(255, 99, 132, 0.5)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                    pointRadius: 5
                }]
            },
            options: {
                scales: {
                    x: {
                        title: { display: true, text: 'Attendance Rate (%)' },
                        min: 0,
                        max: 100
                    },
                    y: {
                        title: { display: true, text: 'GPA' },
                        min: 0,
                        max: 4.0
                    }
                },
                plugins: {
                    legend: { display: true }
                }
            }
        });
    } catch (error) {
        console.error('Error rendering charts:', error);
    }
});