const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/parsed_messages.json', 'utf8'));

const keywords = ['D-PARK', 'DPARK', 'D PARK', '商場', '新世界', '華懋', '40 億', '出售', '沽', '轉手', '成交', '零售', '停車場'];
const matches = data.filter(d => {
    const text = String(d.text || '');
    return keywords.some(k => text.includes(k));
});

console.log('🔍 搜索：愉景新城商場轉手');
console.log('');
console.log('📊 找到:', matches.length, '條');
console.log('');

if (matches.length > 0) {
    const relevant = matches.filter(d => {
        const t = String(d.text);
        return t.includes('40') || t.includes('億') || t.includes('新世界') || t.includes('華懋') || t.includes('出售') || t.includes('沽') || t.includes('成交');
    });
    
    console.log('=== 商場轉手相關記錄 ===');
    console.log('');
    relevant.sort((a, b) => a.date.localeCompare(b.date)).forEach((m, i) => {
        console.log((i + 1) + '. [' + m.date + ' ' + m.time + '] ' + m.sender);
        console.log('   ' + String(m.text).substring(0, 250));
        console.log('');
    });
} else {
    console.log('❌ 未找到商場轉手記錄');
}
