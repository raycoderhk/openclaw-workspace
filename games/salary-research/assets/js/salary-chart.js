// Salary Comparison Chart Generator
// Uses Chart.js to create interactive box plot charts

let salaryData = [];

// Load salary data from JSON
async function loadSalaryData() {
    try {
        const response = await fetch('data/salary-data.json');
        const data = await response.json();
        salaryData = data.industries;
        
        // Sort by median salary (low to high)
        salaryData.sort((a, b) => a.salary.median - b.salary.median);
        
        initCharts();
    } catch (error) {
        console.error('Error loading salary data:', error);
        alert('無法載入薪金數據，請稍後再試');
    }
}

// Initialize all charts
function initCharts() {
    createSalaryBoxPlot();
    createHoursChart();
    createStressChart();
    createProspectsChart();
}

// Create Salary Box Plot Chart
function createSalaryBoxPlot() {
    const ctx = document.getElementById('salaryChart').getContext('2d');
    
    const labels = salaryData.map(ind => {
        const emoji = ind.id.includes('game') ? '🎮 ' : '';
        return emoji + ind.name.split(' (')[0];
    });
    
    // Calculate IQR segments (25th to 75th)
    const iqrData = salaryData.map(ind => (ind.salary.upperQuartile - ind.salary.lowerQuartile) / 1000);
    
    // Box plot data - show IQR as main bar, whiskers as thin lines
    const boxData = {
        labels: labels,
        datasets: [
            // IQR Bar (25th to 75th) - main visible bar
            {
                type: 'bar',
                label: 'IQR (25th-75th) - 中間 50%',
                data: iqrData,
                // Start from 25th percentile (using chartjs plugin or offset)
                backgroundColor: 'rgba(52, 152, 219, 0.9)',  // 🔵 Blue
                borderColor: 'rgba(40, 120, 180, 1)',
                borderWidth: 2,
                barPercentage: 0.6,
                categoryPercentage: 0.8
            },
            // Median line overlay
            {
                type: 'scatter',
                label: 'Median (50th) - 中位數',
                data: salaryData.map((ind, i) => ({
                    x: ind.salary.median / 1000,
                    y: i
                })),
                backgroundColor: 'rgba(231, 76, 60, 1)',  // 🔴 Red
                borderColor: 'rgba(231, 76, 60, 1)',
                pointRadius: 8,
                pointHoverRadius: 10,
                pointStyle: 'rectRot',
                rotation: 0,
                order: -1
            },
            // Bottom whisker (10th to 25th) - thin line
            {
                type: 'scatter',
                label: 'Bottom (10th-25th)',
                data: salaryData.map((ind, i) => ({
                    x: ind.salary.bottom / 1000,
                    y: i
                })),
                backgroundColor: 'rgba(230, 126, 34, 1)',  // 🟠 Orange
                borderColor: 'rgba(230, 126, 34, 1)',
                pointRadius: 4,
                pointHoverRadius: 6,
                pointStyle: 'line',
                rotation: 90,
                order: 0
            },
            // Top whisker (75th to 90th) - thin line
            {
                type: 'scatter',
                label: 'Top (75th-90th)',
                data: salaryData.map((ind, i) => ({
                    x: ind.salary.top / 1000,
                    y: i
                })),
                backgroundColor: 'rgba(155, 89, 182, 1)',  // 🟣 Purple
                borderColor: 'rgba(155, 89, 182, 1)',
                pointRadius: 4,
                pointHoverRadius: 6,
                pointStyle: 'line',
                rotation: 90,
                order: 0
            }
        ]
    };
    
    const config = {
        type: 'bar',
        data: boxData,
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const ind = salaryData[context.dataIndex];
                            const monthlyMedian = (ind.salary.median / 12).toLocaleString(undefined, {maximumFractionDigits: 0});
                            return [
                                `💰 中位數：HK$${monthlyMedian}/月`,
                                `📊 10th: HK$${(ind.salary.bottom/1000).toFixed(0)}K`,
                                `📊 25th: HK$${(ind.salary.lowerQuartile/1000).toFixed(0)}K`,
                                `📊 75th: HK$${(ind.salary.upperQuartile/1000).toFixed(0)}K`,
                                `📊 90th: HK$${(ind.salary.top/1000).toFixed(0)}K`,
                                ``,
                                `⏰ 工時：${ind.workingHours.median} 小時/週`,
                                `😰 壓力：${ind.stressLevel.score}/10`,
                                `📈 前景：${ind.prospects.score}/10`
                            ];
                        }
                    }
                },
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        boxWidth: 20,
                        generateLabels: function(chart) {
                            return [
                                {
                                    text: '🔵 IQR (25th-75th) - 中間 50%',
                                    fillStyle: 'rgba(52, 152, 219, 0.9)',
                                    strokeStyle: 'rgba(40, 120, 180, 1)',
                                    lineWidth: 2,
                                    hidden: false,
                                    datasetIndex: 0
                                },
                                {
                                    text: '🔴 Median (50th) - 中位數',
                                    fillStyle: 'rgba(231, 76, 60, 1)',
                                    strokeStyle: 'rgba(231, 76, 60, 1)',
                                    lineWidth: 2,
                                    pointStyle: 'rectRot',
                                    hidden: false,
                                    datasetIndex: 1
                                },
                                {
                                    text: '🟠 Bottom (10th-25th)',
                                    fillStyle: 'rgba(230, 126, 34, 1)',
                                    strokeStyle: 'rgba(230, 126, 34, 1)',
                                    lineWidth: 2,
                                    pointStyle: 'line',
                                    hidden: false,
                                    datasetIndex: 2
                                },
                                {
                                    text: '🟣 Top (75th-90th)',
                                    fillStyle: 'rgba(155, 89, 182, 1)',
                                    strokeStyle: 'rgba(155, 89, 182, 1)',
                                    lineWidth: 2,
                                    pointStyle: 'line',
                                    hidden: false,
                                    datasetIndex: 3
                                }
                            ];
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: '年薪 (HKD 千)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + value + 'K';
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: '職位',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        autoSkip: false,
                        font: {
                            size: 11
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// Create Working Hours Chart
function createHoursChart() {
    const ctx = document.getElementById('hoursChart').getContext('2d');
    
    // Sort by working hours (low to high)
    const sortedByHours = [...salaryData].sort((a, b) => a.workingHours.median - b.workingHours.median);
    
    const labels = sortedByHours.map(ind => ind.name.split(' (')[0]);
    const colors = sortedByHours.map(ind => {
        if (ind.workingHours.median <= 45) return 'rgba(39, 174, 96, 0.8)'; // Green
        if (ind.workingHours.median <= 50) return 'rgba(241, 196, 15, 0.8)'; // Yellow
        if (ind.workingHours.median <= 60) return 'rgba(243, 156, 18, 0.8)'; // Orange
        return 'rgba(231, 76, 60, 0.8)'; // Red
    });
    
    const data = {
        labels: labels,
        datasets: [{
            label: '每週工時 (小時)',
            data: sortedByHours.map(ind => ind.workingHours.median),
            backgroundColor: colors,
            borderColor: colors.map(c => c.replace('0.8', '1')),
            borderWidth: 1
        }]
    };
    
    const config = {
        type: 'bar',
        data: data,
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed.x;
                            const ind = sortedByHours[context.dataIndex];
                            return [
                                `中位數：${value} 小時/週`,
                                `範圍：${ind.workingHours.min}-${ind.workingHours.max} 小時`,
                                `${ind.workingHours.note}`
                            ];
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 80,
                    title: {
                        display: true,
                        text: '每週工時',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    ticks: {
                        callback: function(value) {
                            return value + 'h';
                        }
                    }
                },
                y: {
                    ticks: {
                        autoSkip: false,
                        font: {
                            size: 10
                        }
                    }
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// Create Stress Level Chart
function createStressChart() {
    const ctx = document.getElementById('stressChart').getContext('2d');
    
    // Sort by stress level (low to high)
    const sortedByStress = [...salaryData].sort((a, b) => a.stressLevel.score - b.stressLevel.score);
    
    const labels = sortedByStress.map(ind => ind.name.split(' (')[0]);
    const colors = sortedByStress.map(ind => {
        if (ind.stressLevel.score <= 4) return 'rgba(39, 174, 96, 0.8)'; // Green
        if (ind.stressLevel.score <= 6) return 'rgba(241, 196, 15, 0.8)'; // Yellow
        if (ind.stressLevel.score <= 8) return 'rgba(243, 156, 18, 0.8)'; // Orange
        return 'rgba(231, 76, 60, 0.8)'; // Red
    });
    
    const data = {
        labels: labels,
        datasets: [{
            label: '壓力指數 (1-10)',
            data: sortedByStress.map(ind => ind.stressLevel.score),
            backgroundColor: colors,
            borderColor: colors.map(c => c.replace('0.8', '1')),
            borderWidth: 1
        }]
    };
    
    const config = {
        type: 'bar',
        data: data,
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed.x;
                            const ind = sortedByStress[context.dataIndex];
                            return [
                                `壓力指數：${value}/10`,
                                `${ind.stressLevel.note}`
                            ];
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 10,
                    title: {
                        display: true,
                        text: '壓力指數 (1-10 分，越低越好)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    }
                },
                y: {
                    ticks: {
                        autoSkip: false,
                        font: {
                            size: 10
                        }
                    }
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// Create Career Prospects Chart
function createProspectsChart() {
    const ctx = document.getElementById('prospectsChart').getContext('2d');
    
    // Sort by prospects (high to low)
    const sortedByProspects = [...salaryData].sort((a, b) => b.prospects.score - a.prospects.score);
    
    const labels = sortedByProspects.map(ind => ind.name.split(' (')[0]);
    const colors = sortedByProspects.map(ind => {
        if (ind.prospects.score >= 8) return 'rgba(39, 174, 96, 0.8)'; // Green
        if (ind.prospects.score >= 6) return 'rgba(241, 196, 15, 0.8)'; // Yellow
        if (ind.prospects.score >= 4) return 'rgba(243, 156, 18, 0.8)'; // Orange
        return 'rgba(231, 76, 60, 0.8)'; // Red
    });
    
    const data = {
        labels: labels,
        datasets: [{
            label: '行業前景 (1-10)',
            data: sortedByProspects.map(ind => ind.prospects.score),
            backgroundColor: colors,
            borderColor: colors.map(c => c.replace('0.8', '1')),
            borderWidth: 1
        }]
    };
    
    const config = {
        type: 'bar',
        data: data,
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed.x;
                            const ind = sortedByProspects[context.dataIndex];
                            return [
                                `前景評分：${value}/10`,
                                `增長：${ind.prospects.growth}`,
                                `${ind.prospects.note}`
                            ];
                        }
                    }
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    max: 10,
                    title: {
                        display: true,
                        text: '行業前景 (1-10 分，越高越好)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    }
                },
                y: {
                    ticks: {
                        autoSkip: false,
                        font: {
                            size: 10
                        }
                    }
                }
            }
        }
    };
    
    new Chart(ctx, config);
}

// Add click event to career paths
function addCareerPathListeners() {
    document.querySelectorAll('.career-paths li').forEach(li => {
        li.addEventListener('click', function() {
            const roleName = this.getAttribute('data-role');
            if (roleName) {
                // Find the industry with matching ID
                const industry = salaryData.find(ind => ind.id === roleName);
                if (industry) {
                    alert(`${industry.name}\n\n薪金中位數：HK$${(industry.salary.median / 12).toLocaleString(undefined, {maximumFractionDigits: 0})}/月\n工時：${industry.workingHours.median} 小時/週\n壓力：${industry.stressLevel.score}/10\n前景：${industry.prospects.score}/10\n\n${industry.notes}`);
                }
            }
        });
    });
}

// Load data when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadSalaryData();
    addCareerPathListeners();
});
