// ============================================
// AI Stock Forecasting - Frontend JavaScript
// ============================================

let currentPrediction = null;
let charts = {};

// ============================================
// Initialize Application
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // Set default dates
    setDefaultDates();
    
    // Add event listeners
    const predictForm = document.getElementById('predictForm');
    if (predictForm) {
        predictForm.addEventListener('submit', handlePrediction);
    }
});

// ============================================
// Date Utilities
// ============================================

function setDefaultDates() {
    const endDateInput = document.getElementById('endDate');
    const startDateInput = document.getElementById('startDate');
    
    if (endDateInput && startDateInput) {
        const today = new Date();
        const twoYearsAgo = new Date();
        twoYearsAgo.setFullYear(today.getFullYear() - 2);
        
        endDateInput.value = formatDate(today);
        startDateInput.value = formatDate(twoYearsAgo);
    }
}

function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// ============================================
// Main Prediction Handler
// ============================================

async function handlePrediction(e) {
    e.preventDefault();
    
    const ticker = document.getElementById('ticker').value.toUpperCase().trim();
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    
    // Validate inputs
    if (!ticker) {
        showAlert('Please enter a stock ticker symbol', 'error');
        return;
    }
    
    if (!startDate || !endDate) {
        showAlert('Please select date range', 'error');
        return;
    }
    
    if (new Date(startDate) >= new Date(endDate)) {
        showAlert('End date must be after start date', 'error');
        return;
    }
    
    // Show loading
    showLoading(true);
    hideResults();
    
    try {
        // Make prediction request
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ticker: ticker,
                start_date: startDate,
                end_date: endDate
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Prediction failed');
        }
        
        // Store prediction data
        currentPrediction = data;
        
        // Display results
        displayResults(data);
        
        // Show success message
        showAlert(`Successfully analyzed ${ticker}`, 'success');
        
    } catch (error) {
        showAlert(error.message, 'error');
        console.error('Prediction error:', error);
    } finally {
        showLoading(false);
    }
}

// ============================================
// Display Results
// ============================================

function displayResults(data) {
    // Update company info
    document.getElementById('companyName').textContent = data.company_name;
    document.getElementById('tickerSymbol').textContent = data.ticker;
    
    // Update stat cards
    document.getElementById('currentPrice').textContent = `$${data.current_price.toFixed(2)}`;
    document.getElementById('predictedPrice').textContent = `$${data.predicted_price.toFixed(2)}`;
    
    // Price change
    const changeElement = document.getElementById('priceChange');
    const changeValue = data.price_change;
    const changePercent = data.price_change_percent;
    
    changeElement.innerHTML = `
        <span class="${changeValue >= 0 ? 'positive' : 'negative'}">
            ${changeValue >= 0 ? '▲' : '▼'} $${Math.abs(changeValue).toFixed(2)} (${Math.abs(changePercent).toFixed(2)}%)
        </span>
    `;
    
    // Data points
    document.getElementById('dataPoints').textContent = data.data_points;
    
    // Recommendation
    const recommendationBadge = document.getElementById('recommendation');
    recommendationBadge.textContent = data.recommendation;
    recommendationBadge.style.backgroundColor = data.recommendation_color;
    recommendationBadge.style.color = 'white';
    
    document.getElementById('recommendationReason').textContent = data.recommendation_reason;
    
    // Risk level
    const riskBadge = document.getElementById('riskLevel');
    riskBadge.textContent = `${data.risk_level} Risk`;
    riskBadge.style.backgroundColor = data.risk_color;
    riskBadge.style.color = 'white';
    
    document.getElementById('volatility').textContent = `${data.volatility.toFixed(2)}%`;
    
    // Best model
    document.getElementById('bestModel').textContent = data.model_comparison['Best Model'];
    
    // Last updated
    document.getElementById('lastUpdated').textContent = data.last_updated;
    
    // Create charts
    createCharts(data);
    
    // Display model comparison
    displayModelComparison(data.model_comparison);
    
    // Show results section
    showResults();
}

// ============================================
// Charts Creation
// ============================================

function createCharts(data) {
    // Destroy existing charts
    Object.values(charts).forEach(chart => {
        if (chart) chart.destroy();
    });
    charts = {};
    
    // 1. Historical Price Chart
    createHistoricalChart(data.chart_data.historical);
    
    // 2. Moving Averages Chart
    createMovingAveragesChart(data.chart_data.historical);
    
    // 3. Actual vs Predicted Chart
    createActualVsPredictedChart(data.chart_data.combined);
}

