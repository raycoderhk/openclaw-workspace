const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/parsed_messages.json', 'utf8'));

const keywords = ['OLIVE', 'Olive', 'olive', '2.0 茶餐廳', '泰 2.0', '同一老闆', '海之戀', '荃灣 餐廳', '西餐', '意粉', '牛排'];
const matches = data.filter(d => {
    const text = String(d.text || '');
    return keywords.some(k => text.toLowerCase().includes(k.toLowerCase()));
});

console.log('🔍 搜索：OLIVE / 2.0 茶餐廳 / 王子廚房');
console.log('');
console.log('📊 找到:', matches.length, '條');
console.log('');

if (matches.length > 0) {
    const relevant = matches.filter(d => {
        const t = String(d.text);
        return t.includes('好') || t.includes('推薦') || t.includes('食') || t.includes('價錢') || t.includes('價') || t.includes('$') || t.includes('開') || t.includes('結');
    });
    
    console.log('=== OLIVE / 2.0 茶餐廳相關記錄 ===');
    console.log('');
    relevant.sort((a, b) => a.date.localeCompare(b.date)).forEach((m, i) => {
        console.log((i + 1) + '. [' + m.date + ' ' + m.time + '] ' + m.sender);
        console.log('   ' + String(m.text).substring(0, 250));
        console.log('');
    });
} else {
    console.log('❌ 未找到相關討論');
}
