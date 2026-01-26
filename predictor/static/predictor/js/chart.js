function drawPieChart(labels, values, startAge, endAge) {
  const canvas = document.getElementById("pieChart");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");

  // Get responsive size based on container
  const container = canvas.parentElement;
  const containerWidth = container.offsetWidth;
  const size = Math.min(containerWidth - 40, 500); // Subtract padding

  // Set canvas size with device pixel ratio for sharp rendering
  const dpr = window.devicePixelRatio || 1;
  canvas.width = size * dpr;
  canvas.height = size * dpr;
  canvas.style.width = size + "px";
  canvas.style.height = size + "px";
  ctx.scale(dpr, dpr);

  const centerX = size / 2;
  const centerY = size / 2;
  const radius = size / 2.5;

  // Define colors
  const colors = {
    Stayed: "#3498db",
    Left: "#e74c3c",
  };

  // Calculate total and percentages
  const total = values.reduce((sum, val) => sum + val, 0);
  let currentAngle = -Math.PI / 2; // Start at top

  // Clear canvas
  ctx.clearRect(0, 0, size, size);

  // Draw pie slices
  labels.forEach((label, index) => {
    const sliceAngle = (values[index] / total) * 2 * Math.PI;
    const percentage = ((values[index] / total) * 100).toFixed(1);

    // Draw slice
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
    ctx.closePath();
    ctx.fillStyle = colors[label] || "#95a5a6";
    ctx.fill();

    // Draw border
    ctx.strokeStyle = "#fff";
    ctx.lineWidth = 2;
    ctx.stroke();

    // Draw percentage text with responsive font size
    const fontSize = Math.max(14, size / 22);
    const textAngle = currentAngle + sliceAngle / 2;
    const textX = centerX + Math.cos(textAngle) * (radius * 0.7);
    const textY = centerY + Math.sin(textAngle) * (radius * 0.7);

    ctx.fillStyle = "#fff";
    ctx.font = `bold ${fontSize}px Arial`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(percentage + "%", textX, textY);

    currentAngle += sliceAngle;
  });

  // Update legend
  updateLegend(labels, values);
}

// Add window resize handler
let resizeTimeout;
window.addEventListener('resize', function() {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(function() {
        const chartData = window.chartDataGlobal;
        if (chartData) {
            drawPieChart(chartData.labels, chartData.values, chartData.startAge, chartData.endAge);
        }
    }, 250);
});

function updateLegend(labels, values) {
    const legendContainer = document.querySelector('.chart-legend');
    legendContainer.innerHTML = '';
    
    labels.forEach((label, index) => {
        const legendItem = document.createElement('div');
        legendItem.className = 'legend-item';
        
        const colorClass = label.toLowerCase();
        legendItem.innerHTML = `
            <div class="legend-color ${colorClass}"></div>
            <span class="legend-text">${label}:</span>
            <span class="legend-value">${values[index]}</span>
        `;
        
        legendContainer.appendChild(legendItem);
    });
}
