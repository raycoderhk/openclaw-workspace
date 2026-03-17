const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/parsed_messages.json', 'utf8'));

const keywords = ['樓價', '房價', '物業', '成交', '呎價', '買賣', '賣樓', '置業', '樓市', 'property', '售價', '叫價', '議價', '地產', '經紀', '中原', '美聯'];
const matches = data.filter(d => {
    const text = String(d.text || '');
    return keywords.some(k => text.toLowerCase().includes(k.toLowerCase()));
});

console.log('🔍 搜索：樓價 / 物業成交');
console.log('');
console.log('📊 找到:', matches.length, '條');
console.log('');

if (matches.length > 0) {
    const priceRelevant = matches.filter(d => {
        const t = String(d.text);
        return t.includes('$') || t.includes('萬') || t.includes('呎') || t.includes('成交') || t.includes('售價') || t.includes('叫價');
    });
    
    console.log('=== 樓價/成交相關 (' + priceRelevant.length + '條) ===');
    console.log('');
    priceRelevant.slice(0, 20).forEach((m, i) => {
        console.log((i + 1) + '. [' + m.date + ' ' + m.time + '] ' + m.sender);
        console.log('   ' + String(m.text).substring(0, 200));
        console.log('');
    });
} else {
    console.log('❌ 未找到樓價相關討論');
}