function createHistoricalChart(historicalData) {
    const ctx = document.getElementById('historicalChart');
    if (!ctx) return;
    
    charts.historical = new Chart(ctx, {
        type: 'line',
        data: {
            labels: historicalData.dates,
            datasets: [{
                label: 'Close Price',
                data: historicalData.close,
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: { color: '#a0aec0', font: { size: 12 } }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(26, 34, 56, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#a0aec0',
                    borderColor: '#2d3748',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    grid: { color: '#2d3748', drawBorder: false },
                    ticks: { 
                        color: '#a0aec0',
                        maxTicksLimit: 10
                    }
                },
                y: {
                    grid: { color: '#2d3748', drawBorder: false },
                    ticks: { 
                        color: '#a0aec0',
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

function createMovingAveragesChart(historicalData) {
    const ctx = document.getElementById('movingAveragesChart');
    if (!ctx) return;
    
    charts.movingAverages = new Chart(ctx, {
        type: 'line',
        data: {
            labels: historicalData.dates,
            datasets: [
                {
                    label: 'Close Price',
                    data: historicalData.close,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.05)',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4,
                    pointRadius: 0
                },
                {
                    label: 'MA 7',
                    data: historicalData.ma7,
                    borderColor: '#10b981',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4,
                    pointRadius: 0
                },
                {
                    label: 'MA 21',
                    data: historicalData.ma21,
                    borderColor: '#f59e0b',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4,
                    pointRadius: 0
                },
                {
                    label: 'MA 50',
                    data: historicalData.ma50,
                    borderColor: '#ef4444',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: { color: '#a0aec0', font: { size: 12 } }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(26, 34, 56, 0.9)',
                    titleColor: '#fff',
                    bodyColor: '#a0aec0',
                    borderColor: '#2d3748',
                    borderWidth: 1
                }
            },
            scales: {
                x: {
                    grid: { color: '#2d3748', drawBorder: false },
                    ticks: { 
                        color: '#a0aec0',
                        maxTicksLimit: 10
                    }
                },
                y: {
                    grid: { color: '#2d3748', drawBorder: false },
                    ticks: { 
                        color: '#a0aec0',
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

function createActualVsPredictedChart(combinedData) {
    const ctx = document.getElementById('predictionChart');
    if (!ctx) return;
    
    charts.prediction = new Chart(ctx, {
        type: 'line',
        data: {
            labels: combinedData.dates,
            datasets: [
                {
                    label: 'Actual Price',
                    data: combinedData.actual,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 3,
                    pointHoverRadius: 6
                },
                {
                    label: 'Predicted Price',
                    data: combinedData.predicted,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.1)',
                    borderWidth: 3,
                    borderDash: [5, 5],
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointHoverRadius: 7,
                    pointStyle: 'circle'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: { 
                        color: '#a0aec0',
                        font: { size: 14, weight: 'bold' },
                        padding: 15
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'rgba(26, 34, 56, 0.95)',
                    titleColor: '#fff',
                    bodyColor: '#a0aec0',
                    borderColor: '#3b82f6',
                    borderWidth: 2,
                    padding: 12,
                    displayColors: true
                }
            },
            scales: {
                x: {
                    grid: { color: '#2d3748', drawBorder: false },
                    ticks: { 
                        color: '#a0aec0',
                        maxTicksLimit: 12
                    }
                },
                y: {
                    grid: { color: '#2d3748', drawBorder: false },
                    ticks: { 
                        color: '#a0aec0',
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        }
    });
}

// ============================================
// Model Comparison Display
// ============================================

function displayModelComparison(modelComparison) {
    const tbody = document.getElementById('modelComparisonBody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    const bestModel = modelComparison['Best Model'];
    delete modelComparison['Best Model'];
    
    for (const [modelName, metrics] of Object.entries(modelComparison)) {
        const row = document.createElement('tr');
        const isBest = modelName === bestModel;
        
        row.innerHTML = `
            <td ${isBest ? 'class="best-model"' : ''}>${modelName} ${isBest ? '⭐' : ''}</td>
            <td>${metrics.RMSE.toFixed(4)}</td>
            <td>${metrics.MAE.toFixed(4)}</td>
        `;
        
        tbody.appendChild(row);
    }
}

// ============================================
// UI Helper Functions
// ============================================

function showLoading(show) {
    const loadingContainer = document.getElementById('loadingContainer');
    const predictButton = document.getElementById('predictButton');
    
    if (show) {
        loadingContainer.classList.add('active');
        if (predictButton) {
            predictButton.disabled = true;
            predictButton.innerHTML = '<span class="spinner-small"></span> Analyzing...';
        }
    } else {
        loadingContainer.classList.remove('active');
        if (predictButton) {
            predictButton.disabled = false;
            predictButton.innerHTML = '📈 Predict Stock Price';
        }
    }
}

function showResults() {
    const resultsSection = document.getElementById('resultsSection');
    if (resultsSection) {
        resultsSection.classList.remove('hidden');
        resultsSection.classList.add('fade-in');
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function hideResults() {
    const resultsSection = document.getElementById('resultsSection');
    if (resultsSection) {
        resultsSection.classList.add('hidden');
    }
}

function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer');
    if (!alertContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} fade-in`;
    
    const icon = type === 'error' ? '❌' : type === 'success' ? '✅' : 'ℹ️';
    alert.innerHTML = `<span>${icon}</span><span>${message}</span>`;
    
    alertContainer.innerHTML = '';
    alertContainer.appendChild(alert);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        alert.remove();
    }, 5000);
}

// ============================================
// Utility Functions
// ============================================

function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
}

function formatPercent(value) {
    return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`;
}
