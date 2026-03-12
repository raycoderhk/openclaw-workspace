// Community Hub - Frontend App
// Loads classified tips and displays with filters

const CATEGORY_NAMES = {
    traffic: '🚗 交通',
    restaurant: '🍽️ 餐廳',
    doctor: '🏥 醫生',
    repair: '🔧 維修',
    tech_tip: '📱 科技',
    shopping: '🛒 購物',
    service: '📦 服務',
    community: '🏠 社區',
    event: '📅 活動',
    news: '📰 新聞',
    education: '📚 教育',
    childcare: '👶 親子'
};

let allTips = [];
let filteredTips = [];
let activeCategory = 'all';

// Load data
async function loadData() {
    try {
        const response = await fetch('classified_messages_useful.json');
        allTips = await response.json();
        
        // Sort by date (newest first)
        allTips.sort((a, b) => new Date(b.datetime) - new Date(a.datetime));
        
        updateStats();
        renderCategoryFilters();
        filterTips();
        
        document.getElementById('loading').style.display = 'none';
    } catch (error) {
        console.error('Error loading data:', error);
        document.getElementById('loading').innerHTML = '❌ 載入失敗，請刷新頁面';
    }
}

// Update statistics
function updateStats() {
    document.getElementById('total-tips').textContent = allTips.length;
    
    const categories = new Set(allTips.map(t => t.category));
    document.getElementById('total-categories').textContent = categories.size;
    
    const senders = new Set(allTips.map(t => t.sender));
    document.getElementById('total-senders').textContent = senders.size;
    
    // Date range
    const dates = allTips.map(t => t.date).sort();
    if (dates.length > 0) {
        const start = new Date(dates[0]).toLocaleDateString('zh-HK');
        const end = new Date(dates[dates.length - 1]).toLocaleDateString('zh-HK');
        document.getElementById('date-range').textContent = `${start} - ${end}`;
    }
    
    document.getElementById('last-update').textContent = new Date().toLocaleDateString('zh-HK', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Render category filter buttons
function renderCategoryFilters() {
    const categories = [...new Set(allTips.map(t => t.category))].sort();
    const container = document.getElementById('category-filters');
    
    categories.forEach(cat => {
        const btn = document.createElement('button');
        btn.className = 'filter-btn';
        btn.dataset.category = cat;
        btn.textContent = CATEGORY_NAMES[cat] || cat;
        btn.onclick = () => setCategory(cat);
        container.appendChild(btn);
    });
}

// Set active category
function setCategory(category) {
    activeCategory = category;
    
    // Update button states
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.category === category);
    });
    
    filterTips();
}

// Filter tips based on search and category
function filterTips() {
    const searchTerm = document.getElementById('search').value.toLowerCase();
    
    filteredTips = allTips.filter(tip => {
        // Category filter
        if (activeCategory !== 'all' && tip.category !== activeCategory) {
            return false;
        }
        
        // Search filter
        if (searchTerm) {
            const searchText = [
                tip.text,
                tip.summary,
                tip.sender,
                ...(tip.entities || [])
            ].join(' ').toLowerCase();
            
            if (!searchText.includes(searchTerm)) {
                return false;
            }
        }
        
        return true;
    });
    
    renderTips();
}

// Render tips
function renderTips() {
    const container = document.getElementById('tips-container');
    const noResults = document.getElementById('no-results');
    
    if (filteredTips.length === 0) {
        container.innerHTML = '';
        noResults.style.display = 'block';
        return;
    }
    
    noResults.style.display = 'none';
    container.innerHTML = filteredTips.map(tip => createTipCard(tip)).join('');
}

// Create tip card HTML
function createTipCard(tip) {
    const categoryClass = `category-${tip.category}`;
    const categoryName = CATEGORY_NAMES[tip.category] || tip.category;
    const date = new Date(tip.date).toLocaleDateString('zh-HK');
    const entities = (tip.entities || []).map(e => `<span class="entity-tag">${e}</span>`).join('');
    
    return `
        <div class="tip-card">
            <div class="tip-header">
                <span class="tip-category ${categoryClass}">${categoryName}</span>
                <span class="tip-date">${date}</span>
            </div>
            
            ${tip.summary ? `<div class="tip-summary">${tip.summary}</div>` : ''}
            
            <div class="tip-text">${escapeHtml(tip.text)}</div>
            
            <div class="tip-meta">
                <span>👤 ${escapeHtml(tip.sender)}</span>
                ${entities ? `<div class="tip-entities">${entities}</div>` : ''}
            </div>
        </div>
    `;
}

// Escape HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Event listeners
document.getElementById('search').addEventListener('input', filterTips);

// Initialize
document.addEventListener('DOMContentLoaded', loadData);
