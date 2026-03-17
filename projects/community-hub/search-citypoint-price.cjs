const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/parsed_messages.json', 'utf8'));

const keywords = ['愉景新城', 'citypoint', '荃灣 樓', '三房', '兩房', '呎價', '成交', '售價', '叫價', '萬', '物業'];
const matches = data.filter(d => {
    const text = String(d.text || '');
    return keywords.some(k => text.includes(k));
});

console.log('🔍 搜索：愉景新城 樓價成交');
console.log('');
console.log('📊 找到:', matches.length, '條');
console.log('');

if (matches.length > 0) {
    const priceRelevant = matches.filter(d => {
        const t = String(d.text);
        return t.includes('$') || t.includes('萬') || t.includes('呎') || t.includes('成交') || t.includes('售價') || t.includes('叫價') || t.includes('沽') || t.includes('售');
    });
    
    console.log('=== 愉景新城成交記錄 ===');
    console.log('');
    priceRelevant.sort((a, b) => a.date.localeCompare(b.date)).forEach((m, i) => {
        console.log((i + 1) + '. [' + m.date + ' ' + m.time + '] ' + m.sender);
        console.log('   ' + String(m.text).substring(0, 250));
        console.log('');
    });
} else {
    console.log('❌ 未找到愉景新城成交記錄');
}
